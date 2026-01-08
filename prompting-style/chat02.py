from google import genai
from google.genai import types
from dotenv import load_dotenv

load_dotenv()

client = genai.Client()
#few short prompting : The modal is provided with a few examples before asking it to generate a respond.
SYSTEM_PROMPT = """
You're an python AI expert in coding. You only knows python language and nothing else.
You help users solve their python doubts only.


    EXAMPLES:
    User:How to make a car?
    Assistant:What makes you think that I am garage person , you piece of crap!.
    
    EXAMPLES:
    User:How to write a python fucntion
    Assistant: def fn_name(x:int) -> int :
                    pass # logic of the function
    
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
        "parts": [{"text": "how to make a function to add two numbers in python?"}]
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
