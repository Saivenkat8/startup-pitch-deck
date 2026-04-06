import os
from dotenv import load_dotenv
from smolagents import ToolCallingAgent, OpenAIServerModel
from tools.market_tools import search_web

# Load our API key from the .env file
load_dotenv()

# 1. Define the LLM we want to use
model = OpenAIServerModel(model_id="gpt-4o") 

# 2. Custom instructions (merged into the default tool-calling system prompt via `instructions`)
instructions = """
You are a sharp, analytical, and professional startup advisor acting as a Market Research Analyst.

Your workflow:
1. Analyze the user's startup idea. If it lacks a clear target user or specific problem, ask exactly ONE clarifying question in a helpful, professional tone. Do not proceed until the user replies.
2. Once the idea is clear, you MUST use your `search_web` tool to find real external data, competitor signals, and market trends. Do not guess or hallucinate numbers.
3. Output a structured report containing: Problem definition, Target users, TAM/SAM/SOM estimates, Competitors, Risks, and Suggested business model.
"""

# 3. Initialize the actual agent
market_analyst_agent = ToolCallingAgent(
    tools=[search_web],
    model=model,
    instructions=instructions,
    name="market_analyst",
    description="Analyzes the startup idea, conducts market research, and defines the target audience and competition."
)