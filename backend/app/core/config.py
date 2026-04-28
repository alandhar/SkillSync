# backend/app/core/config.py
import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")

    AZURE_STORAGE_CONNECTION_STRING = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
    AZURE_BLOB_CONTAINER = os.getenv("AZURE_BLOB_CONTAINER")

    CHROMA_DB_DIR = os.getenv("CHROMA_DB_DIR", "../data/vector_store")

    GITHUB_TOKEN = os.getenv("GITHUB_TOKEN", "")

    MODEL_NAME = os.getenv("MODEL_NAME", "llama3-70b-8192")


settings = Settings()