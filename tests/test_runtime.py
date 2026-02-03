import sys
import os
import pandas as pd

# Add project root to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Ensure dependencies
from importlib.util import find_spec
if find_spec("duckdb") is None or find_spec("pandas") is None:
    print("Installing runtime dependencies...")
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "duckdb", "pandas"])

from lens.runtime.runner import LensRunner

def test_runtime():
    runner = LensRunner()
    
    # 1. Setup Mock Data
    data = {
        'region_name': ['North', 'South', 'North', 'South'],
        'order_date': [
            pd.Timestamp('2025-01-15'), 
            pd.Timestamp('2025-02-20'), 
            pd.Timestamp('2024-12-01'), # Outside FY2025 range
            pd.Timestamp('2025-06-10')
        ],
        'sales': [100, 200, 50, 300]
    }
    df = pd.DataFrame(data)
    runner.register_dataframe("sales_data", df)
    
    # 2. Run Query
    # SQL generated from Phase 5 loop execution
    # SELECT region_name, SUM(sales) as net_sales FROM (SELECT * FROM (SELECT * FROM sales_data) AS sub WHERE order_date >= '2025-01-01' AND order_date <= '2025-12-31') AS agg_sub GROUP BY region_name
    
    sql = """
    SELECT region_name, SUM(sales) as net_sales 
    FROM sales_data 
    WHERE order_date >= '2025-01-01' AND order_date <= '2025-12-31' 
    GROUP BY region_name
    ORDER BY region_name
    """
    
    result = runner.exec(sql, metric_name="net_sales", dimensions=["region"])
    
    print("Execution Result:")
    print(result.dataframe)
    
    # Assertions
    res_df = result.dataframe
    assert len(res_df) == 2
    assert res_df.iloc[0]['region_name'] == 'North'
    assert res_df.iloc[0]['net_sales'] == 100 # Matches 2025-01-15 only
    assert res_df.iloc[1]['region_name'] == 'South' 
    # South has 200 (Feb) + 300 (Jun) = 500
    assert res_df.iloc[1]['net_sales'] == 500 
    
    print("Test Runtime Passed!")

if __name__ == "__main__":
    test_runtime()
