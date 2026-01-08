from langchain_google_genai import ChatGoogleGemini
from dotenv import load_dotenv

load_dotenv()
chat_model = ChatGoogleGemini(model="gemini-1.5-pro", temperature=0, max_completion_tokens=500)
response = chat_model.invoke("Hello, how are you?")
print(response.content)