# LENS - Language for Exploratory & Narrative Statistics

**LENS** is an open-source analytics programming language that bridges the gap between business questions and data execution using natural language.

## Features
- **Declarative Syntax**: English-like queries (`show net_sales by region`)
- **Time Intelligence**: Built-in FY, YTD, rolling dates
- **Auto-Visualization**: Generates best-fit charts (Vega-Lite)
- **Story Engine**: Produces narratives from data trends
- **No-Code Studio**: Streamlit-based visual interface

## Installation

```bash
pip install lens-lang
```

Or install from source:
```bash
git clone https://github.com/Anay007-git/lens.git
cd lens
pip install -e .
```

## Quick Start

### CLI
```bash
python cli/lens_cli.py -q "show net_sales by region for FY2025"
```

### Studio (No-Code UI)
```bash
python -m streamlit run studio/app.py
```

### Python API
```python
from lens.compiler.parser import LensParser

parser = LensParser()
ast = parser.parse("show net_sales by region for FY2025")
print(ast)
```

## Example Query

```lens
show net_sales by region
for FY2025
compare with previous year
```

**Output:**
- SQL query
- Data table
- Auto-generated chart
- Business narrative

## Architecture

```
lens/
├── compiler/        # Lark parser + AST
├── semantics/       # Metric/Dimension registry
├── time_intelligence/  # FY, YTD, relative dates
├── planner/         # Logical plan builder
├── sql_gen/         # DuckDB SQL generator
├── runtime/         # Query execution
├── visualization/   # Altair/Vega-Lite charts
└── story/           # Trend analysis + narratives
```

## License

Apache 2.0

## Author

**Anay Biswas**

---

*Built with ❤️ for the analytics community*
