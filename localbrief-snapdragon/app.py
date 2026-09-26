import os
import time
from pathlib import Path

import streamlit as st

from core.local_llm import generate_pack
from core.transcribe import transcribe_audio

st.set_page_config(page_title="LocalBrief", page_icon="LB", layout="wide")

st.markdown("""
<style>
.block-container {max-width: 1120px; padding-top: 2rem;}
.small {color:#667085; font-size:0.9rem;}
.hero {padding: 10px 0 22px 0;}
.card {border:1px solid #e6e8ec; border-radius:14px; padding:16px; background:#fff;}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="hero"><h1>LocalBrief</h1><div class="small">Private lecture & meeting notes, designed for Snapdragon-powered Windows PCs.</div></div>', unsafe_allow_html=True)

model_path = os.getenv("LOCALBRIEF_LLM_MODEL", "").strip()
whisper_ready = bool(os.getenv("LOCALBRIEF_WHISPER_COMMAND", "").strip())

with st.sidebar:
    st.subheader("Runtime")
    mode = st.radio("Mode", ["Demo / text", "Snapdragon / local model"], index=0)
    if mode == "Snapdragon / local model":
        st.caption("Model assets are loaded from your local machine. No cloud API is required by this app layer.")
        st.write("LLM model:", "configured" if model_path else "not configured")
        st.write("Whisper bridge:", "configured" if whisper_ready else "not configured")
    st.divider()
    st.caption("Tip: use a 30-60 second sample for a fast demo.")

left, right = st.columns([1, 1])

with left:
    st.subheader("1. Get the words")
    source = st.radio("Input", ["Paste transcript", "Upload transcript (.txt)", "Upload audio (.wav/.mp3/.m4a)"], horizontal=False)
    transcript = ""
    if source == "Paste transcript":
        transcript = st.text_area("Transcript", height=270, placeholder="Paste a lecture or meeting transcript here...")
    elif source == "Upload transcript (.txt)":
        f = st.file_uploader("Choose a transcript", type=["txt"])
        if f:
            transcript = f.read().decode("utf-8", errors="ignore")
    else:
        f = st.file_uploader("Choose an audio file", type=["wav", "mp3", "m4a"])
        if f and st.button("Transcribe locally"):
            temp = Path("recording_input")
            temp.write_bytes(f.getbuffer())
            try:
                with st.spinner("Running local speech recognition..."):
                    transcript = transcribe_audio(str(temp))
                st.session_state["transcript"] = transcript
            finally:
                try: temp.unlink()
                except Exception: pass
        transcript = st.session_state.get("transcript", transcript)

    st.text_area("Current transcript", value=transcript, height=180, key="transcript_view")

with right:
    st.subheader("2. Turn it into something useful")
    if st.button("Create note pack", type="primary", use_container_width=True):
        if not transcript.strip():
            st.error("Add a transcript first.")
        else:
            with st.spinner("Building the note pack..."):
                t0 = time.perf_counter()
                pack = generate_pack(transcript, model_path if mode.startswith("Snapdragon") else "")
                elapsed = time.perf_counter() - t0
            st.session_state["pack"] = pack
            st.session_state["elapsed"] = elapsed

    pack = st.session_state.get("pack")
    if pack:
        st.markdown("**Summary**")
        st.write(pack.get("summary", ""))
        st.markdown("**Key points**")
        for item in pack.get("key_points", []):
            st.write("- " + item)

if "pack" in st.session_state:
    pack = st.session_state["pack"]
    st.divider()
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown("**Action items**")
        for item in pack.get("action_items", []):
            st.write("- " + item)
    with c2:
        st.markdown("**Glossary**")
        for item in pack.get("glossary", []):
            if isinstance(item, dict):
                st.write(f"**{item.get('term','Term')}** - {item.get('meaning','')}")
            else:
                st.write("- " + str(item))
    with c3:
        st.markdown("**5 quick questions**")
        for i, q in enumerate(pack.get("questions", [])[:5], 1):
            st.write(f"{i}. {q}")

    st.caption(f"Generation mode: {pack.get('_meta',{}).get('backend','unknown')} | UI time: {st.session_state.get('elapsed',0):.2f}s")

st.divider()
st.caption("Local-first by design. Final submission numbers should be measured on the target Snapdragon HP PC, not estimated.")
