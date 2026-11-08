"""PromoIQ optional Streamlit prototype. Run with: streamlit run app.py."""
from __future__ import annotations
import csv
import io
import re
import tempfile
from pathlib import Path

import streamlit as st

from src.core import write_json
from src.parser import parse_file
from run_pipeline import process_one
from src.presenter import flatten_promo

st.set_page_config(page_title="PromoIQ | Screenplay to Promos", page_icon="🎬", layout="wide")
st.title("PromoIQ")
st.caption("Script-grounded 20–60-second promo discovery • Kuku AI Generalist, Problem 1")
st.info("Screenplay timestamps are estimates until video is checked. All rankings are heuristic and editor approval is required.")
st.markdown("Upload timestamped screenplays to detect first-three-second hooks, unresolved endings and source episode cut points. No video editing, text overlays or music are generated.")

mode=st.radio("Input",["Try fictional demo", "Upload your screenplay (.txt)"],horizontal=True)
files=[]
if mode == "Upload your screenplay (.txt)":
    files=st.file_uploader("Upload one or more screenplay text files",type=["txt"],accept_multiple_files=True)
else:
    st.caption("Original fictional sample: a railway dispatcher confronts a saboteur. This demo is not a Kuku source episode.")

if st.button("Find promo candidates",type="primary"):
    try:
        with tempfile.TemporaryDirectory(prefix="promoiq_app_") as td:
            tmp=Path(td)
            selected=[]
            if mode == "Try fictional demo":
                selected=[Path(__file__).resolve().parent/"examples"/"episode-099-original-demo.txt"]
            else:
                if not files:
                    st.error("Upload at least one screenplay text file first.")
                    st.stop()
                if len(files)>50:
                    st.error("Up to 50 screenplays per run.")
                    st.stop()
                for i,f in enumerate(files):
                    data=f.getvalue()
                    if len(data)>2_000_000:
                        st.error(f"File too large: {f.name} (2 MB maximum per file)")
                        st.stop()
                    text=data.decode("utf-8-sig")
                    m=re.search(r"^EPISODE NUMBER:\s*Episode\s+(\d+)",text,re.I|re.M)
                    if not m:
                        st.error(f"{f.name}: missing EPISODE NUMBER: Episode N")
                        st.stop()
                    eid=f"{int(m.group(1)):03d}"
                    p=tmp/f"episode-{eid}-upload-{i}.txt"
                    p.write_text(text,encoding="utf-8")
                    selected.append(p)
            rows=[]
            episodes=[]
            for path in selected:
                episode,validation=parse_file(path)
                eid=episode.pop("_episode_id")
                processed=tmp/"processed"/f"episode_{eid}.json"
                write_json(processed,episode)
                result,qa=process_one(processed,tmp/"outputs",top_n=4,force=True,gate=True)
                episodes.append((eid,len(result["promos"]),len(qa.get("issues",[]))))
                for p in result["promos"]:
                    rows.append(flatten_promo(p))
            rows.sort(key=lambda r: -float(r["score"]))
            st.session_state["promo_rows"]=rows
            st.session_state["episode_count"]=len(episodes)
    except (ValueError,KeyError,OSError,UnicodeDecodeError) as exc:
        st.error(f"Cannot process screenplay: {exc}")
        st.stop()

if "promo_rows" in st.session_state:
    rows=st.session_state["promo_rows"]
    a,b,c=st.columns(3)
    a.metric("Episodes",st.session_state.get("episode_count",0))
    b.metric("Selected promos",len(rows))
    c.metric("Duration target","20–60s")
    if not rows:
        st.warning("No script-grounded candidate passed the conservative quality gate. Try another script; the tool does not invent a promo.")
    else:
        st.dataframe(rows,use_container_width=True,hide_index=True)
        data=io.StringIO()
        w=csv.DictWriter(data,fieldnames=rows[0].keys())
        w.writeheader()
        w.writerows(rows)
        st.download_button("Download ranked candidates (CSV)",data.getvalue().encode("utf-8"),file_name="promoiq_ranked.csv",mime="text/csv")
st.caption("No LLM calls are required for this demo. Human editorial and actual-footage checks remain pending.")
