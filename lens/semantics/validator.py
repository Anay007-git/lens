from typing import List
from ..compiler.ast_nodes import Query
from .registry import MetricRegistry, DimensionRegistry

class SemanticError(Exception):
    pass

class SemanticValidator:
    def __init__(self, metric_registry: MetricRegistry, dimension_registry: DimensionRegistry):
        self.metric_registry = metric_registry
        self.dimension_registry = dimension_registry

    def validate(self, query: Query):
        errors = []

        # Validate Metric
        if not self.metric_registry.contains(query.metric):
            errors.append(f"Unknown metric: '{query.metric}'")

        # Validate Dimensions
        for dim in query.dimensions:
            if not self.dimension_registry.contains(dim):
                errors.append(f"Unknown dimension: '{dim}'")

        if errors:
            raise SemanticError("\n".join(errors))
        
        return True
