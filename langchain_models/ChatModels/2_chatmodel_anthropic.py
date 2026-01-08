from langchain_anthropic import ChatAnthropic
from dotenv import load_dotenv
load_dotenv()   

chat_model = ChatAnthropic(model="claude-2", temperature=0, max_completion_tokens=500)
response = chat_model.invoke("Hello, how are you?")
print(response.content)