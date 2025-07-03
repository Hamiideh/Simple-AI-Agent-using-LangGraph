"""
Business Agent using LangGraph
Analyzes daily business data and generates recommendations.
"""

from langgraph.graph import StateGraph, END

# Node 1: Input Node
def input_node(data):
    """Receives business data as input."""
    return data

# Node 2: Processing Nodepls pl
def processing_node(data):
    """Calculates profit, CAC, and percentage changes."""
    today = data.get('today', {})
    yesterday = data.get('yesterday', {})
    metrics = {}
    # Profit
    metrics['profit'] = today.get('revenue', 0) - today.get('cost', 0)
    # CAC
    today_customers = today.get('number_of_customers', 1) or 1
    yesterday_customers = yesterday.get('number_of_customers', 1) or 1
    metrics['cac_today'] = today.get('cost', 0) / today_customers
    metrics['cac_yesterday'] = yesterday.get('cost', 0) / yesterday_customers
    # Percentage changes
    metrics['revenue_change_pct'] = (
        (today.get('revenue', 0) - yesterday.get('revenue', 0)) / (yesterday.get('revenue', 1) or 1)
    ) * 100
    metrics['cost_change_pct'] = (
        (today.get('cost', 0) - yesterday.get('cost', 0)) / (yesterday.get('cost', 1) or 1)
    ) * 100
    # Include original data for reference
    metrics['today'] = today
    metrics['yesterday'] = yesterday
    return metrics

# Node 3: Recommendation Node
def recommendation_node(metrics):
    """Generates recommendations based on metrics."""
    output = {
        'profit': metrics['profit'],
        'profit_status': 'profit' if metrics['profit'] > 0 else 'loss',
        'alerts': [],
        'recommendations': []
    }
    # Alert if CAC increased > 20%
    cac_change = ((metrics['cac_today'] - metrics['cac_yesterday']) / (metrics['cac_yesterday'] or 1)) * 100
    if cac_change > 20:
        output['alerts'].append('CAC increased more than 20%')
        output['recommendations'].append('Review marketing campaigns due to CAC increase')
    # Recommend reducing costs if profit is negative
    if metrics['profit'] < 0:
        output['recommendations'].append('Reduce costs if profit is negative')
    # Recommend increasing ad budget if sales (revenue) are growing
    if metrics['revenue_change_pct'] > 0:
        output['recommendations'].append('Consider increasing advertising budget if sales are growing')
    # Warn if costs are growing faster than revenue
    if metrics['cost_change_pct'] > metrics['revenue_change_pct']:
        output['alerts'].append('Costs are growing faster than revenue')
    return output

# Build the LangGraph
def build_graph():
    graph = StateGraph()
    graph.add_node('input', input_node)
    graph.add_node('processing', processing_node)
    graph.add_node('recommendation', recommendation_node)
    graph.add_edge('input', 'processing')
    graph.add_edge('processing', 'recommendation')
    graph.add_edge('recommendation', END)
    graph.set_entry_point('input')
    return graph

# Main function to run the agent
def run_agent(data):
    graph = build_graph()
    result = graph.run(data)
    return result
