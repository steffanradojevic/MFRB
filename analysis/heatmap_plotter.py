"""
Python 3.12.2
Leiden University
Author: Steffan Radojevic
Email: steffanradojevic@gmail.com
Date: 4 September 2025
Description: Python script to use the results from the multi-striding experiments for the Raspberry Pi 5 and the Banana Pi BPI-F3.
These results are presented as heatmaps: take the best performing array for each striding configuration and plot it in the heatmap.
x-axis = stride unroll, y-axis is portion unroll. Color indicates magnitude of throughput.
"""

import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd

csv_file = r"results\vector_ST1_writeKernel_SP20x32_R5x5_23529411.csv"

# Read CSV and convert throughput from B/s to GB/s
df = pd.read_csv(csv_file)
df["throughput"] = df["throughput"] / 1e9


df = df.groupby(["portion", "stride"], as_index=False)["throughput"]
df_max = df.max()


df_min = df.min()
df_diff = pd.DataFrame(columns=["stride", "portion", "throughput"])
for x in range(df_max.shape[0]):
    new_throughput = float(df_max.iloc[x]["throughput"]) - float(
        df_min.iloc[x]["throughput"]
    )
    df_diff = pd.concat(
        [
            df_diff,
            pd.DataFrame(
                [
                    {
                        "stride": int(df_max.iloc[x]["stride"]),
                        "portion": int(df_max.iloc[x]["portion"]),
                        "throughput": new_throughput,
                    }
                ]
            ),
        ],
        ignore_index=True,
    )


# This plot the maximum throughput over all arrays
# Difference in best and worst performing array, use df_diff
pivot = df_max.pivot(index="portion", columns="stride", values="throughput")

# Plot heatmap
ax = sns.heatmap(
    pivot,
    cmap="rocket",
    annot=True,
    fmt=".3f",
)

# Show all y-ticks (portion unrolls)
ax.set_yticks(range(len(pivot.index)))
ax.set_yticklabels(pivot.index)

# Add label to colorbar
colorbar = ax.collections[0].colorbar
colorbar.set_label("Throughput GB/s")

# x-axis, y-axis label and Title
plt.xlabel("stride")
plt.ylabel("portion")
plt.title(
    "ARM writeKernel Vector ST1",
    fontsize=14,
    pad=10,
)

plt.gca().invert_yaxis()  # Invert Y-axis
plt.show()
