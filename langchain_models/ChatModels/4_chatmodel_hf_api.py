import os
from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint
from dotenv import load_dotenv

load_dotenv()

# 1. Setup the Endpoint with a model that DOES NOT need permission
# Zephyr-7B is free, fast, and ungated.
llm = HuggingFaceEndpoint(
    repo_id="HuggingFaceH4/zephyr-7b-beta",
    task="text-generation",
    max_new_tokens=512,
    do_sample=False,
    repetition_penalty=1.03,
)

# 2. Wrap it for Chat
chat_model = ChatHuggingFace(llm=llm)

# 3. Run it
try:
    print("Asking Zephyr...")
    result = chat_model.invoke("What is the capital of India?")
    print(result.content)
except Exception as e:
    print(f"Error: {e}")