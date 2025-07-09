# Streamlit app to upload sports PDF and extract text stats

import streamlit as st
import fitz  # PyMuPDF
import re

st.set_page_config(page_title="Sports PDF Stats Extractor", layout="centered")
st.title("🏀 Sports PDF Stats Extractor")
st.markdown("Upload your sports document (PDF) and extract key statistics.")

# File uploader
uploaded_file = st.file_uploader("Upload PDF Document", type=["pdf"])

if uploaded_file is not None:
    st.success("PDF uploaded successfully!")

    # Open PDF with PyMuPDF
    doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
    full_text = ""
    for page in doc:
        full_text += page.get_text()

    # Display extracted raw text
    with st.expander("📄 View Extracted Text"):
        st.text_area("Raw Text", value=full_text, height=300)

    # Basic stats extraction logic (e.g., player name, score, assists)
    st.subheader("📊 Extracted Statistics")

    # Example regex to extract lines with scores
    score_lines = re.findall(r"\b([A-Za-z ]+):\s*(\d+).*", full_text)

    if score_lines:
        st.write("### Player Stats:")
        st.table(score_lines)
    else:
        st.warning("No obvious stats found. Please upload a well-formatted sports PDF.")
