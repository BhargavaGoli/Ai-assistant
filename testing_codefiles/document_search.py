import os 
import numpy
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(base_url=os.getenv("URL"), api_key=os.getenv("API_KEY"))

EMBED_MODEL = os.getenv("EMBED_MODEL")
KB_FOLDER = os.getenv("KB_FOLDER")

def get_embedding(text) :
    response = client.embeddings.create(
        model = EMBED_MODEL,
        input = text
    )
    
    return response.data[0].embedding

def get_similarity(a, b) :
    return f"{numpy.dot(a, b) / (numpy.linalg.norm(a) * numpy.linalg.norm(b)):.2f}"

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

def search_query(query, documents, top_k=3) :
    results = []
    query_embed = get_embedding(query)

    for doc in documents :
        results.append(
            {
                "name" : doc["name"],
                "similarity" : get_similarity(doc["embed"], query_embed)
            }
        )
    
    results.sort(key = lambda r : r["similarity"], reverse = True)

    return results[:top_k]

documents = load_documents()
documents = embed_documents(documents)

ans = search_query("how are goals set", documents)

for a in ans :
    print(a["name"], "-", a["similarity"])