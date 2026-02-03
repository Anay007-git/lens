from dataclasses import dataclass
from datetime import date, timedelta
from typing import Tuple

@dataclass
class FiscalCalendar:
    start_month: int = 1  # 1 = January, 4 = April, etc.

    def get_fy_range(self, year: int) -> Tuple[date, date]:
        """Returns (start_date, end_date) for a given Fiscal Year."""
        start_year = year if self.start_month == 1 else year - 1
        start_date = date(start_year, self.start_month, 1)
        
        # End date is start date of next FY minus 1 day
        next_start_year = start_year + 1
        next_start_date = date(next_start_year, self.start_month, 1)
        end_date = next_start_date - timedelta(days=1)
        
        return start_date, end_date

    def get_period_prev_year(self, start_date: date, end_date: date) -> Tuple[date, date]:
        """Returns the equivalent period in the previous year."""
        # Simplistic implementation: subtract 1 year (approximate for leap years handling in standard biz logic usually fine to just map day/month)
        # Using simple year subtraction (watch out for Feb 29)
        
        def subtract_year(d):
            try:
                return d.replace(year=d.year - 1)
            except ValueError:
                # Handle Feb 29 -> Feb 28
                return d.replace(month=2, day=28, year=d.year - 1)

        return subtract_year(start_date), subtract_year(end_date)
