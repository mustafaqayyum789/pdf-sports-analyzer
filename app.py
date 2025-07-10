import streamlit as st
import spacy
import fitz  # PyMuPDF

st.set_page_config(page_title="Sports Info Extractor", layout="wide")
st.title("📄 Sports PDF Extractor (Local spaCy Model)")

@st.cache_resource
def load_model():
    return spacy.load("en_core_web_sm")

def extract_text_from_pdf(uploaded_file):
    doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
    text = ""
    for page in doc:
        text += page.get_text()
    return text

def extract_entities(text, nlp):
    doc = nlp(text)
    players = [ent.text for ent in doc.ents if ent.label_ == "PERSON"]
    orgs = [ent.text for ent in doc.ents if ent.label_ == "ORG"]
    scores = [sent.text for sent in doc.sents if any(x in sent.text.lower() for x in ["goal", "assist", "scored", "points", "match"])]
    return players, orgs, scores

uploaded_file = st.file_uploader("Upload a sports match PDF file", type=["pdf"])

if uploaded_file:
    st.success("✅ File uploaded successfully.")
    nlp = load_model()
    text = extract_text_from_pdf(uploaded_file)
    players, orgs, scores = extract_entities(text, nlp)

    st.subheader("📌 Extracted Information")
    st.write("### 🧍 Players")
    st.write(players if players else "No players found.")
    st.write("### 🏟️ Organizations/Teams")
    st.write(orgs if orgs else "No teams or organizations found.")
    st.write("### 📊 Match Performance")
    st.write(scores if scores else "No performance-related info found.")