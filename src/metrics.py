from src.models import Task, Node


def calculate_local_latency(task: Task, local_node: Node) -> float:
    """
    Calculate latency when the task is executed on the local device.

    Formula:
        latency = cpu_cycles / cpu_power
    """
    latency_sec = task.cpu_cycles / local_node.cpu_power
    return latency_sec * 1000


def calculate_offloading_latency(task: Task, node: Node) -> float:
    """
    Calculate latency when the task is offloaded to edge or cloud.

    Formula:
        total latency = upload time + network delay + processing time + download time
    """
    if node.upload_bandwidth <= 0 or node.download_bandwidth <= 0:
        raise ValueError(f"{node.name} node must have positive bandwidth for offloading.")

    upload_time_ms = (task.data_size_mb / node.upload_bandwidth) * 1000
    processing_time_ms = (task.cpu_cycles / node.cpu_power) * 1000
    download_time_ms = (task.result_size_mb / node.download_bandwidth) * 1000

    total_latency_ms = (
        upload_time_ms
        + node.network_delay_ms
        + processing_time_ms
        + download_time_ms
    )

    return total_latency_ms


def calculate_latency(task: Task, node: Node) -> float:
    """
    Calculate latency based on selected node.
    """
    if node.name == "local":
        return calculate_local_latency(task, node)

    return calculate_offloading_latency(task, node)


def calculate_cost(task: Task, node: Node) -> float:
    """
    Calculate transmission cost.

    Local execution has no transmission cost.
    """
    if node.name == "local":
        return 0.0

    total_data_mb = task.data_size_mb + task.result_size_mb
    return total_data_mb * node.cost_per_mb


def calculate_energy(task: Task, node: Node) -> float:
    """
    Calculate energy consumption based on CPU cycles.
    """
    return task.cpu_cycles * node.energy_per_cycle


def is_deadline_missed(task: Task, latency_ms: float) -> bool:
    """
    Check whether the task missed its deadline.
    """
    return latency_ms > task.deadline_ms