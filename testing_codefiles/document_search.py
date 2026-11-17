import os
import json 
from pathlib import Path  
import numpy
from openai import OpenAI
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

client = OpenAI(base_url=os.getenv("URL"), api_key=os.getenv("API_KEY"))

EMBED_MODEL = os.getenv("EMBED_MODEL")
PROJECT_ROOT = Path(__file__).resolve().parent.parent
KB_FOLDER = PROJECT_ROOT/os.getenv("KB_FOLDER", "knowledge_base")
VECTOR_STORE_FILE = PROJECT_ROOT/os.getenv("VECTOR_STORE_FILE", "knowledge_base/vector_store.json")

def get_embedding(text) :
    response = client.embeddings.create(
        model = EMBED_MODEL,
        input = text
    )
    
    return response.data[0].embedding

def get_similarity(a, b) :
    return numpy.dot(a, b) / (numpy.linalg.norm(a) * numpy.linalg.norm(b))

def load_documents(folder=KB_FOLDER) :
    documents = []

    for name in sorted(os.listdir(folder)) :
        if name.endswith(".txt") :
            path = os.path.join(folder, name)

            with open(path, "r", encoding="utf-8") as f :
                documents.append(
                    {
                        "name" : name,
                        "text" : f.read(),
                    }
                )
            
    return documents

def embed_documents(documents) :
    for doc in documents :
        embed = get_embedding(doc["text"])
        doc["embed"] = embed

    return documents 

def search_query(query, chunks, top_k=3) :
    results = []
    query_embed = get_embedding(query)

    for chunk in chunks :
        results.append(
            {
                "name" : chunk["filename"],
                "text" : chunk["text"],
                "id" : chunk["id"],
                "similarity" : get_similarity(chunk["embed"], query_embed)
            }
        )
    
    results.sort(key = lambda r : r["similarity"], reverse = True)

    return results[:top_k]

def get_chunks() :
    docs = load_documents()

    chunks = []

    for doc in docs :
        for chunk in doc["text"].split("\n\n") :
            chunk = chunk.strip()
            if chunk :
                chunks.append(
                    {
                        "filename" : doc["name"],
                        "text" : chunk
                    }
                )

    return chunks

def embed_chunks() :
    chunks = get_chunks()
    for i, chunk in enumerate(chunks) :
        chunk["id"] = i 
        chunk["embed"] = get_embedding(chunk["text"])

    return chunks

def save_vector_store(chunks) :
    vector = {
        "model" : EMBED_MODEL,
        "created_on" : datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "chunks" : chunks
    }
    with open(VECTOR_STORE_FILE, "w", encoding = "utf-8") as f :
        json.dump(vector, f, indent = 4)

def load_vector_store():
    with open(VECTOR_STORE_FILE, "r", encoding = "utf-8") as f :
        return json.load(f)["chunks"]
        
def test(chunks) :
    ans = search_query("python", chunks)

    for a in ans :
        #print("\n", a["name"], "-", f"{a["similarity"]:.2f}", "-", a["text"], "\n")
        print("\n", a["name"], "-", f"{a["similarity"]:.2f}", "\n")

if __name__ == "__main__" :
    if os.path.exists(VECTOR_STORE_FILE) :
        chunks = load_vector_store()
        print(f"Loaded {len(chunks)} chunks from the vector store file {VECTOR_STORE_FILE}")
    else :
        chunks = embed_chunks()
        save_vector_store(chunks)
        print(f"Saved {len(chunks)} chunks to the vector store file {VECTOR_STORE_FILE}")

    test(chunks)
    