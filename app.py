
import streamlit as st
import fitz  # PyMuPDF
import openai
import os

st.title("📊 Sports Match PDF Analyzer with GPT")
st.write("Upload a sports match report PDF and get player performance summaries.")

# Load OpenAI API key from environment or user input
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    api_key = st.text_input("Enter your OpenAI API key:", type="password")
    if not api_key:
        st.warning("Please enter your OpenAI API key to continue.")
        st.stop()
openai.api_key = api_key

# File uploader
uploaded_file = st.file_uploader("Upload PDF", type=["pdf"])
if uploaded_file:
    # Read text from PDF
    with fitz.open(stream=uploaded_file.read(), filetype="pdf") as doc:
        full_text = ""
        for page in doc:
            full_text += page.get_text()

    st.subheader("📄 Extracted Text")
    with st.expander("View Full Text"):
        st.write(full_text)

    if st.button("Analyze with GPT"):
        with st.spinner("🔍 Generating player performance summaries..."):
            prompt = f"Extract structured player performance summaries from this sports match report:

{full_text}

"
            try:
                response = openai.ChatCompletion.create(
                    model="gpt-4",
                    messages=[
                        {"role": "system", "content": "You are a helpful assistant that summarizes player performances."},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.3
                )
                summary = response["choices"][0]["message"]["content"]
                st.subheader("🏅 Player Performance Summary")
                st.write(summary)
            except Exception as e:
                st.error(f"An error occurred: {e}")
