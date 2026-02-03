from dataclasses import dataclass
from typing import List, Optional

@dataclass
class Node:
    pass

@dataclass
class Query(Node):
    metric: str
    dimensions: List[str]
    time_filter: Optional[str] = None
    comparison: Optional[str] = None

@dataclass
class ShowClause(Node):
    metric: str
    dimensions: List[str]
