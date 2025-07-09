import streamlit as st
import fitz  # PyMuPDF
import re

st.set_page_config(page_title="Sports PDF Stats Extractor", layout="centered")
st.title("🏀 Sports PDF Stats Extractor")
st.markdown("Upload your sports document (PDF) and extract key statistics.")

uploaded_file = st.file_uploader("Upload PDF Document", type=["pdf"])

if uploaded_file is not None:
    st.success("PDF uploaded successfully!")

    doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
    full_text = ""
    for page in doc:
        full_text += page.get_text()

    with st.expander("📄 View Extracted Text"):
        st.text_area("Raw Text", value=full_text, height=300)

    st.subheader("📊 Extracted Statistics")

    # Improved pattern for sports stat lines
    matches = re.findall(r"([A-Z][a-z]+(?:\s[A-Z][a-z]+)?)\s*[:\-]?\s*(\d+)\s*(goals?|assists?|shots?)", full_text, re.IGNORECASE)

    if matches:
        st.write("### Player Stats:")
        st.table(matches)
    else:
        st.warning("No clear player stats found. Please upload a document with names and numbers like 'Messi: 3 goals'.")
