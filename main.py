from src.models import Task, Node
from src.metrics import (
    calculate_latency,
    calculate_cost,
    calculate_energy,
    is_deadline_missed,
)


def main():
    task = Task(
        task_id=1,
        data_size_mb=5,
        cpu_cycles=1000000000,
        deadline_ms=500,
        result_size_mb=0.5,
        priority=2,
    )

    local_node = Node(
        name="local",
        cpu_power=1000000000,
        upload_bandwidth=0,
        download_bandwidth=0,
        network_delay_ms=0,
        cost_per_mb=0,
        energy_per_cycle=0.000000001,
    )

    edge_node = Node(
        name="edge",
        cpu_power=5000000000,
        upload_bandwidth=50,
        download_bandwidth=100,
        network_delay_ms=20,
        cost_per_mb=0.001,
        energy_per_cycle=0.0000000004,
    )

    cloud_node = Node(
        name="cloud",
        cpu_power=15000000000,
        upload_bandwidth=20,
        download_bandwidth=50,
        network_delay_ms=100,
        cost_per_mb=0.003,
        energy_per_cycle=0.0000000002,
    )

    nodes = [local_node, edge_node, cloud_node]

    for node in nodes:
        latency = calculate_latency(task, node)
        cost = calculate_cost(task, node)
        energy = calculate_energy(task, node)
        deadline_missed = is_deadline_missed(task, latency)

        print(f"Node: {node.name}")
        print(f"Latency: {latency:.2f} ms")
        print(f"Cost: {cost:.4f}")
        print(f"Energy: {energy:.4f}")
        print(f"Deadline missed: {deadline_missed}")
        print("-" * 30)


if __name__ == "__main__":
    main()