import sys
import os

# Add project root to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from lens.compiler.parser import LensParser
from lens.semantics.registry import MetricRegistry, DimensionRegistry, Metric, Dimension
from lens.semantics.validator import SemanticValidator, SemanticError

def test_semantic_validation():
    # Setup Registry
    metrics = MetricRegistry()
    metrics.add(Metric(name="net_sales", sql_expression="SUM(sales)"))
    
    dims = DimensionRegistry()
    dims.add(Dimension(name="region", sql_expression="region_name"))

    validator = SemanticValidator(metrics, dims)
    parser = LensParser()

    # Test Valid Query
    query = parser.parse("show net_sales by region")
    assert validator.validate(query) is True
    print("Valid query passed.")

    # Test Invalid Metric
    try:
        query_invalid_metric = parser.parse("show gross_profit by region")
        validator.validate(query_invalid_metric)
        assert False, "Should have raised SemanticError for invalid metric"
    except SemanticError as e:
        print(f"Caught expected error: {e}")
        assert "Unknown metric: 'gross_profit'" in str(e)

    # Test Invalid Dimension
    try:
        query_invalid_dim = parser.parse("show net_sales by country")
        validator.validate(query_invalid_dim)
        assert False, "Should have raised SemanticError for invalid dimension"
    except SemanticError as e:
        print(f"Caught expected error: {e}")
        assert "Unknown dimension: 'country'" in str(e)

if __name__ == "__main__":
    test_semantic_validation()
