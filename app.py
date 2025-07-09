import streamlit as st
import fitz  # PyMuPDF
import openai
import os

st.set_page_config(page_title="GPT Sports Analyzer", layout="centered")

st.title("📊 GPT-Powered Sports PDF Analyzer")
st.markdown("Upload a sports match PDF and extract detailed player summaries using **GPT-4**.")

# Sidebar for OpenAI API Key
st.sidebar.title("🔐 API Configuration")
api_key = st.sidebar.text_input("Enter your OpenAI API Key", type="password")

# Upload PDF
uploaded_file = st.file_uploader("Upload a match report PDF", type=["pdf"])

if uploaded_file and api_key:
    with st.spinner("📄 Reading and extracting text..."):
        doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
        extracted_text = ""
        for page in doc:
            extracted_text += page.get_text()

    if extracted_text.strip():
        st.success("✅ Text extracted successfully!")
        with st.expander("🔍 View Extracted Text"):
            st.text_area("Extracted Text", extracted_text, height=200)

        prompt = f"""Extract detailed performance summaries for each player from the following match report text.
Format the output like:
Player: Lionel Messi
- Goals: 2
- Assists: 1
- Notable moments: Scored winning goal in 78th minute.

Match Report:
"""
{extracted_text}
"""
"""

        with st.spinner("🤖 Generating player summaries..."):
            try:
                openai.api_key = api_key
                response = openai.ChatCompletion.create(
                    model="gpt-4",
                    messages=[
                        {"role": "system", "content": "You are a helpful assistant that extracts structured player performance summaries from sports match reports."},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.5,
                    max_tokens=1500
                )
                summary = response.choices[0].message.content
                st.subheader("📋 Player Performance Summary")
                st.markdown(summary)
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
    else:
        st.warning("⚠️ Could not extract any text from the PDF.")
else:
    st.info("👈 Upload a PDF and enter your API key to begin.")
