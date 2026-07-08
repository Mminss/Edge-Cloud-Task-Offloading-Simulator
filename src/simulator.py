import pandas as pd
import yaml

from src.models import Task, Node, SimulationResult
from src.metrics import (
    calculate_latency,
    calculate_cost,
    calculate_energy,
    is_deadline_missed,
)


def load_tasks(csv_path: str) -> list[Task]:
    df = pd.read_csv(csv_path)

    tasks = []

    for _, row in df.iterrows():
        task = Task(
            task_id=int(row["task_id"]),
            data_size_mb=float(row["data_size_mb"]),
            cpu_cycles=float(row["cpu_cycles"]),
            deadline_ms=float(row["deadline_ms"]),
            result_size_mb=float(row["result_size_mb"]),
            priority=int(row["priority"]),
        )
        tasks.append(task)

    return tasks


def load_nodes(config_path: str) -> dict[str, Node]:
    with open(config_path, "r", encoding="utf-8") as file:
        config = yaml.safe_load(file)

    nodes = {}

    for node_name, node_config in config["nodes"].items():
        node = Node(
            name=node_name,
            cpu_power=float(node_config["cpu_power"]),
            upload_bandwidth=float(node_config["upload_bandwidth"]),
            download_bandwidth=float(node_config["download_bandwidth"]),
            network_delay_ms=float(node_config["network_delay_ms"]),
            cost_per_mb=float(node_config["cost_per_mb"]),
            energy_per_cycle=float(node_config["energy_per_cycle"]),
        )
        nodes[node_name] = node

    return nodes


def run_algorithm(
    tasks: list[Task],
    nodes: dict[str, Node],
    algorithm_func,
) -> list[SimulationResult]:
    results = []

    local_node = nodes["local"]
    edge_node = nodes["edge"]
    cloud_node = nodes["cloud"]

    for task in tasks:
        selected_node_name = algorithm_func(
            task,
            local_node,
            edge_node,
            cloud_node,
        )

        selected_node = nodes[selected_node_name]

        latency = calculate_latency(task, selected_node)
        cost = calculate_cost(task, selected_node)
        energy = calculate_energy(task, selected_node)
        deadline_missed = is_deadline_missed(task, latency)

        result = SimulationResult(
            task_id=task.task_id,
            selected_node=selected_node_name,
            latency_ms=latency,
            cost=cost,
            energy=energy,
            deadline_missed=deadline_missed,
        )

        results.append(result)

    return results