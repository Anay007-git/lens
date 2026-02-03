import altair as alt
import pandas as pd
from .explorer import ChartType, DataExplorer

class ChartGenerator:
    def __init__(self):
        self.explorer = DataExplorer()

    def generate(self, df: pd.DataFrame, dimensions: list[str], metric: str) -> alt.Chart:
        chart_type = self.explorer.analyze(df, dimensions, metric)
        
        if not dimensions:
            # Single value - just return a text chart or table
            return alt.Chart(df).mark_text().encode(
                text=metric
            ).properties(title=f"{metric}")
        
        dim_col = dimensions[0]
        
        if chart_type == ChartType.BAR:
            return alt.Chart(df).mark_bar().encode(
                x=alt.X(dim_col, title=dim_col.replace('_', ' ').title()),
                y=alt.Y(metric, title=metric.replace('_', ' ').title()),
                color=alt.Color(dim_col, legend=None),
                tooltip=[dim_col, metric]
            ).properties(
                title=f"{metric.replace('_', ' ').title()} by {dim_col.replace('_', ' ').title()}",
                width=400,
                height=300
            )
        
        elif chart_type == ChartType.LINE:
            return alt.Chart(df).mark_line(point=True).encode(
                x=alt.X(dim_col, title=dim_col.replace('_', ' ').title()),
                y=alt.Y(metric, title=metric.replace('_', ' ').title()),
                tooltip=[dim_col, metric]
            ).properties(
                title=f"{metric.replace('_', ' ').title()} over Time",
                width=500,
                height=300
            )
        
        else:  # TABLE
            # Altair doesn't have a native table, so return a simple text display
            return alt.Chart(df.head(20)).mark_text().encode(
                y=alt.Y('row_number:O', axis=None),
                text=dim_col
            ).transform_window(row_number='row_number()')

    def to_vega_lite(self, df: pd.DataFrame, dimensions: list[str], metric: str) -> dict:
        """Returns the Vega-Lite JSON spec."""
        chart = self.generate(df, dimensions, metric)
        return chart.to_dict()
