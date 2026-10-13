import numpy as np
import pandas as pd
import streamlit as st

from core import instrument, viewer

DEFAULT = pd.DataFrame({
    "Jenis": ["Blanko", "Standar", "Standar", "Standar", "Standar", "Standar", "Sampel", "Sampel"],
    "Nama": ["Blanko", "Std 1", "Std 2", "Std 3", "Std 4", "Std 5", "Sampel A", "Sampel B"],
    "Konsentrasi (mg/L)": [0.0, 1.0, 2.0, 3.0, 4.0, 5.0, 2.4, 3.6],
    "Absorbansi manual (opsional)": [None] * 8,
})


def render():
    st.caption("Masukkan konsentrasi tiap larutan. Alat mensimulasikan absorbansi 3 replikat. "
               "Jika Anda punya data praktikum, isi kolom absorbansi manual (menimpa simulasi).")
    with st.form("alat"):
        c = st.columns(5)
        p = dict(line=c[0].selectbox("Garis Cu", list(instrument.LINES)),
                 lamp=c[1].number_input("Arus lampu (mA)", 1.0, 15.0, 5.0, 0.5),
                 slit=c[2].selectbox("Lebar celah (nm)", [0.2, 0.5, 0.7, 1.3], 1),
                 fuel=c[3].slider("Rasio bahan bakar", 0.7, 1.5, 0.9, 0.05),
                 uptake=c[4].number_input("Laju hisap (mL/mnt)", 2.0, 8.0, 5.0, 0.5))
        df = st.data_editor(DEFAULT, num_rows="dynamic", column_config={
            "Jenis": st.column_config.SelectboxColumn(options=["Blanko", "Standar", "Sampel"], required=True)})
        seed = st.number_input("Seed derau acak", 0, 9999, 1)
        st.form_submit_button("Terapkan ke instrumen")
    rng = np.random.default_rng(int(seed))
    runs = []
    for _, r in df.dropna(subset=["Konsentrasi (mg/L)"]).iterrows():
        man = r["Absorbansi manual (opsional)"]
        A = [float(man)] if pd.notna(man) else instrument.measure(float(r["Konsentrasi (mg/L)"]), p, rng)
        runs.append(dict(type=r["Jenis"], name=str(r["Nama"]), conc=float(r["Konsentrasi (mg/L)"]), A=A))
    st.session_state["runs"], st.session_state["params"] = runs, p
    viewer.render(runs, p)
    st.caption("Model 3D skematik untuk pembelajaran. Garis 324,7 nm adalah UV (tak terlihat), berkasnya divisualisasikan ungu.")
    st.dataframe(pd.DataFrame([{"No": c["id"], "Nama luar": c["outer"], "Nama dalam": "; ".join(c["inner"]), "Fungsi": c["fn"]}
                               for c in viewer.COMPONENTS]), hide_index=True)
