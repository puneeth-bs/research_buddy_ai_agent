import os
import asyncio
from openai import OpenAI
from agents import Agent, Runner
from dotenv import load_dotenv

import agentops
agentops.init("57a140be-a0be-45cf-b9d1-ba3fadbbfc79")

# Load API key from .env file
load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")

if not openai_api_key:
    raise ValueError("❌ OPENAI_API_KEY is not set. Please set it in an environment variable or .env file.")

# Initialize OpenAI Client
client = OpenAI(api_key=openai_api_key)

# 🔹 Define Specialized Research Agents with Improved Prompts
search_agent = Agent(
    name="Search Agent",
    instructions="""
    You are an academic research assistant. Your task is to find relevant, high-quality academic papers 
    based on the given topic. Provide a list of the **top 5 most relevant papers**, including:
    - **Title**
    - **Authors**
    - **Year of Publication**
    - **Brief Summary**
    - **Link to the Paper (if available)**

    If the query is too broad, suggest a more specific research focus.
    """
)

summarization_agent = Agent(
    name="Summarization Agent",
    instructions="""
    You are an AI that specializes in summarizing research papers. Given a research paper excerpt or title, 
    provide a **concise and structured summary** including:
    - **Objective**: What is the purpose of this research?
    - **Key Findings**: What are the main results?
    - **Methodology**: What methods were used?
    - **Impact**: How does this research contribute to the field?

    Keep responses under **250 words** and use clear, academic language.
    """
)

qa_agent = Agent(
    name="Q&A Agent",
    instructions="""
    You are an AI research assistant that answers complex research-related questions based on existing 
    academic knowledge. When answering:
    - Provide a **structured response** with bullet points.
    - Cite **widely accepted knowledge** where possible.
    - If the question is too broad, suggest a more focused inquiry.

    Example:
    **Q:** "How is deep learning used in medical imaging?"
    **A:**
    - **Image Classification**: CNNs classify diseases from X-rays and MRIs.
    - **Segmentation**: AI models identify tumors and abnormalities.
    - **Reconstruction**: AI enhances low-resolution scans for better diagnostics.
    - **Recent Research Focus**: Transformer-based models for medical imaging.

    Always use **concise** and **technical** explanations suited for researchers.
    """
)

citation_agent = Agent(
    name="Citation Agent",
    instructions="""
    You are an AI citation generator. Given a **paper title, author(s), and year**, 
    format citations correctly in **APA and IEEE styles**. Ensure:
    - Proper punctuation and capitalization.
    - Correct formatting for journal articles, conference papers, and books.
    - Include DOIs or links if available.

    **Example Input:**
    "Transformer Models in NLP" by J. Doe, 2022

    **Example Output:**
    - **APA:** Doe, J. (2022). Transformer Models in NLP. *Journal of AI Research, 35*(4), 123-145. https://doi.org/10.xxxxx
    - **IEEE:** J. Doe, "Transformer Models in NLP," *J. AI Res.*, vol. 35, no. 4, pp. 123-145, 2022, doi: 10.xxxxx.

    Ensure high accuracy in formatting.
    """
)

# 🔹 Triage Agent for Routing Requests
triage_agent = Agent(
    name="Triage Agent",
    instructions="""
    You are a routing agent that determines the appropriate research assistant for the given query. 
    If the user asks about:
    - **Finding papers**, direct to the **Search Agent**.
    - **Summarizing research**, direct to the **Summarization Agent**.
    - **Answering research-related questions**, direct to the **Q&A Agent**.
    - **Generating citations**, direct to the **Citation Agent**.

    If the query is ambiguous, ask for clarification.
    """,
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
