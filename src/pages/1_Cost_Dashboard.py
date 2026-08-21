import pandas as pd
import streamlit as st

from src import governance

st.set_page_config(page_title="Cost Dashboard", page_icon="💰", layout="wide")
governance.init_db()

st.title("Cost Dashboard")
st.caption(
    "This app runs entirely on local Ollama — there is no real billing. Costs "
    "below are **illustrative**: what an equivalent call would cost on a typical "
    "paid API, shown for cost-avoidance visibility, not an actual charge. Token "
    "counts are approximated (~4 characters/token), not exact per-model counts."
)

generations = governance.get_events(event_type="generation", limit=500)
retrievals = governance.get_events(event_type="retrieval", limit=500)

if not generations:
    st.info("No generations logged yet — go summarize a PDF on the main page first.")
else:
    gen_df = pd.DataFrame(generations)
    gen_df["timestamp"] = pd.to_datetime(gen_df["timestamp"], unit="s")

    total_cost = gen_df["estimated_cost_usd"].fillna(0).sum()
    total_tokens = (gen_df["input_tokens"].fillna(0) + gen_df["output_tokens"].fillna(0)).sum()
    avg_latency = gen_df["latency_s"].mean()
    success_rate = gen_df["success"].mean() * 100

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total generations", len(gen_df))
    col2.metric("Total estimated cost", f"${total_cost:.4f}")
    col3.metric("Total tokens (est.)", f"{int(total_tokens):,}")
    col4.metric("Success rate", f"{success_rate:.0f}%")

    st.divider()
    st.subheader("Estimated cost over time")
    chart_df = gen_df.set_index("timestamp")[["estimated_cost_usd"]].sort_index()
    st.line_chart(chart_df)

    st.subheader("Recent generations")
    display_df = gen_df[
        ["timestamp", "model", "input_tokens", "output_tokens", "estimated_cost_usd", "latency_s", "success", "error"]
    ].copy()
    display_df.columns = [
        "Time",
        "Model",
        "Input tokens (est.)",
        "Output tokens (est.)",
        "Est. cost ($)",
        "Latency (s)",
        "Success",
        "Error",
    ]
    st.dataframe(display_df, width="stretch")

st.divider()
st.subheader("Governance & audit log — retrieval events")
st.caption(
    "Every retrieval is logged independently of generation, so you can audit "
    "exactly what content was pulled from a document even if generation later failed."
)

if not retrievals:
    st.info("No retrievals logged yet.")
else:
    ret_df = pd.DataFrame(retrievals)
    ret_df["timestamp"] = pd.to_datetime(ret_df["timestamp"], unit="s")
    display_ret = ret_df[["timestamp", "query", "num_chunks", "latency_s"]].copy()
    display_ret.columns = ["Time", "Query", "Chunks retrieved", "Latency (s)"]
    st.dataframe(display_ret, width="stretch")

st.divider()
st.subheader("Enforced governance policies")
st.markdown(
    f"""
- **Max query length**: {governance.MAX_QUERY_CHARS} characters — longer requests are rejected before any pipeline work runs.
- **Rate limit**: {governance.MAX_GENERATIONS_PER_SESSION_PER_MINUTE} generations per minute per session.
- **Illustrative pricing**: ${governance.ILLUSTRATIVE_PRICE_PER_1K_TOKENS} per 1,000 tokens (configurable in `src/governance.py`).
"""
)
