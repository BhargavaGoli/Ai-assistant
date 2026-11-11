import os
import numpy
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    base_url = os.getenv("URL"),
    api_key = os.getenv("API_KEY")
)

def get_similarity(A, B) :
    sim = numpy.dot(A, B)
    lenA = numpy.linalg.norm(A)
    lenB = numpy.linalg.norm(B)

    return sim / (lenA * lenB)

def get_embedding(text) :
    response = client.embeddings.create(
        model = os.getenv("EMBED_MODEL"),
        input = text
    )
    return response.data[0].embedding
    
text = ["python is easy to learn", "He is a good boy", "python is easy to write"]
emb = [0] * len(text)

for i, t in enumerate(text) :
    emb[i] = get_embedding(t)

print(f"{get_similarity(emb[0], emb[1]):.2f}")
print(f"{get_similarity(emb[0], emb[2]):.2f}")