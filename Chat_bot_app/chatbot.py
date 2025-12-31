import streamlit as st
from config.settings import DATA_PATH

from modules.Loader import load_documents
from modules.embeddings import get_embedding_model
from modules.vectordb import get_collection, store_documents
from modules.retriever import retrieve_context
from modules.llm_agent import get_answer

st.set_page_config(page_title="Sunbeam ChatBot", layout="centered")
st.title("💬 Sunbeam Website ChatBot")
st.caption("Answers strictly from Sunbeam website")

@st.cache_resource
def initialize():
    docs = load_documents(DATA_PATH)
    embed_model = get_embedding_model()
    collection = get_collection()
    store_documents(collection, docs, embed_model)
    return collection, embed_model

with st.spinner("Loading knowledge base..."):
    collection, embed_model = initialize()

st.success("Knowledge base ready ✅")

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

user_input = st.chat_input("Ask about courses, internships, batches...")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    context = retrieve_context(collection, embed_model, user_input)
    answer = get_answer(context, user_input)

    st.session_state.messages.append({"role": "assistant", "content": answer})
    with st.chat_message("assistant"):
        st.markdown(answer)
