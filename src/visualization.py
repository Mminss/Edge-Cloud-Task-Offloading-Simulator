import matplotlib.pyplot as plt
import pandas as pd


def plot_summary(csv_path: str = "results/summary.csv", save_path: str = "results/comparison.png"):
    """
    Load results/summary.csv and plot a 2x2 bar chart comparing
    latency, cost, energy, and deadline miss rate across algorithms.
    """
    df = pd.read_csv(csv_path)

    fig, axes = plt.subplots(2, 2, figsize=(12, 8))

    metrics = [
        ("average_latency_ms", "Average Latency (ms)", axes[0, 0]),
        ("average_cost", "Average Cost", axes[0, 1]),
        ("average_energy", "Average Energy", axes[1, 0]),
        ("deadline_miss_rate_percent", "Deadline Miss Rate (%)", axes[1, 1]),
    ]

    colors = plt.cm.Set2.colors

    for column, title, ax in metrics:
        ax.bar(df["algorithm"], df[column], color=colors[: len(df)])
        ax.set_title(title)
        ax.set_ylabel(title)
        ax.tick_params(axis="x", rotation=30)

    fig.suptitle("Offloading Algorithm Comparison", fontsize=14)
    fig.tight_layout()
    fig.savefig(save_path, dpi=150)
    print(f"Saved plot to {save_path}")

    return fig


if __name__ == "__main__":
    plot_summary()