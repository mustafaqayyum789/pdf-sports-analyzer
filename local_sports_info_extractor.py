
import streamlit as st
import fitz  # PyMuPDF
from transformers import pipeline

st.set_page_config(page_title="Local Sports PDF Extractor", layout="centered")
st.title("📄 Local Sports PDF Extractor")
st.markdown("Upload a sports match PDF and extract basic information using a local NLP model.")

@st.cache_resource
def load_pipeline():
    return pipeline("zero-shot-classification", model="facebook/bart-large-mnli")

classifier = load_pipeline()

def extract_text_from_pdf(uploaded_file):
    text = ""
    doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
    for page in doc:
        text += page.get_text()
    return text

uploaded_file = st.file_uploader("Upload your sports match PDF", type=["pdf"])

if uploaded_file:
    with st.spinner("Extracting and analyzing text..."):
        pdf_text = extract_text_from_pdf(uploaded_file)
        st.success("Text extracted successfully!")

        st.subheader("Extracted Text")
        with st.expander("View Text"):
            st.text_area("Text", value=pdf_text, height=300)

        candidate_labels = ["player name", "goals", "assists", "match date", "team names", "score", "yellow cards", "red cards"]

        if st.button("Extract Key Info"):
            result = classifier(pdf_text, candidate_labels)
            st.subheader("🏅 Detected Key Information")
            for label, score in zip(result['labels'], result['scores']):
                st.write(f"**{label.capitalize()}**: {score*100:.2f}% confidence")
