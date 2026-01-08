from google import genai
from google.genai import types
import json
from dotenv import load_dotenv

load_dotenv()

client = genai.Client()
# Chain of Thought : The modal is encouraged to break down reasoning step by step before arriving at a final solution.
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

# history = [
#     {
#         "role": "user",
#         "parts": [{"text": "what is 5/2 "}]
#     }
# ]

# response = client.models.generate_content_stream(
#     model="gemini-2.5-flash",
#     contents=history,
#     config=types.GenerateContentConfig(
#         system_instruction=SYSTEM_PROMPT,
#     )
# )

# for chunk in response:
#     print("\n🤖:", chunk.text, end="")

messages = [{"role": "model", "parts": [{"text": SYSTEM_PROMPT}]}]

while True:
    query = input("\nAsk a question: ")
    messages.append({"role": "user", "parts": [{"text": query}]})

    while True:
        response = client.models.generate_content_stream(
            model="gemini-2.5-flash",
            contents=messages,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                response_schema={
                    "type": "object",
                    "properties": {
                        "step": {"type": "string"},
                        "content": {"type": "string"},
                    },
                    "required": ["step", "content"],
                },
            ),
        )

        full_response = ""
        for chunk in response:
            if chunk.text:
                full_response += chunk.text

        cleaned = (
            full_response.replace("```json", "")
            .replace("```", "")
            .strip()
        )

        try:
            parsed = json.loads(cleaned)
        except Exception:
            print(" Model returned non-JSON:", full_response)
            break

        step = parsed.get("step")
        content = parsed.get("content")

        print(f"🧠 {step}: {content}")

        if step == "result":
            break

        messages.append({
            "role": "model",
            "parts": [{"text": full_response}]
        })

    print("\n Done! Ask me another question.")