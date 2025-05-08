

import streamlit as st
from dotenv import load_dotenv
load_dotenv()

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter 
from langchain_openai import OpenAIEmbeddings
from langchain.vectorstores import Chroma

from langchain_openai import ChatOpenAI
from langchain.chains import RetrievalQA
import tempfile
import os

uploaded_file = st.file_uploader("Choose a file")
st.write("---")
#Loader

def pdf_to_document(uploaded_file):
    temp_dir = tempfile.TemporaryDirectory()
    temp_filepath = os.path.join(temp_dir.name, uploaded_file.name)
    with open(temp_filepath, "wb") as f:
        f.write(uploaded_file.getvalue()) 
    loader=PyPDFLoader("unsu.pdf")
    pages = loader.load_and_split()
    return pages

if uploaded_file is not None:
    pages = pdf_to_document(uploaded_file)
    pass

    #Split
    text_splitter = RecursiveCharacterTextSplitter (
        chunk_size=100,
        chunk_overlap=20,
        length_function=len,
        is_separator_regex=False,
    )
    texts = text_splitter.split_documents(pages)

    #Embedding
    embeddings_model = OpenAIEmbeddings()

    #load it into Chroma
    db = Chroma.from_documents(texts, embeddings_model)

    #Qustions
    st.header("PDF에 질문해보세요.")
    qustion = st.text_input("질문을 적어주세요.")

    if st.button("질문"):
        with st.spinner("기다려주세요."):
            llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
            qa_chain = RetrievalQA.from_chain_type(
                llm=llm,
                chain_type="stuff",
                retriever=db.as_retriever(),  # OK, 단 더 복잡한 질문 확장 가능
            )
            result = qa_chain(qustion)
            st.write(result["result"])




