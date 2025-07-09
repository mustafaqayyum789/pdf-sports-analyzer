
if st.button("Analyze with GPT"):
    if openai_api_key:
        with st.spinner("Generating player summaries..."):
            response = openai.ChatCompletion.create(
                model="gpt-4",
                api_key=openai_api_key,
                messages=[
                    {"role": "system", "content": "You are a sports analyst."},
                    {"role": "user", "content": f"Extract structured player performance data and summaries from this text:\n{text}"}
                ]
            )
            analysis = response.choices[0].message.content.strip()
            st.subheader("GPT Analysis")
            st.text_area("Player Summaries", analysis, height=300)
    else:
        st.error("Please enter a valid OpenAI API key.")
