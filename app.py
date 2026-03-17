import streamlit as st
from utils import read_uploaded_file
from ingest import ingest_document
from rag import run_rag

st.set_page_config(page_title="Endee RAG Assistant", page_icon="🤖", layout="wide")

st.title("🤖 Endee RAG Assistant")
st.caption("Upload documents, store embeddings in Endee, and ask grounded questions.")

with st.sidebar:
    st.header("Upload Documents")
    uploaded_files = st.file_uploader(
        "Choose PDF, TXT, or MD files",
        type=["pdf", "txt", "md"],
        accept_multiple_files=True
    )
    category = st.text_input("Category label", value="general")

    if st.button("Ingest into Endee", use_container_width=True):
        if not uploaded_files:
            st.warning("Please upload at least one file.")
        else:
            total_inserted = 0
            details = []

            with st.spinner("Reading, chunking, embedding, and upserting..."):
                for file in uploaded_files:
                    try:
                        text = read_uploaded_file(file)
                        result = ingest_document(file.name, text, category=category)
                        total_inserted += result["inserted"]
                        details.append(f"{file.name}: {result['inserted']} chunks")
                    except Exception as e:
                        details.append(f"{file.name}: failed - {e}")

            st.success(f"Ingestion complete. Inserted {total_inserted} chunks.")
            for d in details:
                st.write("- ", d)

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

query = st.text_input("Ask a question about your uploaded documents")

col1, col2 = st.columns([2, 1])

if query:
    with st.spinner("Searching Endee and generating answer..."):
        answer, results = run_rag(query)

    st.session_state.chat_history.append({"q": query, "a": answer, "r": results})

with col1:
    st.subheader("Answer")
    if st.session_state.chat_history:
        latest = st.session_state.chat_history[-1]
        st.write(latest["a"])
    else:
        st.info("Upload documents and ask a question to begin.")

with col2:
    st.subheader("Top Retrieved Chunks")
    if st.session_state.chat_history:
        latest = st.session_state.chat_history[-1]
        for i, item in enumerate(latest["r"], start=1):
            meta = item.get("meta", {})
            st.markdown(f"**{i}. {meta.get('source', 'unknown')}**")
            st.write(f"Similarity: {item.get('similarity', 0)}")
            st.write(meta.get("text", "")[:350] + "...")
            st.divider()

st.subheader("Chat History")
for item in reversed(st.session_state.chat_history):
    with st.expander(item["q"]):
        st.write(item["a"])