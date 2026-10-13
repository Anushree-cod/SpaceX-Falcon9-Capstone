from pathlib import Path
import pandas as pd
import streamlit as st
import plotly.express as px

st.set_page_config(page_title="SpaceX Falcon 9 Explorer", layout="wide")
st.title("SpaceX Falcon 9 Launch Explorer")
st.caption("Run notebooks/01_data_collection.ipynb first to download public API data.")
data_path = Path(__file__).resolve().parents[1] / "data" / "spacex_launches_raw.csv"
if not data_path.exists():
    st.warning("No data CSV found. Run the data-collection notebook first.")
    st.stop()
df = pd.read_csv(data_path)
df["landing_success"] = df["landing_success"].map({"True": 1, "False": 0, True: 1, False: 0})
known = df[df["landing_success"].notna()].copy()
c1, c2, c3 = st.columns(3)
c1.metric("Launch records", f"{len(df):,}")
c2.metric("Known landing outcomes", f"{len(known):,}")
c3.metric("Observed landing success", f"{known['landing_success'].mean():.1%}" if len(known) else "N/A")
if len(known):
    by_site = known.groupby("launchpad_name", dropna=False)["landing_success"].mean().reset_index()
    by_site["success_rate_pct"] = 100 * by_site["landing_success"]
    st.plotly_chart(px.bar(by_site, x="launchpad_name", y="success_rate_pct",
                           title="Observed landing success by launch site",
                           labels={"launchpad_name":"Launch site","success_rate_pct":"Success rate (%)"}),
                    use_container_width=True)
    st.dataframe(known[["flight_number","name","date_utc","launchpad_name","orbit","landing_success"]].sort_values("flight_number", ascending=False),
                 use_container_width=True)
st.caption("Descriptive dashboard only; small samples and confounding can make unadjusted site comparisons misleading.")
