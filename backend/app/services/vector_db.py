# backend/app/services/vector_db.py
from sentence_transformers import SentenceTransformer
import chromadb

model = SentenceTransformer("all-MiniLM-L6-v2")
client = chromadb.Client()

collection = client.get_or_create_collection("jobs")

def match_jobs(parsed):
    user_skills = parsed["skills"]
    query_embedding = model.encode(" ".join(user_skills)).tolist()

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=5
    )

    matches = []
    gaps = []

    # Ambil dari metadatas bukan documents
    for metadata in results["metadatas"][0]: 
        job_title = metadata["title"]
        # Misal skills disimpan sebagai string dipisah koma di metadata
        job_skills = metadata["skills"].split(",") 

        overlap = set(user_skills) & set(job_skills)
        missing = set(job_skills) - set(user_skills)

        score = len(overlap) / len(job_skills) if len(job_skills) > 0 else 0

        matches.append({"role": job_title, "score": score})
        gaps.append({"role": job_title, "missing_skills": list(missing)})

    return matches, gaps