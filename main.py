# .env import
# from dotenv import load_dotenv
# import os
import streamlit as st

from langchain_community.llms import CTransformers

# load_dotenv() -> switched to ctransformers
llm = CTransformers(
    model="llama-2-7b-chat.ggmlv3.q5_0.bin",
    model_type="llama"
)

# streamlit UI
st.title("AI Poet")
content = st.text_input('Please enter the topic of the poem.')

if st.button('Generate Poem'):
    with st.spinner('Generating poem...'):
        result = llm.invoke(content + " is the topic. Write poem.")
        st.write(result)
