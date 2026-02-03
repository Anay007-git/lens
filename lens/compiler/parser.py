from lark import Lark, Transformer
import os
from .ast_nodes import Query

class LensTransformer(Transformer):
    def start(self, items):
        return items[0]

    def query(self, items):
        show = items[0]
        time_filter = None
        comparison = None
        
        # Handle optional clauses
        for item in items[1:]:
            if isinstance(item, dict) and 'type' in item:
                 # Check clause type based on return value structure from sub-rules
                 # Simplified for MVP:
                 pass
            # For now, let's just inspect what we get. 
            # Actually, let's make the sub-rules return specific objects or dicts
            
        # Refined approach:
        # items[0] is always show_clause (dict)
        # items[1] could be for_clause, compare_clause or None
        
        # Let's check types
        metric = show['metric']
        dims = show['dimensions']
        
        for item in items[1:]:
            if item is None:
                continue
            if 'time_expr' in item:
                time_filter = item['time_expr']
            if 'comparison' in item:
                comparison = item['comparison']
                
        return Query(metric=metric, dimensions=dims, time_filter=time_filter, comparison=comparison)

    def show_clause(self, items):
        metric = items[0]
        dimensions = [d for d in items[1:]]
        return {'metric': metric, 'dimensions': dimensions}

    def by_clause(self, items):
        return items[0] 

    def for_clause(self, items):
        return {'time_expr': items[0]}

    def compare_clause(self, items):
        return {'comparison': items[0]}

    def metric(self, items):
        return str(items[0])

    def dimension(self, items):
        return str(items[0])

    def time_expr(self, items):
        return str(items[0])
    
    def prev_year(self, items):
        return "previous_year"

    def prev_month(self, items):
        return "previous_month"

class LensParser:
    def __init__(self):
        grammar_path = os.path.join(os.path.dirname(__file__), 'grammar.lark')
        with open(grammar_path, 'r') as f:
            grammar = f.read()
        self.parser = Lark(grammar, start='start', parser='lalr', transformer=LensTransformer())

    def parse(self, text):
        return self.parser.parse(text)
