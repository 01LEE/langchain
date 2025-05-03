# .env import
# from dotenv import load_dotenv
from langchain_openai import OpenAI # 최신 버전
import os

# load_dotenv()
llm = OpenAI()

#streamlit import
import streamlit as st

st.title("인공지능 시인")
content = st.text_input('시의 주제를 제시해주세요.')

if st.button('시 만들기'):
    with st.spinner('시 작성 중...'):
        result = llm.invoke( content + "을 주제로 한 다섯 줄 시를 써줘 ")
        st.write(result)
