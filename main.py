import os
import pandas as pd

from src.visualization import plot_summary

from src.simulator import load_tasks, load_nodes, run_algorithm
from src.algorithms import (
    local_only,
    edge_only,
    cloud_only,
    latency_greedy,
    deadline_cost_minimization,
)


def summarize_results(results):
    avg_latency = sum(result.latency_ms for result in results) / len(results)
    avg_cost = sum(result.cost for result in results) / len(results)
    avg_energy = sum(result.energy for result in results) / len(results)

    deadline_miss_rate = (
        sum(result.deadline_missed for result in results) / len(results)
    ) * 100

    return avg_latency, avg_cost, avg_energy, deadline_miss_rate


def main():
    tasks = load_tasks("data/sample_tasks.csv")
    nodes = load_nodes("config.yaml")

    algorithms = {
        "Local Only": local_only,
        "Edge Only": edge_only,
        "Cloud Only": cloud_only,
        "Latency Greedy": latency_greedy,
        "Deadline Cost Minimization": deadline_cost_minimization,
    }

    print(f"Loaded {len(tasks)} tasks")
    print(f"Loaded nodes: {list(nodes.keys())}")
    print("=" * 60)

    summary_rows = []

    for algorithm_name, algorithm_func in algorithms.items():
        results = run_algorithm(tasks, nodes, algorithm_func)

        avg_latency, avg_cost, avg_energy, deadline_miss_rate = summarize_results(
            results
        )

        summary_rows.append(
            {
                "algorithm": algorithm_name,
                "average_latency_ms": avg_latency,
                "average_cost": avg_cost,
                "average_energy": avg_energy,
                "deadline_miss_rate_percent": deadline_miss_rate,
            }
        )

        print(f"Algorithm: {algorithm_name}")
        print(f"Average latency: {avg_latency:.2f} ms")
        print(f"Average cost: {avg_cost:.4f}")
        print(f"Average energy: {avg_energy:.4f}")
        print(f"Deadline miss rate: {deadline_miss_rate:.2f}%")
        print("-" * 60)

    os.makedirs("results", exist_ok=True)

    summary_df = pd.DataFrame(summary_rows)
    summary_df.to_csv("results/summary.csv", index=False)

    print("Saved summary to results/summary.csv")

    plot_summary()


if __name__ == "__main__":
    main()