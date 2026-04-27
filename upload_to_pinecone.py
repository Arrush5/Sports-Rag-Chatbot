import os
import time
import re
from dotenv import load_dotenv
from pinecone import Pinecone, ServerlessSpec
from langchain_community.document_loaders import PyPDFLoader
from langchain_core.documents import Document
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_pinecone import PineconeVectorStore

# --- 1. LOAD API KEYS FROM .env ---
# This looks for a .env file in the current directory and loads the variables
load_dotenv() 

# Verify that the keys were loaded successfully
if not os.getenv("GOOGLE_API_KEY") or not os.getenv("PINECONE_API_KEY"):
    raise ValueError("Missing API keys! Please check your .env file.")

# --- 2. SEMANTIC CHUNKING ---
print("Loading and chunking document...")
pdf_path = "sports_encyclopedia.pdf"
loader = PyPDFLoader(pdf_path)
documents = loader.load()

full_text = "\n".join([doc.page_content for doc in documents])
raw_chunks = re.split(r'\n(?=\d{1,3}\.\s)', full_text)

chunks = []
for chunk in raw_chunks:
    clean_text = chunk.strip()
    if len(clean_text) > 20: 
        chunks.append(Document(page_content=clean_text, metadata={"source": "sports_encyclopedia"}))

print(f"Created {len(chunks)} semantic chunks.")

# --- 3. PINECONE INITIALIZATION ---
print("Connecting to Pinecone...")
# Pinecone automatically uses the PINECONE_API_KEY from the environment
pc = Pinecone() 

index_name = "sports-rag-index"
embedding_dimension = 3072 

if index_name not in pc.list_indexes().names():
    print(f"Creating new Pinecone index: '{index_name}'...")
    pc.create_index(
        name=index_name,
        dimension=embedding_dimension,
        metric="cosine", 
        spec=ServerlessSpec(
            cloud="aws",
            region="us-east-1" 
        )
    )
    time.sleep(10)
else:
    print(f"Index '{index_name}' already exists.")

# --- 4. GENERATE EMBEDDINGS & UPLOAD ---
print("Generating Gemini embeddings and uploading to Pinecone. This may take a minute...")

# GoogleGenerativeAIEmbeddings automatically uses the GOOGLE_API_KEY from the environment
embeddings = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001")

vectorstore = PineconeVectorStore.from_documents(
    documents=chunks,
    embedding=embeddings,
    index_name=index_name
)

print("Success! All 100 sports have been successfully embedded and uploaded to Pinecone.")