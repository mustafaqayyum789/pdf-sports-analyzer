
import streamlit as st
import fitz  # PyMuPDF
import re
import pandas as pd

st.set_page_config(page_title="General Sports Match Analyzer", layout="centered")

st.title("🏆 General Sports Match Analyzer")
st.markdown("Upload a sports match PDF (e.g., football, cricket, tennis) with player narratives to extract meaningful stats and summaries.")

uploaded_file = st.file_uploader("📄 Upload Match Report (PDF)", type=["pdf"])

def extract_text_from_pdf(file):
    doc = fitz.open(stream=file.read(), filetype="pdf")
    text = ""
    for page in doc:
        text += page.get_text()
    return text

def parse_general_stats(text):
    # Pattern 1: Match X: Player scored Y goals and Z assists.
    pattern_1 = r"Match\s*(\d+):\s*([\w\s]+?)\s+scored\s+(\d+)\s+goals?(?:\s+and\s+made\s+(\d+)\s+assists?)?"

    # Pattern 2: Player had X shots and scored in Yth minute.
    pattern_2 = r"([\w\s]+?)\s+had\s+(\d+)\s+\w+\s+shots?\s+and\s+scored\s+in\s+the\s+(\d+)(?:st|nd|rd|th)?\s+minute"

    results = []

    for match, player, goals, assists in re.findall(pattern_1, text, re.IGNORECASE):
        results.append({
            "Match": int(match),
            "Player": player.strip(),
            "Goals": int(goals),
            "Assists": int(assists) if assists else 0,
            "Shots": None,
            "Minute Scored": None
        })

    for player, shots, minute in re.findall(pattern_2, text, re.IGNORECASE):
        results.append({
            "Match": None,
            "Player": player.strip(),
            "Goals": 1,
            "Assists": 0,
            "Shots": int(shots),
            "Minute Scored": int(minute)
        })

    return pd.DataFrame(results)

if uploaded_file:
    st.success("✅ PDF uploaded successfully!")
    text = extract_text_from_pdf(uploaded_file)

    with st.expander("📝 View Extracted Text"):
        st.write(text)

    df = parse_general_stats(text)

    if not df.empty:
        st.markdown("### 📊 Extracted Player Stats")
        st.dataframe(df)

        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button("⬇️ Download CSV", csv, "player_stats.csv", "text/csv")
    else:
        st.warning("⚠️ No structured stats found. Try using patterns like:
'Match 1: Messi scored 2 goals and made 1 assist.'")
