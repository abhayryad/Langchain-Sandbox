from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()
chat_model = ChatOpenAI(model="gpt-4", temperature=0, max_completion_tokens=500)
response = chat_model.invoke("Hello, how are you?")
print(response.content) 