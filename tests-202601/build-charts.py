#!/usr/bin/env python3

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

def subplots():
    fig, ax = plt.subplots(2, 1, gridspec_kw={"hspace": 0}, figsize=[9.6, 4.3], layout="tight")
    return fig, ax

def savefig(path, xmin=1, xmax=1152, legend="top", xlabel="Delay [us]", transparent=True):
    ax[0].set_ylabel("QPS [count/s]")
    if legend=="top":
        ax[0].legend()
    ax[0].minorticks_on()
    ax[0].grid()
    ax[0].grid(which="minor", alpha=0.2)

    ax[1].set_ylabel("P99 Latency [ms]")
    if legend=="bottom":
        ax[1].legend()
    ax[1].minorticks_on()
    ax[1].grid()
    ax[1].grid(which="minor", alpha=0.2)

    xticks = ax[1].get_xticks()
    ax[0].set_xticks(xticks, labels=[])

    ax[0].set_xlim(xmin, xmax)
    ax[1].set_xlim(xmin, xmax)

    plt.xlabel(xlabel)

    plt.savefig(path, transparent=transparent)
    #plt.close()

scylla_1b_1_10 = pd.read_csv("data/yandex-deep-1b-20260121-m32-10-scylla.csv")
scylla_1b_1_100 = pd.read_csv("data/yandex-deep-1b-20260121-m32-100-scylla.csv")

fig, ax = subplots()
ax[0].plot(scylla_1b_1_10["Concurrency"], scylla_1b_1_10["QPS"], label="k=10 recall~=97.0%")
ax[1].plot(scylla_1b_1_10["Concurrency"], scylla_1b_1_10["P99"], label="k=10 recall~=97.0%")
ax[0].plot(scylla_1b_1_100["Concurrency"], scylla_1b_1_100["QPS"], label="k=100 recall~=92.6%")
ax[1].plot(scylla_1b_1_100["Concurrency"], scylla_1b_1_100["P99"], label="k=100 recall~=92.6%")
savefig("scylla-1b-20260121-0.png", xlabel="Concurrency with index = {N=1B m=32 ef-*=256}", xmax=512, transparent=False)

vs_1b_1_10 = pd.read_csv("data/yandex-deep-1b-20260121T110333-10-vs.csv")
vs_1b_1_100 = pd.read_csv("data/yandex-deep-1b-20260121T110333-100-vs.csv")

fig, ax = subplots()
ax[0].plot(vs_1b_1_10["Concurrency"], vs_1b_1_10["QPS"], label="k=10")
ax[1].plot(vs_1b_1_10["Concurrency"], vs_1b_1_10["P99"], label="k=10")
ax[0].plot(vs_1b_1_100["Concurrency"], vs_1b_1_100["QPS"], label="k=100")
ax[1].plot(vs_1b_1_100["Concurrency"], vs_1b_1_100["P99"], label="k=100")
savefig("vs-1b-20260121-0.png", xlabel="Concurrency with index = {N=1B m=32 ef-*=256}", xmax=512, transparent=False)

scylla_1b_2_10 = pd.read_csv("data/yandex-deep-1b-20260121T210052-10-scylla.csv")
scylla_1b_2_100 = pd.read_csv("data/yandex-deep-1b-20260121T210052-100-scylla.csv")

fig, ax = subplots()
ax[0].plot(scylla_1b_2_10["Concurrency"], scylla_1b_2_10["QPS"], label="k=10 recall~=91.7%")
ax[1].plot(scylla_1b_2_10["Concurrency"], scylla_1b_2_10["P99"], label="k=10 recall~=91.7%")
ax[0].plot(scylla_1b_2_100["Concurrency"], scylla_1b_2_100["QPS"], label="k=100 recall~=82.6%")
ax[1].plot(scylla_1b_2_100["Concurrency"], scylla_1b_2_100["P99"], label="k=100 recall~=82.6%")
savefig("scylla-1b-20260121-1.png", xlabel="Concurrency with index = {N=1B m=32 ef-*=128}", xmax=512, transparent=False)

vs_1b_2_10 = pd.read_csv("data/yandex-deep-1b-20260121T210052-10-vs.csv")
vs_1b_2_100 = pd.read_csv("data/yandex-deep-1b-20260121T210052-100-vs.csv")

fig, ax = subplots()
ax[0].plot(vs_1b_2_10["Concurrency"], vs_1b_2_10["QPS"], label="k=10")
ax[1].plot(vs_1b_2_10["Concurrency"], vs_1b_2_10["P99"], label="k=10")
ax[0].plot(vs_1b_2_100["Concurrency"], vs_1b_2_100["QPS"], label="k=100")
ax[1].plot(vs_1b_2_100["Concurrency"], vs_1b_2_100["P99"], label="k=100")
savefig("vs-1b-20260121-1.png", xlabel="Concurrency with index = {N=1B m=32 ef-*=128}", xmax=512, transparent=False)

scylla_1b_3_10 = pd.read_csv("data/yandex-deep-1b-20260122T230313-10-scylla.csv")
scylla_1b_3_100 = pd.read_csv("data/yandex-deep-1b-20260122T230313-100-scylla.csv")

fig, ax = subplots()
ax[0].plot(scylla_1b_3_10["Concurrency"], scylla_1b_3_10["QPS"], label="k=10 recall~=95.8%")
ax[1].plot(scylla_1b_3_10["Concurrency"], scylla_1b_3_10["P99"], label="k=10 recall~=95.8%")
ax[0].plot(scylla_1b_3_100["Concurrency"], scylla_1b_3_100["QPS"], label="k=100 recall~=89.3%")
ax[1].plot(scylla_1b_3_100["Concurrency"], scylla_1b_3_100["P99"], label="k=100 recall~=89.3%")
savefig("scylla-1b-20260122.png", xlabel="Concurrency with index = {N=1B m=64 ef-construction=256 ef-search=128}", xmax=512, transparent=False)

vs_1b_3_10 = pd.read_csv("data/yandex-deep-1b-20260122T230313-10-vs.csv")
vs_1b_3_100 = pd.read_csv("data/yandex-deep-1b-20260122T230313-100-vs.csv")

fig, ax = subplots()
ax[0].plot(vs_1b_3_10["Concurrency"], vs_1b_3_10["QPS"], label="k=10")
ax[1].plot(vs_1b_3_10["Concurrency"], vs_1b_3_10["P99"], label="k=10")
ax[0].plot(vs_1b_3_100["Concurrency"], vs_1b_3_100["QPS"], label="k=100")
ax[1].plot(vs_1b_3_100["Concurrency"], vs_1b_3_100["P99"], label="k=100")
savefig("vs-1b-20260122.png", xlabel="Concurrency with index = {N=1B m=64 ef-construction=256 ef-search=128}", xmax=512, transparent=False)
