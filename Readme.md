🔎 Groq Research Agent

An AI-powered research automation agent that leverages Groq-accelerated LLaMA, real-time web search, and academic knowledge sources including ArXiv and Wikipedia. Designed to deliver fast, structured, and verified research insights with formal academic explanations.

🚀 Features

->Groq High-Speed LLM Inference using Gemma-2 9B for rapid, low-latency responses
->Multi-source retrieval via DuckDuckGo Search, ArXiv API, and Wikipedia API
->Research-grade response generation with structured, detailed, and 200+ word academic output
->Interactive Web UI built with Streamlit for seamless user experience
->Query grounding through automated tool calling and context expansion
->Session-based conversation persistence in the UI

🧠 Tech Stack
Component	Technology
LLM Inference	Groq + LangChain
Search & Retrieval	DuckDuckGo Search API, Wikipedia API, ArXiv API
Framework	Streamlit
Tooling	LangChain Tools, Callback Streaming
Security	.env-based API Key configuration
📦 Installation
git clone https://github.com/ShivangGit123/Groq_Research_Agent.git
cd Groq_Research_Agent

pip install -r requirements.txt


Create a .env file in the project directory and add:

GROQ_API_KEY=your_api_key_here

▶️ Run the Application
streamlit run app.py


Open the browser link shown in the terminal to access the UI.

🛠️ How It Works

User submits a query through Chat UI

LLM decides whether to:

Search the web

Query ArXiv

Use Wikipedia

Results are fetched and summarized into structured, academic-style output (200+ words)

Previous messages remain visible for continuous conversation context

📌 Example Use Cases

Academic research assistance

Literature review automation

Technology and scientific topic exploration

Fact-grounded content generation

🔐 Authentication

The Groq API key is required.
Input it securely in the Streamlit sidebar.
No key is stored on the server.

🖼 Screenshot (Optional)

Add UI screenshot here

🤝 Contributing

Pull requests and feature improvements are welcome.
Feel free to open issues for bug reporting or suggestions.

📜 License

This project is open-source under the MIT License.
