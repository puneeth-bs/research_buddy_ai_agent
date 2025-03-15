import os
import asyncio
from openai import OpenAI
from agents import Agent, Runner
from dotenv import load_dotenv

# Load API key from .env file
load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")

if not openai_api_key:
    raise ValueError("❌ OPENAI_API_KEY is not set. Please set it in an environment variable or .env file.")

# Initialize OpenAI Client
client = OpenAI(api_key=openai_api_key)

# 🔹 Define Specialized Research Agents
search_agent = Agent(name="Search Agent", instructions="Find relevant academic papers.")
summarization_agent = Agent(name="Summarization Agent", instructions="Summarize research papers.")
qa_agent = Agent(name="Q&A Agent", instructions="Answer research-related questions.")
citation_agent = Agent(name="Citation Agent", instructions="Generate APA and IEEE citations.")

# 🔹 Triage Agent for Routing Requests
triage_agent = Agent(
    name="Triage Agent",
    instructions="Delegate the research query to the appropriate agent based on task type.",
    handoffs=[search_agent, summarization_agent, qa_agent, citation_agent],
)

# Function to process AI research responses
async def process_research_request(user_input):
    """Routes user queries to the correct agent based on task type."""
    if "summarize" in user_input.lower():
        agent = summarization_agent
    elif "find papers" in user_input.lower() or "search" in user_input.lower():
        agent = search_agent
    elif "citation" in user_input.lower():
        agent = citation_agent
    else:
        agent = qa_agent  # Default to Q&A if no specific type is found

    # Run the research AI agent asynchronously
    response = await Runner.run(agent, input=user_input)
    return response.final_output
