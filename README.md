# Academic Research Assistant 📚

A powerful Streamlit-based application that helps researchers find, analyze, and explore academic papers using AI-powered assistance.

## 🌟 Features

- **Intelligent Query Processing**: Automatically classifies and routes queries to specialized agents
- **Paper Search**: Find relevant research papers from arXiv based on your queries
- **Interactive Q&A**: Ask questions about specific papers and get contextual answers
- **Future Research Directions**: Explore potential research opportunities and gaps in the field
- **User-Friendly Interface**: Clean and intuitive Streamlit-based UI with chat functionality

## 🛠️ Installation

1. Clone the repository:
```bash
git clone git@github.com:shreybhuva/academic-research-assistant.git
cd academic-research-assistant
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up your Google API key:
   - Get a Google API key from the Google Cloud Console
   - Update `config.py` with your API key or set it as an environment variable:
```python
export GOOGLE_API_KEY="your_api_key_here"
```

## 🚀 Usage

1. Start the application:
```bash
streamlit run app.py
```

2. Access the application in your web browser at `http://localhost:8501`

3. Enter your research-related queries in the chat interface:
   - Search for papers: "Find recent papers on deep learning"
   - Ask questions: "What are the key findings in the paper about transformer architectures?"
   - Explore future directions: "What are potential research opportunities in reinforcement learning?"

## 🧩 System Architecture

The application consists of several key components:

### Agents

- **IntentAgent**: Classifies user queries into appropriate categories
- **SearchAgent**: Handles paper search and retrieval from arXiv
- **QAAgent**: Processes questions about specific papers
- **FutureWorksAgent**: Analyzes research trends and suggests future directions

### Core Features

- **Vector Store**: Uses FAISS for efficient similarity search of paper content
- **Embedding**: Utilizes Google's Generative AI embeddings
- **PDF Processing**: Handles PDF download and text extraction
- **Context Management**: Maintains conversation history and paper context

## 📁 Project Structure

```
academic-research-assistant/
├── app.py                 # Main Streamlit application
├── router.py             # Query routing and intent classification
├── config.py             # Configuration and API setup
├── requirements.txt      # Project dependencies
├── agents/
│   ├── __init__.py      # Agent module initialization
│   ├── search_agent.py  # Paper search functionality
│   ├── qa_agent.py      # Question answering functionality
│   └── future_works_agent.py  # Future research analysis
└── papers/              # Directory for temporary paper storage
```

## 🔧 Configuration

The application uses the following dependencies:
- langchain-google-genai
- langchain-community
- arxiv
- pymupdf
- faiss-cpu
- pdfminer.six
- google-generativeai
- streamlit

## ⚠️ Note

- Make sure you have adequate storage space for downloaded papers
- The application requires an active internet connection
- Some features may be limited by API rate limits

## 🔍 Troubleshooting

Common issues and solutions:

1. **API Key Issues**:
   - Ensure your Google API key is properly set
   - Check API quotas and limits

2. **Paper Download Issues**:
   - Verify internet connection
   - Check available disk space
   - Ensure the `papers/` directory exists and is writable

3. **Memory Issues**:
   - Consider reducing the number of papers processed simultaneously
   - Clear the `papers/` directory periodically
