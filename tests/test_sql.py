import sys
import os

# Add project root to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from lens.planner.plan_nodes import Scan, Filter, Aggregate
from lens.sql_gen.duckdb_generator import DuckDBGenerator

def test_sql_generation():
    # Construct a plan manually (mimicking Planner output)
    # Plan: Aggregate(Filter(Scan(sales), date cond), group by region, sum sales)
    
    scan = Scan(table_name="sales_data", columns=["*"])
    filt = Filter(child=scan, condition="order_date >= '2025-01-01' AND order_date <= '2025-12-31'")
    agg = Aggregate(child=filt, group_by=["region_name"], metrics=["SUM(sales) as net_sales"])
    
    generator = DuckDBGenerator()
    sql = generator.generate(agg)
    
    print("Generated SQL:")
    print(sql)
    
    # Assertions
    # Basic check for structure
    assert "SELECT region_name, SUM(sales) as net_sales" in sql
    assert "FROM" in sql
    assert "sales_data" in sql
    assert "WHERE order_date >=" in sql
    assert "GROUP BY region_name" in sql
    
    print("Test SQL Generation Passed!")

if __name__ == "__main__":
    test_sql_generation()
