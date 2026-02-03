import duckdb
import pandas as pd
from .result import LensResult

class LensRunner:
    def __init__(self, db_path: str = ":memory:"):
        self.conn = duckdb.connect(db_path)

    def exec(self, sql: str, metric_name: str, dimensions: list[str]) -> LensResult:
        # Execute Query
        df = self.conn.execute(sql).df()
        
        return LensResult(
            dataframe=df,
            sql=sql,
            metric=metric_name,
            dimensions=dimensions
        )

    def register_dataframe(self, name: str, df: pd.DataFrame):
        """Registers a pandas dataframe as a table in DuckDB for querying."""
        self.conn.register(name, df)
