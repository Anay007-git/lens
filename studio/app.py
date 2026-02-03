import streamlit as st
import pandas as pd
import sys
import os

# Add project root to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from lens.compiler.parser import LensParser
from lens.semantics.registry import MetricRegistry, DimensionRegistry, Metric, Dimension
from lens.semantics.validator import SemanticValidator, SemanticError
from lens.time_intelligence.calendar_logic import FiscalCalendar
from lens.planner.logical_planner import LogicalPlanner
from lens.sql_gen.duckdb_generator import DuckDBGenerator
from lens.runtime.runner import LensRunner
from lens.visualization.chart_generator import ChartGenerator
from lens.story.trend_analyzer import TrendAnalyzer
from lens.story.narrative_generator import NarrativeGenerator

# --- Page Config ---
st.set_page_config(page_title="LENS Studio", page_icon="🔍", layout="wide")
st.title("🔍 LENS Studio")
st.markdown("*No-code analytics powered by natural language*")

# --- Initialize Components (cached for performance) ---
@st.cache_resource
def init_components():
    metrics = MetricRegistry()
    metrics.add(Metric(name="net_sales", sql_expression="SUM(sales)"))
    metrics.add(Metric(name="total_orders", sql_expression="COUNT(*)"))
    
    dims = DimensionRegistry()
    dims.add(Dimension(name="region", sql_expression="region_name"))
    dims.add(Dimension(name="product", sql_expression="product_name"))
    
    calendar = FiscalCalendar(start_month=1)
    
    return {
        "parser": LensParser(),
        "validator": SemanticValidator(metrics, dims),
        "planner": LogicalPlanner(metrics, dims, calendar),
        "sql_gen": DuckDBGenerator(),
        "runner": LensRunner(),
        "chart_gen": ChartGenerator(),
        "trend": TrendAnalyzer(),
        "narrator": NarrativeGenerator(),
        "metrics": metrics,
        "dims": dims,
    }

@st.cache_resource
def setup_sample_data(_components):
    """Setup sample data in DuckDB."""
    runner = _components["runner"]
    sample_df = pd.DataFrame({
        'region_name': ['North', 'South', 'East', 'West', 'North', 'South'],
        'product_name': ['Widget', 'Widget', 'Gadget', 'Gadget', 'Widget', 'Gadget'],
        'order_date': pd.to_datetime(['2025-01-15', '2025-02-20', '2025-03-10', '2025-04-05', '2025-05-11', '2025-06-22']),
        'sales': [100, 200, 150, 300, 250, 400]
    })
    runner.register_dataframe("sales_data", sample_df)
    return sample_df

components = init_components()
sample_data = setup_sample_data(components)

# --- UI ---
st.sidebar.header("📊 Data Preview")
st.sidebar.dataframe(sample_data, use_container_width=True)

st.header("Write your query")
query_text = st.text_area(
    "Enter a LENS query:", 
    value="show net_sales by region\nfor FY2025",
    height=100
)

if st.button("▶️ Run Query", type="primary"):
    try:
        # 1. Parse
        ast = components["parser"].parse(query_text)
        st.success(f"Parsed: Metric=`{ast.metric}`, Dimensions=`{ast.dimensions}`, Time=`{ast.time_filter}`")
        
        # 2. Validate
        components["validator"].validate(ast)
        
        # 3. Plan
        plan = components["planner"].plan(ast)
        
        # 4. Generate SQL
        sql = components["sql_gen"].generate(plan)
        
        with st.expander("🔧 Generated SQL"):
            st.code(sql, language="sql")
        
        # 5. Execute
        result = components["runner"].exec(sql, ast.metric, ast.dimensions)
        
        col1, col2 = st.columns([2, 1])
        
        # Use actual column names from result (not AST dimension names)
        actual_dims = [c for c in result.dataframe.columns if c != ast.metric]
        
        with col1:
            st.subheader("📈 Chart")
            chart = components["chart_gen"].generate(result.dataframe, actual_dims, ast.metric)
            st.altair_chart(chart, use_container_width=True)
        
        with col2:
            st.subheader("📝 Insight")
            insight = components["trend"].analyze(result.dataframe, actual_dims, ast.metric)
            story = components["narrator"].generate(insight, ast.metric, actual_dims)
            st.markdown(story)
        
        st.subheader("📊 Data")
        st.dataframe(result.dataframe, use_container_width=True)
        
    except SemanticError as e:
        st.error(f"Semantic Error: {e}")
    except Exception as e:
        st.error(f"Error: {e}")
        st.exception(e)
