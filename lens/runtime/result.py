from dataclasses import dataclass
import pandas as pd
from typing import Optional

@dataclass
class LensResult:
    dataframe: pd.DataFrame
    sql: str
    metric: str
    dimensions: list[str]
    time_filter: Optional[str] = None
