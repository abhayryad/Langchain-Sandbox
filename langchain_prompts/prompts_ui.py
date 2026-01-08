import streamlit as st
from dotenv import load_dotenv
from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint # 1. Updated Imports
from langchain_core.prompts import load_prompt

load_dotenv()

# 2. Configure the Hugging Face Endpoint (Zephyr)
llm = HuggingFaceEndpoint(
    repo_id="HuggingFaceH4/zephyr-7b-beta",
    task="text-generation",
    max_new_tokens=512,
    do_sample=False,
    repetition_penalty=1.03,
)

# 3. Wrap it in ChatHuggingFace
# This allows it to work exactly like ChatOpenAI (outputting message objects)
model = ChatHuggingFace(llm=llm)

st.header('Research Tool')

paper_input = st.selectbox(
    "Select Research Paper Name", 
    ["Attention Is All You Need", "BERT: Pre-training of Deep Bidirectional Transformers", "GPT-3: Language Models are Few-Shot Learners", "Diffusion Models Beat GANs on Image Synthesis"]
)

style_input = st.selectbox(
    "Select Explanation Style", 
    ["Beginner-Friendly", "Technical", "Code-Oriented", "Mathematical"]
) 

length_input = st.selectbox(
    "Select Explanation Length", 
    ["Short (1-2 paragraphs)", "Medium (3-5 paragraphs)", "Long (detailed explanation)"]
)

# Ensure 'template.json' exists in your folder!
try:
    template = load_prompt('template.json')
except:
    st.error("Error: 'template.json' file not found. Please create it.")
    st.stop()

if st.button('Summarize'):
    with st.spinner('Generating summary...'):
        try:
            chain = template | model
            result = chain.invoke({
                'paper_input': paper_input,
                'style_input': style_input,
                'length_input': length_input
            })
            st.write(result.content)
        except Exception as e:
            st.error(f"An error occurred: {e}")