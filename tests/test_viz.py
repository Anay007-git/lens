import sys
import os
import pandas as pd

# Add project root to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from lens.visualization.explorer import DataExplorer, ChartType
from lens.visualization.chart_generator import ChartGenerator

def test_explorer():
    explorer = DataExplorer()
    
    # Test 1: Categorical dimension -> BAR
    df1 = pd.DataFrame({
        'region_name': ['North', 'South', 'East'],
        'net_sales': [100, 200, 150]
    })
    assert explorer.analyze(df1, ['region_name'], 'net_sales') == ChartType.BAR
    print("Test 1 (Categorical -> BAR): Passed")
    
    # Test 2: Temporal dimension -> LINE
    df2 = pd.DataFrame({
        'order_date': pd.to_datetime(['2025-01-01', '2025-02-01', '2025-03-01']),
        'net_sales': [100, 200, 150]
    })
    assert explorer.analyze(df2, ['order_date'], 'net_sales') == ChartType.LINE
    print("Test 2 (Temporal -> LINE): Passed")

def test_chart_generator():
    generator = ChartGenerator()
    
    df = pd.DataFrame({
        'region_name': ['North', 'South', 'East'],
        'net_sales': [100, 200, 150]
    })
    
    spec = generator.to_vega_lite(df, ['region_name'], 'net_sales')
    
    mark = spec.get('mark')
    if isinstance(mark, dict):
        assert mark.get('type') == 'bar'
    else:
        assert mark == 'bar'
    print("Test 3 (Chart Generation): Passed")
    print("Vega-Lite Spec (truncated):", {k: v for k, v in spec.items() if k != 'data'})

if __name__ == "__main__":
    test_explorer()
    test_chart_generator()
