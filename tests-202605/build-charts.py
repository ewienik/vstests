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

scylla_1b_1_10 = pd.read_csv("data/yandex-deep-1b-20260512T104613-10-scylla.csv")
scylla_1b_1_30 = pd.read_csv("data/yandex-deep-1b-20260512T104613-30-scylla.csv")
scylla_1b_1_100 = pd.read_csv("data/yandex-deep-1b-20260512T104613-100-scylla.csv")

fig, ax = subplots()
ax[0].plot(scylla_1b_1_10["Concurrency"], scylla_1b_1_10["QPS"], label="k=10 recall~=89.0%")
ax[1].plot(scylla_1b_1_10["Concurrency"], scylla_1b_1_10["P99"], label="k=10 recall~=89.0%")
ax[0].plot(scylla_1b_1_30["Concurrency"], scylla_1b_1_30["QPS"], label="k=30 recall~=90.0%")
ax[1].plot(scylla_1b_1_30["Concurrency"], scylla_1b_1_30["P99"], label="k=30 recall~=90.0%")
ax[0].plot(scylla_1b_1_100["Concurrency"], scylla_1b_1_100["QPS"], label="k=100 recall~=90.7%")
ax[1].plot(scylla_1b_1_100["Concurrency"], scylla_1b_1_100["P99"], label="k=100 recall~=90.7%")
savefig("scylla-1b-202605-0.png", xlabel="Concurrency with index = {N=1B m=64 ef-*=512 quantization=i8 oversampling=1.0 rescoring=false}", xmax=512, transparent=False)

scylla_1b_2_10 = pd.read_csv("data/yandex-deep-1b-20260512T124447-10-scylla.csv")
scylla_1b_2_100 = pd.read_csv("data/yandex-deep-1b-20260512T124447-100-scylla.csv")

fig, ax = subplots()
ax[0].plot(scylla_1b_2_10["Concurrency"], scylla_1b_2_10["QPS"], label="k=10 recall~=89.0%")
ax[1].plot(scylla_1b_2_10["Concurrency"], scylla_1b_2_10["P99"], label="k=10 recall~=89.0%")
ax[0].plot(scylla_1b_2_100["Concurrency"], scylla_1b_2_100["QPS"], label="k=100 recall~=90.7%")
ax[1].plot(scylla_1b_2_100["Concurrency"], scylla_1b_2_100["P99"], label="k=100 recall~=90.7%")
savefig("scylla-1b-202605-1.png", xlabel="Concurrency with index = {N=1B m=64 ef-*=512 quantization=i8 oversampling=1.5 rescoring=false}", xmax=512, transparent=False)

scylla_1b_3_10 = pd.read_csv("data/yandex-deep-1b-20260512T132329-10-scylla.csv")
scylla_1b_3_100 = pd.read_csv("data/yandex-deep-1b-20260512T132329-100-scylla.csv")

fig, ax = subplots()
ax[0].plot(scylla_1b_3_10["Concurrency"], scylla_1b_3_10["QPS"], label="k=10 recall~=97.9%")
ax[1].plot(scylla_1b_3_10["Concurrency"], scylla_1b_3_10["P99"], label="k=10 recall~=97.9%")
ax[0].plot(scylla_1b_3_100["Concurrency"], scylla_1b_3_100["QPS"], label="k=100 recall~=98.1%")
ax[1].plot(scylla_1b_3_100["Concurrency"], scylla_1b_3_100["P99"], label="k=100 recall~=98.1%")
savefig("scylla-1b-202605-2.png", xlabel="Concurrency with index = {N=1B m=64 ef-*=512 quantization=i8 oversampling=1.5 rescoring=true}", xmax=512, transparent=False)

scylla_1b_4_10 = pd.read_csv("data/yandex-deep-1b-20260513T162016-10-scylla.csv")
scylla_1b_4_100 = pd.read_csv("data/yandex-deep-1b-20260513T162016-100-scylla.csv")

fig, ax = subplots()
ax[0].plot(scylla_1b_4_10["Concurrency"], scylla_1b_4_10["QPS"], label="k=10 recall~=99.3%")
ax[1].plot(scylla_1b_4_10["Concurrency"], scylla_1b_4_10["P99"], label="k=10 recall~=99.3%")
ax[0].plot(scylla_1b_4_100["Concurrency"], scylla_1b_4_100["QPS"], label="k=100 recall~=98.5%")
ax[1].plot(scylla_1b_4_100["Concurrency"], scylla_1b_4_100["P99"], label="k=100 recall~=98.5%")
savefig("scylla-1b-202605-3.png", xlabel="Concurrency with index = {N=1B m=64 ef-*=512 quantization=f32 oversampling=1.0 rescoring=false}", xmax=512, transparent=False)

vs_1b_4_10 = pd.read_csv("data/yandex-deep-1b-20260513T162016-10-vs.csv")
vs_1b_4_100 = pd.read_csv("data/yandex-deep-1b-20260513T162016-100-vs.csv")

fig, ax = subplots()
ax[0].plot(vs_1b_4_10["Concurrency"], vs_1b_4_10["QPS"], label="k=10")
ax[1].plot(vs_1b_4_10["Concurrency"], vs_1b_4_10["P99"], label="k=10")
ax[0].plot(vs_1b_4_100["Concurrency"], vs_1b_4_100["QPS"], label="k=100")
ax[1].plot(vs_1b_4_100["Concurrency"], vs_1b_4_100["P99"], label="k=100")
savefig("vs-1b-202605-3.png", xlabel="(search-http) Concurrency with index = {N=1B m=64 ef-*=512 quantization=f32}", xmax=512, transparent=False)

scylla_1b_5_10 = pd.read_csv("data/yandex-deep-1b-20260514T091010-10-scylla.csv")
scylla_1b_5_100 = pd.read_csv("data/yandex-deep-1b-20260514T091010-100-scylla.csv")

fig, ax = subplots()
ax[0].plot(scylla_1b_5_10["Concurrency"], scylla_1b_5_10["QPS"], label="k=10 recall~=99.3%")
ax[1].plot(scylla_1b_5_10["Concurrency"], scylla_1b_5_10["P99"], label="k=10 recall~=99.3%")
ax[0].plot(scylla_1b_5_100["Concurrency"], scylla_1b_5_100["QPS"], label="k=100 recall~=98.5%")
ax[1].plot(scylla_1b_5_100["Concurrency"], scylla_1b_5_100["P99"], label="k=100 recall~=98.5%")
savefig("scylla-1b-202605-4.png", xlabel="Concurrency with index = {N=1B m=64 ef-*=512 quantization=f32 oversampling=1.0 rescoring=false}", xmax=1152, transparent=False)

vs_1b_5_10 = pd.read_csv("data/yandex-deep-1b-20260514T091010-10-vs.csv")
vs_1b_5_100 = pd.read_csv("data/yandex-deep-1b-20260514T091010-100-vs.csv")

fig, ax = subplots()
ax[0].plot(vs_1b_5_10["Concurrency"], vs_1b_5_10["QPS"], label="k=10")
ax[1].plot(vs_1b_5_10["Concurrency"], vs_1b_5_10["P99"], label="k=10")
ax[0].plot(vs_1b_5_100["Concurrency"], vs_1b_5_100["QPS"], label="k=100")
ax[1].plot(vs_1b_5_100["Concurrency"], vs_1b_5_100["P99"], label="k=100")
savefig("vs-1b-202605-4.png", xlabel="(search-http) Concurrency with index = {N=1B m=64 ef-*=512 quantization=f32}", xmax=1152, transparent=False)
