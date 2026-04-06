from unittest.mock import patch
from agents.market_analyst import market_analyst_agent

# We patch the 'forward' method of the tool ALREADY inside the agent's toolbox
@patch.object(market_analyst_agent.tools["search_web"], "forward")
def test_vague_idea_asks_question(mock_forward):
    # 1. Run the agent with a vague idea
    market_analyst_agent.run("I want to build an app for UPSC aspirants.")

    # 2. Assert that the search tool's execution was NEVER triggered
    mock_forward.assert_not_called()

if __name__ == "__main__":
    test_vague_idea_asks_question()