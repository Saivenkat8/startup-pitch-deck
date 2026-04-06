import json
from agents.financial_analyst import financial_analyst_agent, FinancialStrategy
from pydantic import ValidationError

def test_financial_output_schema():
    # 1. Run the agent to get the raw response
    raw_response = financial_analyst_agent.run("Provide financial strategy for a dog walking app.")
    
    # 2. Try to parse the response into our Pydantic model
    try:
        # We assume the agent returns a JSON string
        data = json.loads(raw_response)
        validated_data = FinancialStrategy(**data)
        print("--- Test Passed: Data is schema-valid! ---")
        
    except (json.JSONDecodeError, ValidationError) as e:
        print(f"--- Test Failed: Validation Error! {e} ---")
        assert False