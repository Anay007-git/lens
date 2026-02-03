from ..planner.plan_nodes import LogicalNode, Scan, Filter, Aggregate

class DuckDBGenerator:
    def generate(self, plan: LogicalNode) -> str:
        return self._visit(plan)

    def _visit(self, node: LogicalNode) -> str:
        if isinstance(node, Aggregate):
            return self._visit_aggregate(node)
        elif isinstance(node, Filter):
            return self._visit_filter(node)
        elif isinstance(node, Scan):
            return self._visit_scan(node)
        # Project not implemented in MVP logic yet, but pattern is similar
        raise NotImplementedError(f"Node type {type(node)} not supported in SQL generation")

    def _visit_scan(self, node: Scan) -> str:
        return f"SELECT * FROM {node.table_name}"

    def _visit_filter(self, node: Filter) -> str:
        # Filter usually wraps a Scan or another subquery.
        # In SQL, this is WHERE.
        # Structure: SELECT * FROM (child_query) WHERE condition
        # Optimization: If child is Scan, we can merge, but for now let's wrap strictly for correctness.
        child_sql = self._visit(node.child)
        return f"SELECT * FROM ({child_sql}) AS sub WHERE {node.condition}"

    def _visit_aggregate(self, node: Aggregate) -> str:
        # AGG wraps child.
        # SELECT dims, metrics FROM (child) GROUP BY dims
        child_sql = self._visit(node.child)
        
        dims = ", ".join(node.group_by)
        metrics = ", ".join(node.metrics)
        select_clause = f"{dims}, {metrics}" if dims else metrics
        group_by_clause = f" GROUP BY {dims}" if dims else ""
        
        return f"SELECT {select_clause} FROM ({child_sql}) AS agg_sub{group_by_clause}"
