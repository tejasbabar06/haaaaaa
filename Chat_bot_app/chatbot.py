import streamlit as st
import tempfile
import os

from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet

from config.settings import DATA_PATH
from modules.Loader import load_documents
from modules.embeddings import get_embedding_model
from modules.vectordb import get_collection, store_documents
from modules.retriever import retrieve_context
from modules.llm_agent import get_answer



PDF_THRESHOLD = 800  


st.set_page_config(page_title="Sunbeam ChatBot", layout="centered")
st.title("Sunbeam AI Assistant")
st.caption("Answers strictly from Sunbeam website")



if "messages" not in st.session_state:
    st.session_state.messages = []

if "latest_long_answer" not in st.session_state:
    st.session_state.latest_long_answer = None

if "pdf_path" not in st.session_state:
    st.session_state.pdf_path = None



if st.button("➕ New Chat", type="primary"):
    st.session_state.messages = []
    st.session_state.latest_long_answer = None
    st.session_state.pdf_path = None
    st.rerun()


def create_pdf(text: str, filename="Sunbeam_Answer.pdf"):
    temp_dir = tempfile.gettempdir()
    file_path = os.path.join(temp_dir, filename)

    doc = SimpleDocTemplate(file_path)
    styles = getSampleStyleSheet()
    story = []

    for line in text.split("\n"):
        story.append(Paragraph(line, styles["Normal"]))

    doc.build(story)
    return file_path



@st.cache_resource
def initialize():
    docs = load_documents(DATA_PATH)
    embed_model = get_embedding_model()
    collection = get_collection()
    store_documents(collection, docs, embed_model)
    return collection, embed_model


with st.spinner("Loading knowledge base..."):
    collection, embed_model = initialize()


for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])


user_input = st.chat_input("Ask about sunbeam...")

if user_input:
    st.session_state.messages.append(
        {"role": "user", "content": user_input}
    )
    with st.chat_message("user"):
        st.markdown(user_input)

    context = retrieve_context(collection, embed_model, user_input)
    answer = get_answer(context, user_input)

    st.session_state.messages.append(
        {"role": "assistant", "content": answer}
    )

    with st.chat_message("assistant"):
        st.markdown(answer)

    
    if len(answer) > PDF_THRESHOLD:
        st.session_state.latest_long_answer = answer
    else:
        st.session_state.latest_long_answer = None
        st.session_state.pdf_path = None



if st.session_state.latest_long_answer:

    st.write("")  # spacing

    if st.button("📄 Save this answer as PDF", type="secondary"):
        st.session_state.pdf_path = create_pdf(
            st.session_state.latest_long_answer
        )



if st.session_state.pdf_path:
    with open(st.session_state.pdf_path, "rb") as f:
        st.download_button(
            label="⬇️ Download PDF",
            data=f,
            file_name="Sunbeam_Answer.pdf",
            mime="application/pdf",
            type="primary"
        )
