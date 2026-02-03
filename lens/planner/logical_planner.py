
from ..compiler.ast_nodes import Query
from ..semantics.registry import MetricRegistry, DimensionRegistry
from ..time_intelligence.calendar_logic import FiscalCalendar
from ..time_intelligence.date_parser import DateParser
from .plan_nodes import LogicalNode, Scan, Filter, Aggregate

class LogicalPlanner:
    def __init__(self, metrics: MetricRegistry, dimensions: DimensionRegistry, 
                 calendar: FiscalCalendar):
        self.metrics = metrics
        self.dimensions = dimensions
        self.date_parser = DateParser(calendar)
        self.default_table = "sales_data" # Placeholder for MVP

    def plan(self, query: Query) -> LogicalNode:
        # 1. Source (Scan)
        # For now, we assume all metrics/dimensions come from one table.
        # In a real system, we'd look up the table from the Metric definition.
        
        # For MVP, resolving to SQL expressions directly in Agg/Group is fine.
        
        scan_node = Scan(table_name=self.default_table, columns=["*"]) 
        current_node = scan_node

        # 2. Filter (Time)
        if query.time_filter:
            date_range = self.date_parser.parse_time_filter(query.time_filter)
            if date_range:
                start, end = date_range
                # Assuming a standard 'date_column' for the MVP table
                condition = f"order_date >= '{start}' AND order_date <= '{end}'"
                current_node = Filter(child=current_node, condition=condition)
        
        # 3. Aggregate
        metric_def = self.metrics.get(query.metric)
        dim_defs = [self.dimensions.get(d) for d in query.dimensions]
        
        # Construct SQL expressions
        group_exprs = [d.sql_expression for d in dim_defs if d]
        metric_expr = f"{metric_def.sql_expression} as {query.metric}" if metric_def else query.metric
        
        current_node = Aggregate(
            child=current_node,
            group_by=group_exprs,
            metrics=[metric_expr]
        )

        # 4. Filter (Comparison) - Not implemented in this step, but placeholder
        # Comparisons usually require a Join or separate CTEs. 
        # For Phase 4 MVP, we'll just return the base plan.

        return current_node
