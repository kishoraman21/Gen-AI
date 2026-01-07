import tiktoken

enc = tiktoken.encoding_for_model("gpt-4o")

text = "hello , this is genai class"

tokens = enc.encode(text)

print("Tokens: ", tokens)

decodedTokens = enc.decode(tokens)

print("Decoded tokens", decodedTokens)