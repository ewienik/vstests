#!/usr/bin/env python3
"""Convert VectorDBBench parquet (openai_small_50k) into the text format
expected by SCT's latte workload vector_search_recall.rn.

Produces the three files with the exact names the script hardcodes:
  vs_sanity_dataset_50k_1536dim.txt      lines: "id, [v1, v2, ...]"
  vs_sanity_test_vectors_1k_1536dim.txt  lines: "v1, v2, ..."
  vs_sanity_ground_truth_1k_1536dim.txt  lines: "id1, id2, ..."
Line i of test vectors corresponds to line i of ground truth (aligned by id).

Usage:
  uv run --with pyarrow parquet_to_sct_text.py ~/datasets/openai_small_50k ~/datasets/sct-vector-text
"""

import sys
from pathlib import Path

import pyarrow.parquet as pq


def fmt(x: float) -> str:
    return f"{x:.8g}"


def main() -> None:
    src = Path(sys.argv[1]).expanduser()
    dst = Path(sys.argv[2]).expanduser()
    dst.mkdir(parents=True, exist_ok=True)

    train = pq.read_table(src / "shuffle_train.parquet", columns=["id", "emb"])
    with open(dst / "vs_sanity_dataset_50k_1536dim.txt", "w") as f:
        for id_, emb in zip(train["id"].to_pylist(), train["emb"].to_pylist()):
            f.write(f"{id_}, [{', '.join(fmt(x) for x in emb)}]\n")
    print(f"dataset: {train.num_rows} lines")

    test = pq.read_table(src / "test.parquet", columns=["id", "emb"])
    neigh = pq.read_table(src / "neighbors.parquet", columns=["id", "neighbors_id"])
    nmap = dict(zip(neigh["id"].to_pylist(), neigh["neighbors_id"].to_pylist()))

    test_ids = test["id"].to_pylist()
    with open(dst / "vs_sanity_test_vectors_1k_1536dim.txt", "w") as f:
        for emb in test["emb"].to_pylist():
            f.write(", ".join(fmt(x) for x in emb) + "\n")
    with open(dst / "vs_sanity_ground_truth_1k_1536dim.txt", "w") as f:
        for tid in test_ids:
            f.write(", ".join(str(i) for i in nmap[tid]) + "\n")
    print(f"test vectors + ground truth: {len(test_ids)} lines")


if __name__ == "__main__":
    main()
