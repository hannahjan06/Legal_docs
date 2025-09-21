import streamlit as st
import os
from PyPDF2 import PdfReader
from transformers import pipeline
import numpy as np



# 1. Load Hugging Face model


qa_pipeline = pipeline("question-answering", model="deepset/roberta-base-squad2")



# 2. Function to read PDF


def read_pdf(file):
    pdf = PdfReader(file)
    text = ""
    for page in pdf.pages:
        text += page.extract_text() or ""
    return text



# 3. Split text into chunks


def chunk_text(text, chunk_size=500):
    words = text.split()
    return [" ".join(words[i:i+chunk_size]) for i in range(0, len(words), chunk_size)]



# 4. Find best chunk for query


def find_best_chunk(chunks, query):
    # Very simple scoring: which chunk has most words from the query
    query_words = set(query.lower().split())
    best_score, best_chunk = -1, ""
    for chunk in chunks:
        score = sum(1 for word in query_words if word in chunk.lower())
        if score > best_score:
            best_score, best_chunk = score, chunk
    return best_chunk



# 5. Ask Hugging Face model


def ask_ai_local(question, context):
    result = qa_pipeline(question=question, context=context)
    return result["answer"]



# 6. Streamlit UI


st.title("Legal Document Q&A Chatbot (Hugging Face)")

uploaded_file = st.file_uploader("Upload a legal PDF", type="pdf")

if uploaded_file is not None:
    st.success(" File uploaded successfully!")
    text = read_pdf(uploaded_file)
    chunks = chunk_text(text)

    query = st.text_input("Ask a question about the document:")
    if query:
        best_chunk = find_best_chunk(chunks, query)
        if best_chunk.strip():
            answer = ask_ai_local(query, best_chunk)
            st.subheader("Answer:")
            st.write(answer)
        else:
            st.warning("⚠ No relevant section found in the document.")