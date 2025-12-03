#!/usr/bin/env python3
"""Convert VectorDBBench parquet (openai_small_50k) into text files for the
BUCKETED latte vector workload (the one-upload scaling-curve mode).

Replicates vector-search-benchmark's quantile stratification (data/mod.rs:116)
offline so latte never has to reimplement it in Rune: each train id is assigned
to one of 9 disjoint buckets sized ~1/2, 1/5, 1/10 ... 1/1000 of the dataset by
the same period algorithm (ids iterated in ascending order, as vsb's BTreeMap).

Outputs (into <dst>/):
  dataset_buckets.txt            "id, bucket, [v1, v2, ...]"   (all train rows)
  bucket/test_bucketN.txt        "v1, v2, ..."   query vectors with non-empty GT in bucket N
  bucket/gt_bucketN.txt          "id1, id2, ..." their bucket-N-local true neighbours, in order
for N in 0..8. Per-query GT is the global neighbour list filtered to bucket N
(vsb parquet.rs:369); only queries with a non-empty bucket-N GT are emitted
(vsb parquet.rs:377). recall@k in the workload then takes the first k.

Usage:
  uv run --with pyarrow parquet_to_bucket_text.py ~/datasets/openai_small_50k ~/datasets/sct-vector-text
"""

import sys
from pathlib import Path

import pyarrow.parquet as pq

# vsb max_buckets (data/mod.rs:127): assign 1 vector per N seen -> ~1/N of dataset.
MAX_BUCKETS = [2, 5, 10, 20, 50, 100, 200, 500, 1000]  # 50% .. 0.1%
NB = len(MAX_BUCKETS)
UNASSIGNED = 255


def fmt(x: float) -> str:
    return f"{x:.8g}"


def assign_buckets(ids: list[int]) -> dict[int, int]:
    """Replicate vsb build_buckets: ids iterated ascending; per-slot running
    counter; first slot whose threshold is reached claims an unassigned id."""
    counts = [0] * NB
    bucket = {}
    for i in sorted(ids):
        b = UNASSIGNED
        for idx in range(NB):
            counts[idx] += 1
            if b == UNASSIGNED and counts[idx] >= MAX_BUCKETS[idx]:
                b = idx
                counts[idx] -= MAX_BUCKETS[idx]
        bucket[i] = b
    return bucket


def main() -> None:
    src = Path(sys.argv[1]).expanduser()
    dst = Path(sys.argv[2]).expanduser()
    (dst / "bucket").mkdir(parents=True, exist_ok=True)

    train = pq.read_table(src / "shuffle_train.parquet", columns=["id", "emb"])
    train_ids = train["id"].to_pylist()
    bucket = assign_buckets(train_ids)

    sizes = [0] * NB
    for b in bucket.values():
        if b != UNASSIGNED:
            sizes[b] += 1
    print("bucket sizes (train vectors):",
          {f"{i}({MAX_BUCKETS[i]})": sizes[i] for i in range(NB)},
          "unassigned:", sum(1 for b in bucket.values() if b == UNASSIGNED))

    with open(dst / "dataset_buckets.txt", "w") as f:
        for id_, emb in zip(train_ids, train["emb"].to_pylist()):
            f.write(f"{id_}, {bucket[id_]}, [{', '.join(fmt(x) for x in emb)}]\n")
    print(f"dataset_buckets: {train.num_rows} lines")

    test = pq.read_table(src / "test.parquet", columns=["id", "emb"])
    neigh = pq.read_table(src / "neighbors.parquet", columns=["id", "neighbors_id"])
    nmap = dict(zip(neigh["id"].to_pylist(), neigh["neighbors_id"].to_pylist()))
    test_ids = test["id"].to_pylist()
    test_embs = test["emb"].to_pylist()

    for n in range(NB):
        kept = 0
        with open(dst / "bucket" / f"test_bucket{n}.txt", "w") as ftv, \
             open(dst / "bucket" / f"gt_bucket{n}.txt", "w") as fgt:
            for tid, emb in zip(test_ids, test_embs):
                gt_n = [nid for nid in nmap[tid] if bucket.get(nid) == n]
                if not gt_n:
                    continue
                ftv.write(", ".join(fmt(x) for x in emb) + "\n")
                fgt.write(", ".join(str(i) for i in gt_n) + "\n")
                kept += 1
        print(f"bucket {n}: {kept} queries with non-empty GT")


if __name__ == "__main__":
    main()
