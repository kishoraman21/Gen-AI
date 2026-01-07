from dotenv import load_dotenv

from google import genai


load_dotenv()

client = genai.Client()

result = client.models.embed_content(
        model="gemini-embedding-001",
        contents="What is the need of the genai?")

print("Embedings:",result.embeddings)
[embedding_obj] = result.embeddings
embedding_length = len(embedding_obj.values)

print(f"Length of embedding: {embedding_length}")