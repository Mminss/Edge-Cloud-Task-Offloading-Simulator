from dataclasses import dataclass


@dataclass
class Task:
    task_id: int
    data_size_mb: float
    cpu_cycles: float
    deadline_ms: float
    result_size_mb: float
    priority: int


@dataclass
class Node:
    name: str
    cpu_power: float
    upload_bandwidth: float
    download_bandwidth: float
    network_delay_ms: float
    cost_per_mb: float
    energy_per_cycle: float


@dataclass
class SimulationResult:
    task_id: int
    selected_node: str
    latency_ms: float
    cost: float
    energy: float
    deadline_missed: bool