import streamlit as st
import pandas as pd
import time
import altair as alt

from database import create_table, fetch_all, insert, clear_data
from processor import process_texts
from search import search
from export import export_csv
from sentiment import analyze, analyzer

create_table()

st.set_page_config(page_title="Parallel Text Processor", layout="wide")

st.title("🚀 Parallel Text Handling Processor")
st.caption("Large file support + analytics + performance tracking")

tab1, tab2, tab3 = st.tabs(["📊 Dashboard", "🔍 Search", "📁 Export"])

# 🔥 ADD THIS (DO NOT REMOVE)
if "search_results" not in st.session_state:
    st.session_state.search_results = []


# ================= HELPER ================= #
def create_dataframe(data):
    if not data:
        return None
    return pd.DataFrame(data, columns=["ID","Text","Score","Sentiment","Time"])


# ================= DASHBOARD ================= #
with tab1:

    st.header("📊 Processing Dashboard")

    if st.button("🗑️ Reset Data"):
        clear_data()
        st.success("Data cleared")
        st.rerun()

    st.divider()

    uploaded_files = st.file_uploader(
        "Upload ANY File (TXT, CSV, Excel, JSON, etc.)",
        accept_multiple_files=True
    )

    texts = []
    MAX_LIMIT = 50000

    if uploaded_files:
        st.success(f"{len(uploaded_files)} file(s) uploaded")

        for file in uploaded_files:
            try:
                if file.size == 0:
                    st.warning(f"{file.name} is empty ⚠️")
                    continue

                if file.size > 200 * 1024 * 1024:
                    st.warning(f"{file.name} too large, skipping")
                    continue

                if file.name.endswith(".txt"):
                    content = file.read().decode("utf-8", errors="ignore")
                    texts += content.replace("\n", ".").split(".")

                elif file.name.endswith(".csv"):
                    for chunk in pd.read_csv(file, chunksize=5000):
                        for row in chunk.values:
                            texts.extend([str(x) for x in row if pd.notna(x)])
                        if len(texts) >= MAX_LIMIT:
                            break

                elif file.name.endswith(".xlsx"):
                    df = pd.read_excel(file)
                    texts += df.astype(str).stack().tolist()

                else:
                    content = file.read().decode("utf-8", errors="ignore")
                    texts += content.split("\n")

            except:
                st.warning(f"Error reading {file.name}")

    texts = [t.strip() for t in texts if t.strip()]

    if len(texts) > MAX_LIMIT:
        texts = texts[:MAX_LIMIT]
        st.warning(f"Limited to {MAX_LIMIT} records")

    if not texts and uploaded_files:
        st.error("⚠️ No valid data extracted from files")

    st.write("📊 Total Extracted Records:", len(texts))


    # ================= PROCESS ================= #
    if st.button("🚀 Start Processing"):

        if not texts:
            st.error("No valid data found")
            st.stop()

        progress = st.progress(0)

        with st.spinner("Processing data... Please wait ⏳"):

            start = time.time()

            batch_size = 5000
            output = {"normal_time": 0, "parallel_time": 0, "cores_used": 0}

            for i in range(0, len(texts), batch_size):
                batch = texts[i:i + batch_size]
                result = process_texts(batch)

                output["normal_time"] += result["normal_time"]
                output["parallel_time"] += result["parallel_time"]
                output["cores_used"] = result["cores_used"]

                # 🔥 ADD THESE (Milestone-4 aggregation)
                if "original_count" in result:
                    output["original_count"] = output.get("original_count", 0) + result["original_count"]
                    output["optimized_count"] = output.get("optimized_count", 0) + result["optimized_count"]
                    output["optimize_time"] = output.get("optimize_time", 0) + result["optimize_time"]

                progress.progress(min((i + batch_size) / len(texts), 1.0))

            end = time.time()

        st.success("Processing Completed ✅")

        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Normal Time", round(output["normal_time"], 2))
        col2.metric("Parallel Time", round(output["parallel_time"], 2))
        col3.metric("CPU Cores", output["cores_used"])
        col4.metric("Total Time", round(end - start, 2))

        # 🔥 MILESTONE 4 DISPLAY
        if "original_count" in output:
            col5, col6, col7 = st.columns(3)
            col5.metric("Original Records", output["original_count"])
            col6.metric("Optimized Records", output["optimized_count"])
            col7.metric("Optimization Time", round(output["optimize_time"], 2))

        st.info("Parallel is slower for small data, faster for large datasets.")

    st.divider()


    # ================= MANUAL ================= #
    st.subheader("✍️ Manual Text Analysis")

    if "manual_result" not in st.session_state:
        st.session_state.manual_result = None

    user_text = st.text_area("Enter any text")

    col1, col2 = st.columns(2)
    analyze_btn = col1.button("Analyze Text")
    save_btn = col2.button("💾 Save Result")

    if analyze_btn:
        if not user_text.strip():
            st.warning("Enter some text")
        else:
            score, sentiment, pos, neg = analyze(user_text)

            st.session_state.manual_result = {
                "text": user_text,
                "score": score,
                "sentiment": sentiment,
                "pos": pos,
                "neg": neg
            }

    if st.session_state.manual_result:

        r = st.session_state.manual_result

        words = r["text"].split()
        neutral = max(len(words) - (r["pos"] + r["neg"]), 0)

        st.success("Analysis Completed")

        st.metric("Score", r["score"])
        st.metric("Sentiment", r["sentiment"])

        chart_df = pd.DataFrame({
            "Type": ["Positive", "Negative", "Neutral"],
            "Count": [r["pos"], r["neg"], neutral]
        })

        st.bar_chart(chart_df.set_index("Type"))

        pie = alt.Chart(chart_df).mark_arc().encode(
            theta="Count",
            color="Type"
        )
        st.altair_chart(pie, use_container_width=True)

    if save_btn:
        if st.session_state.manual_result:
            r = st.session_state.manual_result
            insert(r["text"], r["score"], r["sentiment"])
            st.success("Saved ✅")
            st.session_state.manual_result = None

    st.divider()


    # ================= DATABASE ================= #
    data = fetch_all()
    df = create_dataframe(data)

    if df is not None:

        st.subheader("📊 Stored Data")

        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Total", len(df))
        col2.metric("Positive", (df["Sentiment"] == "Positive").sum())
        col3.metric("Negative", (df["Sentiment"] == "Negative").sum())
        col4.metric("Neutral", (df["Sentiment"] == "Neutral").sum())

        sent_counts = df["Sentiment"].value_counts().reindex(
            ["Positive","Negative","Neutral"], fill_value=0
        )

        st.bar_chart(sent_counts)

        pie_df = sent_counts.reset_index()
        pie_df.columns = ["Sentiment", "Count"]

        st.altair_chart(
            alt.Chart(pie_df).mark_arc().encode(
                theta="Count",
                color="Sentiment"
            ),
            use_container_width=True
        )

        total_pos = 0
        total_neg = 0
        total_neutral = 0

        for text in df["Text"]:
            _, _, p, n = analyze(text)
            total_pos += p
            total_neg += n

            for w in text.lower().split():
                if w and w not in analyzer.lexicon:
                    total_neutral += 1

        colA, colB, colC = st.columns(3)
        colA.metric("Total Positive Words", total_pos)
        colB.metric("Total Negative Words", total_neg)
        colC.metric("Total Neutral Words", total_neutral)

        word_df = pd.DataFrame({
            "Type": ["Positive", "Negative", "Neutral"],
            "Count": [total_pos, total_neg, total_neutral]
        })

        st.subheader("📊 Overall Word Distribution")

        st.bar_chart(word_df.set_index("Type"))

        st.altair_chart(
            alt.Chart(word_df).mark_arc().encode(
                theta="Count",
                color="Type"
            ),
            use_container_width=True
        )

        st.dataframe(df, use_container_width=True)


