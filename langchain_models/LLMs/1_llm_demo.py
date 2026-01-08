from langachain_openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

llm=OpenAI(model="")

result= llm.invoke("What is the capital of India?")
print(result)