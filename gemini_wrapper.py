from google import genai
from dotenv import dotenv_values

config = dotenv_values(".env")

client = genai.Client(api_key=config["GEMINI_API_KEY"])
response = client.models.generate_content(
    model="gemini-2.0-flash", contents="respond only with the word 'test'"
)
print(response.text)
