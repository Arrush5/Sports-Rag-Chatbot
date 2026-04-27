import re
from langchain_community.document_loaders import PyPDFLoader
from langchain_core.documents import Document

# 1. Load the clean PDF
pdf_path = "sports_encyclopedia.pdf"
loader = PyPDFLoader(pdf_path)
documents = loader.load()

# Combine all pages into one giant string of text
full_text = "\n".join([doc.page_content for doc in documents])

# 2. Semantic Split using Regular Expressions
# This regex looks for a newline followed by 1-3 digits, a dot, and a space (e.g., "\n1. ", "\n42. ", "\n100. ")
# It splits the text right BEFORE the number, keeping the number attached to the sport!
raw_chunks = re.split(r'\n(?=\d{1,3}\.\s)', full_text)

# 3. Clean up the chunks and convert them back into LangChain Document objects
chunks = []
for chunk in raw_chunks:
    clean_text = chunk.strip()
    # Ensure it's an actual sport entry and not a random blank space
    if len(clean_text) > 20: 
        chunks.append(Document(page_content=clean_text))

print(f"Successfully split the document into {len(chunks)} semantic chunks!")
print("-" * 50)
print("SAMPLE CHUNK (Chunk #42 - Bowling):")
print("-" * 50)
# Remember, arrays start at 0, so chunk 41 is the 42nd sport
print(chunks[41].page_content)