# -*- coding: utf-8 -*-
"""Penetapan Kadar Tembaga (Cu) dengan AAS - aplikasi Streamlit (entry point)."""
import streamlit as st

from views import analisis, instrumen, prosedur, teori

st.set_page_config(page_title="Kadar Cu dengan AAS", page_icon="🔬", layout="wide")
st.title("🔬 Penetapan Kadar Tembaga (Cu) dengan AAS")
st.caption("Atomic Absorption Spectrophotometry - media belajar interaktif")

t1, t2, t3, t4 = st.tabs(["📖 Teori", "🧊 Instrumen 3D & Pengukuran", "📊 Analisis Data Cu", "🧪 Prosedur"])
with t1:
    teori.render()
with t2:
    instrumen.render()
with t3:
    analisis.render()
with t4:
    prosedur.render()
