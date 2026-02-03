from dataclasses import dataclass
from typing import List

@dataclass
class LogicalNode:
    pass

@dataclass
class Scan(LogicalNode):
    table_name: str
    columns: List[str]

@dataclass
class Filter(LogicalNode):
    child: LogicalNode
    condition: str  # SQL-like condition for now, e.g., "date >= '2025-01-01'"

@dataclass
class Aggregate(LogicalNode):
    child: LogicalNode
    group_by: List[str]
    metrics: List[str]  # e.g., ["SUM(sales) as net_sales"]

@dataclass
class Project(LogicalNode):
    child: LogicalNode
    columns: List[str]
