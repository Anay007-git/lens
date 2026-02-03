import sys
import os
from datetime import date

# Add project root to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from lens.compiler.ast_nodes import Query
from lens.semantics.registry import MetricRegistry, DimensionRegistry, Metric, Dimension
from lens.time_intelligence.calendar_logic import FiscalCalendar
from lens.planner.logical_planner import LogicalPlanner
from lens.planner.plan_nodes import Scan, Filter, Aggregate

def test_planner():
    # Setup Registry
    metrics = MetricRegistry()
    metrics.add(Metric(name="net_sales", sql_expression="SUM(sales)"))
    
    dims = DimensionRegistry()
    dims.add(Dimension(name="region", sql_expression="region_name"))
    
    cal = FiscalCalendar(start_month=1)
    planner = LogicalPlanner(metrics, dims, cal)

    # Test Query: show net_sales by region for FY2025
    query = Query(metric="net_sales", dimensions=["region"], time_filter="FY2025")
    
    plan = planner.plan(query)
    print("Plan:", plan)
    
    # Assertions
    assert isinstance(plan, Aggregate)
    assert plan.metrics == ["SUM(sales) as net_sales"]
    assert plan.group_by == ["region_name"]
    
    filter_node = plan.child
    assert isinstance(filter_node, Filter)
    # FY2025 (Jan start) -> 2025-01-01 to 2025-12-31
    assert "order_date >= '2025-01-01'" in filter_node.condition
    assert "order_date <= '2025-12-31'" in filter_node.condition
    
    scan_node = filter_node.child
    assert isinstance(scan_node, Scan)
    assert scan_node.table_name == "sales_data"
    
    print("Test Planner Passed!")

if __name__ == "__main__":
    test_planner()
