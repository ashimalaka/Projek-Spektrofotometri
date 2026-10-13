import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from core import calibration as cal
from core import instrument


def render():
    runs = st.session_state.get("runs")
    if not runs:
        st.info("Isi dan terapkan data di tab Instrumen 3D terlebih dahulu.")
        return
    rows = []
    for r in runs:
        a = np.array(r["A"])
        m, sd, _ = cal.mean_sd_ci(a)
        t = instrument.readout(m)
        rows.append({"Jenis": r["type"], "Nama": r["name"], "C (mg/L)": r["conc"], "A rata-rata": m, "SD": sd,
                     "%RSD": sd / m * 100 if m else np.nan, "%T": t["T"], "It/I0": t["It"] / t["I0"]})
    d = pd.DataFrame(rows)
    st.subheader("1) Data terbaca instrumen")
    st.dataframe(d, hide_index=True)

    std = d[d["Jenis"].isin(["Blanko", "Standar"])]
    if len(std) < 3:
        st.warning("Minimal 3 titik (blanko + standar) untuk kalibrasi.")
        return
    f = cal.fit(std["C (mg/L)"], std["A rata-rata"])
    blk = [np.std(r["A"], ddof=1) for r in runs if r["type"] == "Blanko" and len(r["A"]) > 1]
    lod, loq = cal.limits(f, blk[0] if blk else None)
    st.subheader("2) Kurva kalibrasi")
    k = st.columns(5)
    k[0].metric("Slope", f"{f['m']:.4f}")
    k[1].metric("Intersep", f"{f['b']:.4f}")
    k[2].metric("R² / r", f"{f['r2']:.4f} / {f['r']:.4f}")
    k[3].metric("LOD / LOQ", f"{lod:.3f} / {loq:.3f} mg/L")
    k[4].metric("Konsentrasi karakteristik", f"{cal.char_conc(f):.3f} mg/L")
    st.latex(rf"A = {f['m']:.4f}\,C {'+' if f['b'] >= 0 else '-'} {abs(f['b']):.4f}")
    g1, g2 = st.columns(2)
    xx = np.linspace(0, max(f["x"]) * 1.1, 40)
    s = d[d["Jenis"] == "Sampel"]
    fg = go.Figure([go.Scatter(x=f["x"], y=f["y"], mode="markers", name="Standar"),
                    go.Scatter(x=xx, y=f["m"] * xx + f["b"], mode="lines", name="Regresi"),
                    go.Scatter(x=cal.conc(f, s["A rata-rata"]), y=s["A rata-rata"], mode="markers", name="Sampel",
                               marker=dict(symbol="diamond", size=11, color="#C0392B"))])
    fg.update_layout(xaxis_title="Cu (mg/L)", yaxis_title="Absorbansi", height=360, margin=dict(t=20))
    g1.plotly_chart(fg)
    fr = go.Figure(go.Bar(x=f["x"], y=f["res"]))
    fr.update_layout(xaxis_title="Cu (mg/L)", yaxis_title="Residual (A)", height=360, margin=dict(t=20), title="Residual")
    g2.plotly_chart(fr)
    st.success("R² ≥ 0,995: kalibrasi memenuhi." if f["r2"] >= 0.995 else "R² < 0,995: periksa standar/outlier.")

    st.subheader("3) Penetapan kadar Cu pada sampel")
    c1, c2, c3 = st.columns(3)
    massa = c1.number_input("Massa sampel (g)", 0.0001, value=1.0, format="%.4f")
    vol = c2.number_input("Volume akhir (mL)", 0.1, value=50.0)
    fp = c3.number_input("Faktor pengenceran", 1.0, value=1.0)
    out = []
    for r in [r for r in runs if r["type"] == "Sampel"]:
        cs = cal.conc(f, r["A"])
        kd = cal.kadar(cs, vol, fp, massa)
        m, sd, ci = cal.mean_sd_ci(kd)
        flag = "di luar rentang" if (cs.max() > f["x"].max() or cs.min() < 0) else "OK"
        out.append({"Sampel": r["name"], "C terukur (mg/L)": cs.mean(), "Kadar Cu (mg/kg)": m, "SD": sd,
                    "%RSD": sd / m * 100 if m else np.nan, "CI 95% (±)": ci, "Rentang": flag})
    if out:
        o = pd.DataFrame(out)
        st.dataframe(o, hide_index=True)
        st.latex(r"\text{Kadar (mg/kg)} = \frac{C\,(\text{mg/L}) \times V\,(\text{mL}) \times FP}{m\,(\text{g})}")
        st.download_button("⬇️ Unduh hasil (CSV)", o.to_csv(index=False).encode(), "hasil_kadar_cu.csv", "text/csv")
