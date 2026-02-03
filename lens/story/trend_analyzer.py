import pandas as pd
from dataclasses import dataclass
from typing import Optional

@dataclass
class TrendInsight:
    direction: str  # 'up', 'down', 'stable'
    change_pct: float
    top_performer: Optional[str] = None
    bottom_performer: Optional[str] = None

class TrendAnalyzer:
    def analyze(self, df: pd.DataFrame, dimensions: list[str], metric: str) -> TrendInsight:
        if df.empty:
            return TrendInsight(direction='stable', change_pct=0.0)
        
        metric_col = metric
        
        # Find top and bottom performers
        top_idx = df[metric_col].idxmax()
        bottom_idx = df[metric_col].idxmin()
        
        top_performer = None
        bottom_performer = None
        if dimensions:
            dim_col = dimensions[0]
            top_performer = str(df.loc[top_idx, dim_col])
            bottom_performer = str(df.loc[bottom_idx, dim_col])
        
        # Basic trend (compare first to last if temporal, else range)
        first_val = df[metric_col].iloc[0]
        last_val = df[metric_col].iloc[-1]
        
        if first_val == 0:
            change_pct = 100.0 if last_val > 0 else 0.0
        else:
            change_pct = ((last_val - first_val) / first_val) * 100
        
        if change_pct > 5:
            direction = 'up'
        elif change_pct < -5:
            direction = 'down'
        else:
            direction = 'stable'
        
        return TrendInsight(
            direction=direction,
            change_pct=round(change_pct, 2),
            top_performer=top_performer,
            bottom_performer=bottom_performer
        )
