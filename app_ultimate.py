import streamlit as st
import fitz  # PyMuPDF
import re
import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO

st.set_page_config(page_title="Ultimate Sports Stats Analyzer", layout="wide")
st.title("🏆 Ultimate Sports PDF Player Analyzer")

uploaded_file = st.file_uploader("Upload Sports PDF Document", type=["pdf"])

# Sample player profile images (would normally be from a DB or API)
player_images = {
    "Lionel Messi": "https://upload.wikimedia.org/wikipedia/commons/b/b8/Messi_vs_Nigeria_2018.jpg",
    "Cristiano Ronaldo": "https://upload.wikimedia.org/wikipedia/commons/8/8c/Cristiano_Ronaldo_2018.jpg",
    "Kylian Mbappe": "https://upload.wikimedia.org/wikipedia/commons/a/a8/Kylian_Mbapp%C3%A9_2019.jpg"
}

if uploaded_file is not None:
    st.success("✅ PDF uploaded successfully!")

    doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
    full_text = ""
    for page in doc:
        full_text += page.get_text()

    with st.expander("📄 View Extracted Text"):
        st.text_area("Raw Text", value=full_text, height=300)

    st.subheader("📊 Player Performance by Match")

    # Match per game (e.g. Match 1: Messi scored 2 goals)
    matches = re.findall(
        r"(Match\s\d+):\s*([A-Z][a-z]+(?:\s[A-Z][a-z]+)+).*?(scored\s(\d+)\sgoals?|made\s(\d+)\sassists?|had\s(\d+)\sshots?)",
        full_text, re.IGNORECASE
    )

    match_stats = []
    for match_id, name, _, goals, assists, shots in matches:
        match_stats.append({
            "Match": match_id,
            "Player": name,
            "Goals": int(goals) if goals else 0,
            "Assists": int(assists) if assists else 0,
            "Shots": int(shots) if shots else 0
        })

    if match_stats:
        df = pd.DataFrame(match_stats)

        st.sidebar.header("🔍 Filter Options")
        player_filter = st.sidebar.multiselect("Select Player(s)", df["Player"].unique())
        match_filter = st.sidebar.multiselect("Select Match(es)", df["Match"].unique())

        filtered_df = df.copy()
        if player_filter:
            filtered_df = filtered_df[filtered_df["Player"].isin(player_filter)]
        if match_filter:
            filtered_df = filtered_df[filtered_df["Match"].isin(match_filter)]

        st.dataframe(filtered_df)

        st.subheader("🧾 Player Match Summaries")
        for i, row in filtered_df.iterrows():
            st.markdown(f"- **{row['Match']}** – {row['Player']} scored {row['Goals']} goal(s), made {row['Assists']} assist(s), and had {row['Shots']} shot(s).")

            if row["Player"] in player_images:
                st.image(player_images[row["Player"]], width=150, caption=row["Player"])

        # CSV Export
        csv = filtered_df.to_csv(index=False).encode('utf-8')
        st.download_button("📥 Download Match Stats as CSV", csv, "match_stats.csv", "text/csv")

        # Chart: Goals per Match
        st.subheader("📈 Goals per Match")
        pivot = filtered_df.pivot_table(index="Match", columns="Player", values="Goals", aggfunc="sum").fillna(0)
        st.bar_chart(pivot)

        # Simulate PDF export (actual styled PDF requires reportlab or weasyprint)
        st.subheader("🖨️ Export Summary (PDF-style)")
        st.markdown("_(PDF generation is simulated below. True styled PDF would need external libraries.)_")
        pdf_preview = ""
        for i, row in filtered_df.iterrows():
            pdf_preview += f"{row['Match']} - {row['Player']} - {row['Goals']} Goals, {row['Assists']} Assists, {row['Shots']} Shots\n"
        st.text_area("📄 PDF Summary Preview", pdf_preview.strip(), height=200)

    else:
        st.warning("⚠️ No match-based performance found. Try using 'Match 1: Messi scored 2 goals' format.")
