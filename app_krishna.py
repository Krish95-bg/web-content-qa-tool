import streamlit as st
import requests
from bs4 import BeautifulSoup
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.text_splitter import CharacterTextSplitter
from langchain.docstore.document import Document
from langchain.chains import RetrievalQA
from langchain.chat_models import ChatOpenAI
import os

st.set_page_config(page_title="Web Content Q&A Tool", page_icon="🧠")

st.title("🧠 Web Content Q&A Tool")
st.markdown("Enter one or more URLs, and ask questions based on the content scraped from them.")

# Input fields
urls = st.text_area("Enter URLs (comma-separated)", height=100)
question = st.text_input("Ask your question based on the content")

# API Key Input (if not using environment variable)
openai_key = st.text_input("Enter your OpenAI API Key", type="password")
if openai_key:
    os.environ["OPENAI_API_KEY"] = openai_key

# Function to extract text from a URL
def extract_text_from_url(url):
    try:
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")
        paragraphs = [p.get_text() for p in soup.find_all("p")]
        return " ".join(paragraphs)
    except Exception as e:
        return f"Error fetching content from {url}: {str(e)}"

# Function to create vector store
def create_vector_store(texts):
    splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    docs = [Document(page_content=t) for t in splitter.split_text(texts)]
    embeddings = OpenAIEmbeddings()
    return FAISS.from_documents(docs, embeddings)

# Generate answer
if st.button("Get Answer"):
    if not urls or not question:
        st.warning("Please enter both URLs and a question.")
    elif not openai_key:
        st.warning("Please enter your OpenAI API key.")
    else:
        with st.spinner("Processing URLs and fetching answer..."):
            combined_text = ""
            for url in urls.split(","):
                combined_text += extract_text_from_url(url.strip()) + " "

            if combined_text.strip() == "":
                st.error("No valid content found in the provided URLs.")
            else:
                vectorstore = create_vector_store(combined_text)
                qa_chain = RetrievalQA.from_chain_type(
                    llm=ChatOpenAI(temperature=0),
                    retriever=vectorstore.as_retriever()
                )
                answer = qa_chain.run(question)
                st.success("Answer generated successfully!")
                st.markdown(f"**Answer:** {answer}")
