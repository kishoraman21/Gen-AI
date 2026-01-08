from google import genai
from google.genai import types
import json
from dotenv import load_dotenv

load_dotenv()

client = genai.Client()
#Chain of Thought : The modal is encouraged to break down reasoning step by step before arriving at a final solution. 
SYSTEM_PROMPT = """
    You're are an helpful AI assistant who is specialized in resolving user query.
    For the given user input, analyze the input and break down the problem step by step.
    
    The steps are: You get a user input , you analyze, you think , you think again , and think for several times and then return the output with an explanation.
    
    Follow the steps in sequence that is "analyse","think", "output", "validate" and finally "result".
    
  Rules:
    1. Respond ONLY in strict JSON as per schema.
    2. Perform one step at a time.
    3. Think step-by-step.

    
   Example:
    Input: what is 2+2
    Output: {"step": "analyse", "content": "User is asking a basic arithmetic question."}
    Output: {"step": "think", "content": "I should add 2 and 2."}
    Output: {"step": "output", "content": "4"}
    Output: {"step": "validate", "content": "4 is correct."}
    Output: {"step": "result", "content": "2+2 = 4."}
     
"""

history = [
    {
        "role": "user",
        "parts": [{"text": "what is 5/2 "}]
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
    print("\n🤖:", chunk.text, end="")
