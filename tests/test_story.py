import sys
import os
import pandas as pd

# Add project root to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from lens.story.trend_analyzer import TrendAnalyzer
from lens.story.narrative_generator import NarrativeGenerator

def test_story_engine():
    analyzer = TrendAnalyzer()
    narrator = NarrativeGenerator()
    
    # Test 1: Upward trend
    df = pd.DataFrame({
        'region_name': ['North', 'South', 'East'],
        'net_sales': [100, 200, 300]
    })
    
    insight = analyzer.analyze(df, ['region_name'], 'net_sales')
    print("Insight:", insight)
    assert insight.direction == 'up'
    assert insight.top_performer == 'East'
    
    narrative = narrator.generate(insight, 'net_sales', ['region_name'])
    print("Narrative:", narrative)
    assert 'upward' in narrative
    assert 'East' in narrative
    print("Test 1 (Upward Trend): Passed")
    
    # Test 2: Downward trend
    df_down = pd.DataFrame({
        'region_name': ['A', 'B', 'C'],
        'revenue': [500, 300, 100]
    })
    insight_down = analyzer.analyze(df_down, ['region_name'], 'revenue')
    assert insight_down.direction == 'down'
    print("Test 2 (Downward Trend): Passed")

if __name__ == "__main__":
    test_story_engine()
