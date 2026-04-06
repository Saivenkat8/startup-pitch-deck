import os
from dotenv import load_dotenv
from smolagents import ToolCallingAgent, OpenAIServerModel

# Load API keys
load_dotenv()

# Initialize the model
model = OpenAIServerModel(model_id="gpt-4o")

# The system prompt we just designed
instructions = """
You are a World-Class Pitch Deck Designer 🎨. Your task is to turn startup research into a high-impact presentation using Marp Markdown.

DATA HANDLING RULES:
1. Use ONLY the information provided by the Market Analyst, Product Manager, and Financial Analyst. Do not invent new features, market stats, or pricing.
2. If a specific piece of data is missing, note it professionally rather than hallucinating a placeholder.

FORMATTING RULES:
- Use Marp Markdown syntax (use `---` to separate slides).
- Follow this strict 8-slide structure: Title, Problem, Market, Solution, Features, Business Model, Why Now, and Call to Action.
- Keep text concise: Use bullet points and bold text for readability.
"""

# Initialize the Pitch Creator Agent
pitch_creator_agent = ToolCallingAgent(
    tools=[], 
    model=model,
    instructions=instructions,
    name="pitch_creator",
    description="Synthesizes market, product, and financial data into a final Marp Markdown pitch deck."
)