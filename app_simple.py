
import streamlit as st
import fitz  # PyMuPDF
import re
import pandas as pd

st.set_page_config(page_title="Simple Sports PDF Extractor")

st.title("📄 Simple Sports PDF Player Analyzer")
st.write("Upload a sports match report PDF and extract simple performance summaries.")

uploaded_file = st.file_uploader("Upload PDF", type=["pdf"])

if uploaded_file:
    st.success("PDF uploaded successfully!")

    # Extract text
    with fitz.open(stream=uploaded_file.read(), filetype="pdf") as doc:
        text = ""
        for page in doc:
            text += page.get_text()

    st.subheader("📃 Extracted Text")
    with st.expander("View Text"):
        st.text(text)

    # Pattern example: "Match 1: Messi scored 2 goals and made 1 assist."
    pattern = r"Match\s*\d+:\s*(.*?)\s+scored\s+(\d+)\s+goals?(?:\s+and\s+made\s+(\d+)\s+assists?)?"

    matches = re.findall(pattern, text, re.IGNORECASE)
    data = []

    for match in matches:
        player = match[0]
        goals = match[1]
        assists = match[2] if match[2] else "0"
        data.append({"Player": player, "Goals": int(goals), "Assists": int(assists)})

    if data:
        df = pd.DataFrame(data)
        st.subheader("📊 Player Performance Summary")
        st.dataframe(df)
    else:
        st.warning("⚠️ No structured performance data found. Try using format like: 'Match 1: Messi scored 2 goals and made 1 assist.'")
