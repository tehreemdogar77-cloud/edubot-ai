import os
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings

def load_knowledge_base(folder_path: str = "knowledge_base/"):
    documents = []
    for filename in os.listdir(folder_path):
        filepath = os.path.join(folder_path, filename)
        if filename.endswith(".txt"):
            loader = TextLoader(filepath, encoding="utf-8")
            documents.extend(loader.load())
            print(f"Loaded: {filename}")
    return documents

def create_vectorstore(documents):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50
    )
    chunks = splitter.split_documents(documents)
    print(f"Created {len(chunks)} searchable chunks")

    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    vectorstore = FAISS.from_documents(chunks, embeddings)
    print("Vector store ready!")
    return vectorstore

def search_documents(vectorstore, query: str, k: int = 3) -> str:
    results = vectorstore.similarity_search(query, k=k)
    context = "\n\n---\n\n".join([doc.page_content for doc in results])
    return context