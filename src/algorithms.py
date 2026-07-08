from src.models import Task, Node
from src.metrics import calculate_latency, calculate_cost


def local_only(task: Task, local_node: Node, edge_node: Node, cloud_node: Node) -> str:
    return "local"


def edge_only(task: Task, local_node: Node, edge_node: Node, cloud_node: Node) -> str:
    return "edge"


def cloud_only(task: Task, local_node: Node, edge_node: Node, cloud_node: Node) -> str:
    return "cloud"


def latency_greedy(task: Task, local_node: Node, edge_node: Node, cloud_node: Node) -> str:
    nodes = {
        "local": local_node,
        "edge": edge_node,
        "cloud": cloud_node,
    }

    latencies = {
        name: calculate_latency(task, node)
        for name, node in nodes.items()
    }

    return min(latencies, key=latencies.get)


def deadline_cost_minimization(
    task: Task,
    local_node: Node,
    edge_node: Node,
    cloud_node: Node,
) -> str:
    nodes = {
        "local": local_node,
        "edge": edge_node,
        "cloud": cloud_node,
    }

    valid_candidates = {}

    for name, node in nodes.items():
        latency = calculate_latency(task, node)

        if latency <= task.deadline_ms:
            cost = calculate_cost(task, node)
            valid_candidates[name] = cost

    if valid_candidates:
        return min(valid_candidates, key=valid_candidates.get)

    latencies = {
        name: calculate_latency(task, node)
        for name, node in nodes.items()
    }

    return min(latencies, key=latencies.get)
