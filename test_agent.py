import pytest
from agent import run_agent

def test_run_agent():
    # Sample input data
    data = {
        'today': {'revenue': 1000, 'cost': 700, 'number_of_customers': 50},
        'yesterday': {'revenue': 900, 'cost': 650, 'number_of_customers': 45}
    }
    result = run_agent(data)
    assert isinstance(result, dict)
    # Check profit calculation
    assert result['profit'] == 300
    assert result['profit_status'] == 'profit'
    # Check alerts and recommendations
    assert 'alerts' in result
    assert 'recommendations' in result
    # CAC increased more than 20% should NOT be triggered in this case
    assert not any('CAC increased' in alert for alert in result['alerts'])
    # Should recommend increasing ad budget if sales are growing
    assert any('advertising budget' in rec for rec in result['recommendations'])
    # Should not recommend reducing costs since profit is positive
    assert not any('Reduce costs' in rec for rec in result['recommendations'])
 