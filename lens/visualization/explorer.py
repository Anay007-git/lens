import pandas as pd
from enum import Enum, auto

class ChartType(Enum):
    BAR = auto()
    LINE = auto()
    TABLE = auto()

class DataExplorer:
    """Analyzes a DataFrame to determine the best chart type."""
    
    def analyze(self, df: pd.DataFrame, dimensions: list[str], metric: str) -> ChartType:
        if not dimensions:
            return ChartType.TABLE
            
        dim_col = dimensions[0]
        
        # Check if dimension is temporal
        if pd.api.types.is_datetime64_any_dtype(df[dim_col]):
            return ChartType.LINE
        
        # Check cardinality - if too many categories, suggest table
        unique_count = df[dim_col].nunique()
        if unique_count > 20:
            return ChartType.TABLE
            
        return ChartType.BAR
