from dataclasses import dataclass
from typing import Dict, Optional

@dataclass
class Metric:
    name: str
    sql_expression: str
    format: Optional[str] = None

@dataclass
class Dimension:
    name: str
    sql_expression: str

class MetricRegistry:
    def __init__(self):
        self._metrics: Dict[str, Metric] = {}

    def add(self, metric: Metric):
        self._metrics[metric.name] = metric

    def get(self, name: str) -> Optional[Metric]:
        return self._metrics.get(name)

    def contains(self, name: str) -> bool:
        return name in self._metrics

class DimensionRegistry:
    def __init__(self):
        self._dimensions: Dict[str, Dimension] = {}

    def add(self, dimension: Dimension):
        self._dimensions[dimension.name] = dimension

    def get(self, name: str) -> Optional[Dimension]:
        return self._dimensions.get(name)

    def contains(self, name: str) -> bool:
        return name in self._dimensions
