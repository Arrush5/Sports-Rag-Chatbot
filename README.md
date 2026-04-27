# Global Sports RAG Chatbot

An intelligent, streaming Retrieval-Augmented Generation (RAG) chatbot that acts as an encyclopedia for 100 different sports. Ask it about the rules, origins, player counts, and famous countries of any sport, and watch it stream the answers in real-time.

Built with **Pinecone**, **Streamlit**, and **Google's Gemini 1.5 Flash**.

## Features

* **Custom Knowledge Base:** Contains highly structured data on 100 global sports, programmatically generated into a clean PDF.
* **Semantic Chunking:** Uses Regex-based semantic chunking to ensure the vector database holds perfectly encapsulated data for each sport, eliminating context loss.
* **High-Dimensional Embeddings:** Utilizes Google's latest `gemini-embedding-001` model (3072 dimensions) for hyper-accurate retrieval.
* **Serverless Vector Storage:** Hosted on Pinecone's serverless architecture for blazing-fast semantic search.
* **Real-time Streaming:** Powered by Gemini 1.5 Flash, the bot streams responses letter-by-letter for a seamless conversational experience.
* **Bulletproof Extraction:** Includes custom logic to safely handle complex LLM streaming chunks and multimodal outputs.

## Tech Stack

* **Frontend:** [Streamlit](https://streamlit.io/)
* **LLM Orchestrator:** Google Gemini Flash via [LangChain](https://python.langchain.com/)
* **Embeddings:** Google `gemini-embedding-001`
* **Vector Database:** [Pinecone](https://www.pinecone.io/) (Serverless)
* **Document Processing:** `fpdf`, `pypdf`, `langchain-text-splitters`
* **Environment Management:** `python-dotenv`

## Project Structure
```text
Sports-Rag-Chatbot/
    ├── sports_details.py                      
    ├── chunk_data.py       
    ├── upload_to_pinecone.py           
    ├── app.py                   
    └── README.md
```

## Prerequisites

Before you begin, ensure you have the following API keys:
1. **Google Gemini API Key:** Get it from [Google AI Studio](https://aistudio.google.com/)
2. **Pinecone API Key:** Get it from [Pinecone](https://www.pinecone.io/)

## Installation & Setup

**1. Clone the repository and navigate to the project directory**
```bash
git clone https://github.com/Arrush5/Sports-Rag-Chatbot.git
cd Sports-Rag_Chatbot.git
```
**2. Set up a virtual environment (Optional but recommended)**
```bash
python -m venv .venv
# On Windows:
.venv\Scripts\activate
# On Mac/Linux:
source .venv/bin/activate
```
**3. Install the required dependencies**
```bash
pip install fpdf langchain langchain-community langchain-text-splitters pypdf pinecone-client langchain-pinecone langchain-google-genai streamlit python-dotenv
```
**4. Configure your Environment Variables**

Create a .env file in the root directory and add your API keys:
```code snippet
GOOGLE_API_KEY=your_google_api_key_here
PINECONE_API_KEY=your_pinecone_api_key_here
```
## Usage Guide
Follow these steps in order to build the brain of the AI and launch the app:

**Step 1: Generate the Knowledge Base**

Run the script to generate the 100-sport PDF.
```bash
python sports_details.py
```
**Step 2: Upload to Pinecone**

Run the script to chunk the PDF, embed the data, and create your Pinecone vector index. (Note: This may take a minute as it creates a new 3072-dimension index named sports-rag-index).
```bash
python upload_to_pinecone.py
```
**Step 3: Launch the Chatbot**

Start the Streamlit web server to interact with your AI.
```bash
streamlit run app.py
```
Navigate to http://localhost:8501 in your browser. Ask the bot questions like:
- "What are the rules of Ultimate Frisbee?"
- "Where did Surfing originate?"
- "How many players are on a water polo team?"
## How the RAG Pipeline Works
1. User Input: The user asks a question via the Streamlit UI.
2. Retrieval: The question is embedded using Google's embedding model and sent to Pinecone to find the top 3 most relevant chunks (sports).
3. Augmentation: The retrieved text chunks are injected into a strict prompt, instructing the AI to only use the provided context.
4. Generation: Gemini Flash processes the prompt and streams the highly accurate, fact-based answer back to the user interface.