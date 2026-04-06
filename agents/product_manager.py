import os
from dotenv import load_dotenv
from smolagents import ToolCallingAgent, OpenAIServerModel

# Load environment variables
load_dotenv()

# Initialize the model
model = OpenAIServerModel(model_id="gpt-4o")

# System prompt based on tutorial requirements
instructions = """
You are an experienced Product Manager 👔. Your goal is to take a market research report and synthesize it into a focused product definition.

CRITICAL RULE: Do not rewrite or repeat the market analysis data. Instead, extract the key insights to produce an actionable definition.

Your output must follow this structure:
1. **Product Overview**: A concise summary of what the product is and exactly who it serves.
2. **Core Value Proposition**: The single most important benefit the product provides.
3. **Key Features**: Identify 3-6 essential features that solve the core problem identified in the market research.
4. **Constraints & Considerations**: List any technical or market-based realities that must be kept in mind during development.
"""

# Initialize the Product Manager Agent
product_manager_agent = ToolCallingAgent(
    tools=[], 
    model=model,
    instructions=instructions,
    name="product_manager",
    description="Converts market research into a focused product specification and feature set."
)