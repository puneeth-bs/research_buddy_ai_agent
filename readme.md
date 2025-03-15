
You said:
# 📚 Research Buddy AI Agent 🤖

**Research Buddy AI Agent** is an intelligent research assistant that helps users search for research papers, summarize academic content, generate citations, and answer research-related questions. Built using **Streamlit** for the frontend and **OpenAI Agents** for AI-driven research.

## 🚀 Features
✅ **Find research papers** from AI-powered searches  
✅ **Summarize research papers** for easy reading  
✅ **Generate citations** in APA & IEEE formats  
✅ **Answer research-related questions**  
✅ **Interactive chat interface** powered by Streamlit  

---

## 📂 Project Structure
    .
    ├── app.py                                # main file to run the project
    ├── research_agents.py                    # contains AI agents written using OpenAPI Agents
    ├── requirements.txt                      # contains list of packages required to run the project
    ├── .gitignore
    └── README.md


---

## 🔧 Installation & Setup

### **Run the following commands**
bash
git clone https://github.com/puneeth-bs/research_buddy_ai_agent

python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

pip install -r requirements.txt

export OPENAI_API_KEY="your-api-key-here"

streamlit run app.py





## 🖼️ UI Preview
![Chatbot UI](images/image_1.png)

## 🖼️ AgentOps Dashboard
![AgentOps Dashboard](images/agentops_dashbaord.jpeg)