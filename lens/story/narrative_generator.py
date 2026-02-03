from .trend_analyzer import TrendInsight

class NarrativeGenerator:
    def generate(self, insight: TrendInsight, metric: str, dimensions: list[str]) -> str:
        metric_display = metric.replace('_', ' ').title()
        
        parts = []
        
        # Trend direction
        if insight.direction == 'up':
            parts.append(f"**{metric_display}** is trending **upward** with a change of **+{insight.change_pct}%**.")
        elif insight.direction == 'down':
            parts.append(f"**{metric_display}** is trending **downward** with a change of **{insight.change_pct}%**.")
        else:
            parts.append(f"**{metric_display}** is **stable** with minimal change.")
        
        # Top/Bottom performers
        if insight.top_performer:
            parts.append(f"Top performer: **{insight.top_performer}**.")
        
        if insight.bottom_performer and insight.bottom_performer != insight.top_performer:
            parts.append(f"Bottom performer: **{insight.bottom_performer}**.")
        
        return " ".join(parts)
