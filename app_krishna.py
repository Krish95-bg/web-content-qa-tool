import streamlit as st
import requests
from bs4 import BeautifulSoup
import google.generativeai as genai


st.set_page_config(page_title="Web Content Q&A Tool", page_icon="🧠")
st.title("🧠 Web Content Q&A Tool with Gemini")
st.markdown("Enter URLs and ask questions based on the scraped content.")


urls = st.text_area("Enter URLs (comma-separated)", height=100)
question = st.text_input("Ask your question based on the content")
gemini_key = st.text_input("Enter your Gemini API Key", type="password")

if gemini_key:
    genai.configure(api_key=gemini_key)


def extract_text_from_url(url):
    try:
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")
        paragraphs = [p.get_text() for p in soup.find_all("p")]
        return " ".join(paragraphs)
    except Exception as e:
        return f"Error fetching content from {url}: {str(e)}"


if st.button("Get Answer"):
    if not urls or not question:
        st.warning("Please enter both URLs and a question.")
    elif not gemini_key:
        st.warning("Please enter your Gemini API key.")
    else:
        with st.spinner("Fetching and processing..."):
            combined_text = ""
            for url in urls.split(","):
                combined_text += extract_text_from_url(url.strip()) + " "

            if combined_text.strip() == "":
                st.error("No valid content found.")
            else:
                model_name = "models/gemini-1.5-pro-latest"
                try:
                    model = genai.GenerativeModel(model_name=model_name)
                    response = model.generate_content(
                        f"Context: {combined_text}\n\nQuestion: {question}"
                    )
                    st.success("✅ Answer generated successfully!")
                    st.markdown(f"**Answer:** {response.text}")
                except Exception as e:
                    st.error(f"❌ Gemini Error: {e}")
