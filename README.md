# Business Agent using LangGraph

This project implements an AI Agent that analyzes basic business data (e.g., daily sales and costs) and generates a summary report with actionable recommendations.

## Features
- Calculates daily profit
- Computes Customer Acquisition Cost (CAC)
- Compares today's and yesterday's revenue and costs
- Generates alerts and recommendations based on business logic

## Usage

### 1. Install dependencies
```
pip install -r requirements.txt
```

### 2. Run the agent
You can use the `run_agent` function in `agent.py`:

```python
from agent import run_agent

data = {
    'today': {'revenue': 1000, 'cost': 700, 'number_of_customers': 50},
    'yesterday': {'revenue': 900, 'cost': 650, 'number_of_customers': 45}
}
result = run_agent(data)
print(result)
```

### 3. Run tests
```
pytest test_agent.py
```

## Output Example
```
{
  'profit': 300,
  'profit_status': 'profit',
  'alerts': [],
  'recommendations': [
    'Consider increasing advertising budget if sales are growing'
  ]
}
``` 