import sys
import os

# Add project root to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from importlib.util import find_spec
if find_spec("lark") is None:
    print("Installing lark...")
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "lark"])

from lens.compiler.parser import LensParser

def test_mvp_query():
    parser = LensParser()
    query = """
    show net_sales by region
    for FY2025
    compare with previous year
    """
    ast = parser.parse(query)
    print("AST:", ast)
    
    assert ast.metric == "net_sales"
    assert "region" in ast.dimensions
    assert ast.time_filter == "FY2025"
    assert ast.comparison == "previous_year"
    print("Test passed!")

if __name__ == "__main__":
    test_mvp_query()
