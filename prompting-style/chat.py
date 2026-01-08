from google import genai
from google.genai import types
from dotenv import load_dotenv

load_dotenv()

client = genai.Client()
#zero short prompting

SYSTEM_PROMPT = """
You're an stoneage AI expert in coding. You only knows stone language and nothing else.
You help users solve their stone doubts only.


    INSTRUCTIONS:
    1.Always respond in markdown format.
    2.Always stone the user at beginning. 
"""

history = [
    {
        "role": "user",
        "parts": [{"text": "Hey make a spaceship"}]
    },
    {
        "role": "model",
        "parts": [{"text": "Hi Aman! Nice to meet you. How can I help you today?"}]
    },
    {
        "role": "user",
        "parts": [{"text": "Tell me why I should learn about genai and prompting styles?"}]
    }
]

response = client.models.generate_content_stream(
    model="gemini-2.5-flash",
    contents=history,
    config=types.GenerateContentConfig(
        system_instruction=SYSTEM_PROMPT,
    )
)

for chunk in response:
    print(chunk.text, end="")
