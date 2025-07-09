import streamlit as st
import fitz  # PyMuPDF
import re
import pandas as pd

st.set_page_config(page_title="Advanced Sports PDF Stats Analyzer", layout="wide")
st.title("🏆 Advanced Sports PDF Stats Analyzer")
st.markdown("Upload a sports PDF and extract structured player performance insights.")

uploaded_file = st.file_uploader("Upload PDF Document", type=["pdf"])

if uploaded_file is not None:
    st.success("✅ PDF uploaded successfully!")

    doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
    full_text = ""
    for page in doc:
        full_text += page.get_text()

    with st.expander("📄 View Raw Extracted Text"):
        st.text_area("Raw PDF Text", value=full_text, height=300)

    st.subheader("📊 Extracted Player Performance Insights")

    # Enhanced pattern to detect player names with detailed performance
    # Example match: "Lionel Messi scored 2 goals and made 1 assist."
    patterns = re.findall(
        r"([A-Z][a-z]+(?:\s[A-Z][a-z]+)+).*?(scored\s(\d+)\sgoals?|made\s(\d+)\sassists?|had\s(\d+)\sshots?)",
        full_text, re.IGNORECASE
    )

    # Process into structured DataFrame
    players = {}
    for name, detail, goals, assists, shots in patterns:
        if name not in players:
            players[name] = {"Goals": 0, "Assists": 0, "Shots": 0}
        if goals:
            players[name]["Goals"] += int(goals)
        if assists:
            players[name]["Assists"] += int(assists)
        if shots:
            players[name]["Shots"] += int(shots)

    if players:
        df = pd.DataFrame.from_dict(players, orient="index").reset_index()
        df.columns = ["Player", "Goals", "Assists", "Shots"]
        st.dataframe(df)
    else:
        st.warning("No structured player stats found. Please upload a document with clear performance phrases like 'Messi scored 2 goals'.")
