
import streamlit as st
import fitz  # PyMuPDF
import openai
import os

st.set_page_config(page_title="Sports PDF Analyzer", layout="centered")
st.title("📊 Sports PDF Match Analyzer (GPT-4 Powered)")

# Input OpenAI API key
api_key = st.text_input("Enter your OpenAI API Key:", type="password")
if not api_key:
    st.warning("Please enter your OpenAI API key to proceed.")
    st.stop()

openai.api_key = api_key

uploaded_file = st.file_uploader("Upload a sports match report PDF", type=["pdf"])

if uploaded_file:
    st.success("✅ PDF uploaded successfully!")

    # Extract text from PDF
    text = ""
    with fitz.open(stream=uploaded_file.read(), filetype="pdf") as doc:
        for page in doc:
            text += page.get_text()

    with st.expander("📄 View Extracted Text"):
        st.text_area("Extracted Text", value=text, height=300)

    if st.button("Analyze with GPT"):
        with st.spinner("Generating player summaries..."):
            prompt = f"Extract structured player performance summaries from this sports match report:

{text}

Format like:
- Player Name: Summary of actions, goals, assists, key moments."
            try:
                response = openai.ChatCompletion.create(
                    model="gpt-4",
                    messages=[
                        {"role": "system", "content": "You are a sports analyst assistant."},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.5,
                    max_tokens=1000
                )
                result = response['choices'][0]['message']['content']
                st.subheader("🏅 Player Summaries")
                st.text_area("Summaries", result, height=300)
            except Exception as e:
                st.error(f"❌ Error: {e}")