# ================= SEARCH ================= #
with tab2:

    st.header("🔍 Smart Search")

    keyword = st.text_input("Keyword")
    sentiment = st.selectbox("Sentiment", ["All", "Positive", "Negative", "Neutral"])
    min_score = st.slider("Score", -5, 5, 0)

    if st.button("Search"):

        if not keyword:
            st.warning("Enter keyword")
            st.stop()

        selected = None if sentiment == "All" else sentiment

        score, sent, _, _ = analyze(keyword)

        if selected and sent != selected:
            st.error(f"'{keyword}' is {sent}")
            st.stop()

        results = search(keyword, selected, min_score)

        st.session_state.search_results = results

        df = create_dataframe(results)

        if df is not None:
            st.success(f"Found {len(df)} results")
            st.dataframe(df, use_container_width=True)
        else:
            st.warning("No results found")


# ================= EXPORT ================= #
with tab3:

    st.header("📁 Export Data")

    option = st.selectbox("Export Type", ["Database Data", "Search Results"])

    if st.button("Generate CSV"):

        if option == "Database Data":
            file = export_csv()

        else:
            if not st.session_state.search_results:
                st.warning("No search results available")
                st.stop()

            df = pd.DataFrame(
                st.session_state.search_results,
                columns=["ID","Text","Score","Sentiment","Time"]
            )

            file = "search_results.csv"
            df.to_csv(file, index=False)

        with open(file, "rb") as f:
            st.download_button("Download CSV", f, file_name=file)
