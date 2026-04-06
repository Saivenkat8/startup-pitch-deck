import os
from typing import List
from pydantic import BaseModel, Field
from dotenv import load_dotenv
from smolagents import ToolCallingAgent, OpenAIServerModel

# Load API keys
load_dotenv()

# 1. Define the structured output schema 
# This ensures the agent always returns data in a predictable format.
class FinancialStrategy(BaseModel):
    revenue_streams: List[str] = Field(description="List of ways the product generates money.")
    pricing_model: str = Field(description="Detailed pricing strategy, tiers, and justification.")
    key_cost_drivers: List[str] = Field(description="The primary expenses required to run and grow the business.")
    initial_investment_needs: str = Field(description="Rough estimate of the capital needed to launch and sustain the MVP.")
    financial_logic: str = Field(description="A brief explanation of why this model is sustainable for this specific market.")

# Initialize the model
model = OpenAIServerModel(model_id="gpt-4o")

# 2. System Prompt [cite: 130, 132]
# We instruct the agent to be pragmatic and consistent with previous data.
instructions = """
You are a pragmatic Financial Analyst for early-stage startups. 
Your job is to take market research and product specifications and transform them into a coherent financial narrative.

Instead of 5-year projections, focus on the 'Unit Economics' and the 'Business Model'. 
Ensure your numbers and logic are consistent with the market size and product features provided to you.

CRITICAL: Your final answer MUST be a single JSON object only (no markdown fences, no commentary before or after) with exactly these keys:
- "revenue_streams": array of strings
- "pricing_model": string
- "key_cost_drivers": array of strings
- "initial_investment_needs": string
- "financial_logic": string

Cover unit economics and business model in those fields; do not rename keys or omit any key.
"""

# 3. Initialize the Financial Analyst Agent
financial_analyst_agent = ToolCallingAgent(
    tools=[], # No external tools needed; it processes internal context
    model=model,
    instructions=instructions,
    name="financial_analyst",
    description="Generates a structured financial strategy and business model based on market and product data."
)