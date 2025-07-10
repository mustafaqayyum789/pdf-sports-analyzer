
import streamlit as st
import spacy.cli
import spacy
import fitz  # PyMuPDF

# Ensure the spaCy model is available
spacy.cli.download("en_core_web_sm")

# Load spaCy model
@st.cache_resource
def load_model():
    return spacy.load("en_core_web_sm")

nlp = load_model()

st.title("Local Sports PDF Extractor")
st.subheader("Upload a sports match PDF and extract basic information using a local NLP model.")

uploaded_file = st.file_uploader("Upload PDF", type=["pdf"])

def extract_text_from_pdf(file):
    doc = fitz.open(stream=file.read(), filetype="pdf")
    text = ""
    for page in doc:
        text += page.get_text()
    return text

if uploaded_file:
    text = extract_text_from_pdf(uploaded_file)
    st.success("PDF text extracted successfully!")

    if st.button("Analyze Text"):
        with st.spinner("Analyzing text with spaCy..."):
            doc = nlp(text)
            people = set(ent.text for ent in doc.ents if ent.label_ == "PERSON")
            orgs = set(ent.text for ent in doc.ents if ent.label_ == "ORG")
            dates = set(ent.text for ent in doc.ents if ent.label_ == "DATE")
            st.subheader("Extracted Information")
            st.write("**People (likely players):**", people)
            st.write("**Organizations (teams):**", orgs)
            st.write("**Dates:**", dates)
