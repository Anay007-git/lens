import sys
import os
from datetime import date

# Add project root to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from lens.time_intelligence.calendar_logic import FiscalCalendar
from lens.time_intelligence.date_parser import DateParser

def test_time_intelligence():
    # Test 1: Standard Calendar (Jan 1)
    cal = FiscalCalendar(start_month=1)
    parser = DateParser(cal)
    
    # Test FY2025 (should be 2025-01-01 to 2025-12-31)
    start, end = parser.parse_time_filter("FY2025")
    assert start == date(2025, 1, 1)
    assert end == date(2025, 12, 31)
    print("Test 1 (Jan FY) Passed")

    # Test 2: April Fiscal Year (start_month=4)
    # FY2025 usually means ending in 2025? Or starting in 2025?
    # Logic: Usually FY25 = year ending 2025. 
    # BUT simple implementation often is "Fiscal Year 2025 starts in 2025".
    # Let's adjust logic: 
    # If start_month=4: FY2025. 
    # - Option A: Apr 2024 - Mar 2025 (Year Ending approach)
    # - Option B: Apr 2025 - Mar 2026 (Year Starting approach)
    # For MVP, my code implemented Option A logic:
    # "start_year = year if self.start_month == 1 else year - 1"
    # So if month=4, year=2025 => start_year=2024. => Apr 1, 2024.
    # Checks:
    cal_apr = FiscalCalendar(start_month=4)
    parser_apr = DateParser(cal_apr)
    
    start_apr, end_apr = parser_apr.parse_time_filter("FY2025")
    assert start_apr == date(2024, 4, 1)
    assert end_apr == date(2025, 3, 31)
    print("Test 2 (Apr FY) Passed")
    
    # Test 3: Previous Year Calculation
    prev_start, prev_end = cal.get_period_prev_year(date(2025, 1, 1), date(2025, 12, 31))
    assert prev_start == date(2024, 1, 1)
    assert prev_end == date(2024, 12, 31)
    print("Test 3 (Prev Year) Passed")

if __name__ == "__main__":
    test_time_intelligence()
