import streamlit as st
import time
import asyncio
from research_agents import process_research_request  # Import function from backend

# 🌟 Streamlit Page Config
st.set_page_config(
    page_title="Research Buddy 🤖",
    page_icon="📚",
    layout="wide"
)

# 🎨 Custom CSS for Styling
st.markdown(
    """
    <style>
    .stChatMessageUser { color: #1E88E5; font-weight: bold; }
    .stChatMessageAssistant { color: #43A047; font-weight: bold; }
    .stTextInput>div>div>input { font-size: 18px; }
    .chat-container { background-color: #F4F4F4; padding: 15px; border-radius: 10px; }
    .status { color: green; font-weight: bold; }
    </style>
    """,
    unsafe_allow_html=True
)

# 📚 Sidebar with Sample Prompts
st.sidebar.title("💡 Need Inspiration?")
st.sidebar.write("Try these research queries:")

sample_prompts = [
    "Give research papers related to emotion recognition using deep learning.",
    "Find latest research papers on artificial intelligence.",
    "How is deep learning used in medical imaging?",
    "Generate an APA citation for 'Transformer Models in NLP' by J. Doe, 2022.",
    "What are the ethical concerns in AI research?",
]

# ✅ Ensure session_state variables are initialized
if "selected_prompt" not in st.session_state:
    st.session_state.selected_prompt = ""

if "messages" not in st.session_state:
    st.session_state.messages = []

# 🎯 Sidebar buttons to autofill input
for prompt in sample_prompts:
    if st.sidebar.button(prompt):
        st.session_state.selected_prompt = prompt

# 💬 Chat Title
st.markdown("## 📚 Research Buddy 🤖")
st.write("Ask anything about research papers, summaries, citations, or academic insights!")

# 🔍 Autofill input if a prompt is selected
user_input = st.chat_input("Ask me a research question...")
if st.session_state.selected_prompt:
    user_input = st.session_state.selected_prompt
    st.session_state.selected_prompt = ""  # Reset after autofill

# 🔄 Display Chat History
for message in st.session_state.messages:
    role = message["role"]
    with st.chat_message(role):
        st.markdown(message["content"], unsafe_allow_html=True)

# ✅ Function to format AI response for better readability
def format_response(response):
    """Enhances response readability by adding markdown formatting."""
    formatted_response = ""

    # Detect structured responses (e.g., lists, citations)
    if "\n" in response:
        lines = response.split("\n")
        for line in lines:
            if line.strip():
                if ":" in line:  # Key-Value format (e.g., "Title: Deep Learning")
                    formatted_response += f"**{line.split(':')[0].strip()}**: {line.split(':')[1].strip()}  \n"
                else:
                    formatted_response += f"- {line.strip()}  \n"
    else:
        formatted_response = response  # Keep simple text as-is

    return formatted_response

# 🔍 Processing AI Response
if user_input:
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": f"🧑‍💻 **You:** {user_input}"})

    # Display user message
    with st.chat_message("user"):
        st.markdown(f"🧑‍💻 **You:** {user_input}", unsafe_allow_html=True)

    # AI is "thinking..."
    with st.chat_message("assistant"):
        status = st.empty()
        status.markdown("⏳ **Thinking...**", unsafe_allow_html=True)

        # Process research query using AI agents
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        response = loop.run_until_complete(process_research_request(user_input))

        # 🎬 Stream response word by word
        response_text = ""
        for word in response.split():
            response_text += word + " "
            status.markdown(f"🤖 **Research Buddy:** {response_text}", unsafe_allow_html=True)
            time.sleep(0.05)

        # Format the final response
        formatted_response = format_response(response)

    # Add AI assistant's response to chat history
    st.session_state.messages.append({"role": "assistant", "content": f"🤖 **Research Buddy:**  \n{formatted_response}"})
    
    # Display formatted response
    with st.chat_message("assistant"):
        st.markdown(f"🤖 **Research Buddy:**  \n{formatted_response}", unsafe_allow_html=True)

# 📖 User Guide Section
st.sidebar.markdown("## 📖 How to Use")
st.sidebar.markdown(
    """
    - 🏷️ **Choose a topic** from sample prompts.
    - 📝 **Ask research-related questions.**
    - 📑 **Get AI-generated answers, summaries, & citations.**
    - 🔄 **Chat history is saved during the session.**
    """
)
