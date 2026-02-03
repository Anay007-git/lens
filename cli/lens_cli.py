#!/usr/bin/env python
"""LENS CLI - Run LENS queries from the command line."""
import argparse
import sys
import os

# Add project root to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pandas as pd
from lens.compiler.parser import LensParser
from lens.semantics.registry import MetricRegistry, DimensionRegistry, Metric, Dimension
from lens.semantics.validator import SemanticValidator, SemanticError
from lens.time_intelligence.calendar_logic import FiscalCalendar
from lens.planner.logical_planner import LogicalPlanner
from lens.sql_gen.duckdb_generator import DuckDBGenerator
from lens.runtime.runner import LensRunner
from lens.story.trend_analyzer import TrendAnalyzer
from lens.story.narrative_generator import NarrativeGenerator

def setup_default_registry():
    metrics = MetricRegistry()
    metrics.add(Metric(name="net_sales", sql_expression="SUM(sales)"))
    metrics.add(Metric(name="total_orders", sql_expression="COUNT(*)"))
    
    dims = DimensionRegistry()
    dims.add(Dimension(name="region", sql_expression="region_name"))
    dims.add(Dimension(name="product", sql_expression="product_name"))
    
    return metrics, dims

def setup_sample_data(runner):
    sample_df = pd.DataFrame({
        'region_name': ['North', 'South', 'East', 'West'],
        'product_name': ['Widget', 'Widget', 'Gadget', 'Gadget'],
        'order_date': pd.to_datetime(['2025-01-15', '2025-02-20', '2025-03-10', '2025-04-05']),
        'sales': [100, 200, 150, 300]
    })
    runner.register_dataframe("sales_data", sample_df)

def main():
    parser = argparse.ArgumentParser(description="LENS Language CLI")
    parser.add_argument('-q', '--query', type=str, required=True, help='LENS query to execute')
    args = parser.parse_args()
    
    query_text = args.query
    
    # Initialize components
    metrics, dims = setup_default_registry()
    calendar = FiscalCalendar(start_month=1)
    
    lens_parser = LensParser()
    validator = SemanticValidator(metrics, dims)
    planner = LogicalPlanner(metrics, dims, calendar)
    sql_gen = DuckDBGenerator()
    runner = LensRunner()
    trend = TrendAnalyzer()
    narrator = NarrativeGenerator()
    
    setup_sample_data(runner)
    
    try:
        # 1. Parse
        ast = lens_parser.parse(query_text)
        print(f"Parsed: metric={ast.metric}, dims={ast.dimensions}, time={ast.time_filter}")
        
        # 2. Validate
        validator.validate(ast)
        
        # 3. Plan
        plan = planner.plan(ast)
        
        # 4. Generate SQL
        sql = sql_gen.generate(plan)
        print(f"\n--- SQL ---")
        print(sql)
        
        # 5. Execute
        result = runner.exec(sql, ast.metric, ast.dimensions)
        print(f"\n--- Result ---")
        print(result.dataframe.to_string(index=False))
        
        # 6. Story
        # Use actual column names from result
        actual_dims = [c for c in result.dataframe.columns if c != ast.metric]
        insight = trend.analyze(result.dataframe, actual_dims, ast.metric)
        story = narrator.generate(insight, ast.metric, actual_dims)
        print(f"\n--- Insight ---")
        print(story)
        
    except SemanticError as e:
        print(f"Semantic Error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
