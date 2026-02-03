import re
from datetime import date
from typing import Optional, Tuple
from .calendar_logic import FiscalCalendar

class DateParser:
    def __init__(self, calendar: FiscalCalendar):
        self.calendar = calendar

    def parse_time_filter(self, expression: str) -> Optional[Tuple[date, date]]:
        """Parses strings like 'FY2025', '2024'."""
        expression = expression.strip().upper()
        
        # Regex for FYYYYY
        fy_match = re.match(r'^FY(\d{4})$', expression)
        if fy_match:
            year = int(fy_match.group(1))
            return self.calendar.get_fy_range(year)
            
        # Regex for YYYY
        cal_match = re.match(r'^(\d{4})$', expression)
        if cal_match:
            year = int(cal_match.group(1))
            # Treat plain year as Calendar Year (Jan-Dec) or Fiscal? 
            # Usually strict numbers mean Calendar Year, strict FY means Fiscal.
            # But relying on the calendar object for strictly FY requests.
            # For this MVP, if they pass "2025" and we are in fiscal mode, it might be ambiguous.
            # Let's assume plain year is also fiscal year for simplicity or specific calendar year.
            # actually let's implement Calendar Year for '2025'
            return date(year, 1, 1), date(year, 12, 31)

        return None
