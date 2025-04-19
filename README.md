# 🧠 Web Content Q&A Tool

This is a Streamlit web app that allows users to input one or more URLs and ask questions based on the content scraped from those pages. The tool uses LangChain and OpenAI's language models to answer questions using information retrieved from the given web pages.

---

## 🚀 Features

- Scrapes text content from given URLs
- Splits and embeds text using LangChain
- Uses FAISS for vector storage and retrieval
- Answers questions using OpenAI's GPT model via LangChain's `RetrievalQA`

---

## 📦 Requirements

Install dependencies using:

pip install -r requirements.txt
---

## 💡 Usage

Run the app locally using:


streamlit run app.py
You will need an OpenAI API Key to generate answers.

---

## 🌐 Deployed App

👉 [Click here to access the app](https://bgweb-content-app-tool-pwmrvyuf2hylbqd7p3kdu6.streamlit.app/) *(replace with your Streamlit app link)*

---

## ⚠️ Note

If you exceed your OpenAI quota, you can use a dummy response to test the app UI.
