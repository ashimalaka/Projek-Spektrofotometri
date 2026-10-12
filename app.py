# -*- coding: utf-8 -*-
"""Penetapan Kadar Tembaga (Cu) dengan AAS - aplikasi Streamlit."""
import re
import textwrap

import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

st.set_page_config(page_title="Kadar Cu dengan AAS", page_icon="🔬", layout="wide")

# ============================================================
# 1. HELPER GEOMETRI 3D
# ============================================================
_I = [7, 0, 0, 0, 4, 4, 6, 6, 4, 0, 3, 2]
_J = [3, 4, 1, 2, 5, 6, 5, 2, 0, 1, 6, 3]
_K = [0, 7, 2, 3, 6, 7, 1, 1, 5, 5, 7, 6]


def hexa(v):
    v = np.array(v, float)
    return dict(x=v[:, 0], y=v[:, 1], z=v[:, 2], i=_I, j=_J, k=_K)


def box(x0, x1, y0, y1, z0, z1):
    return hexa([(x0, y0, z0), (x0, y1, z0), (x1, y1, z0), (x1, y0, z0),
                 (x0, y0, z1), (x0, y1, z1), (x1, y1, z1), (x1, y0, z1)])


def taper(b, t, z0, z1):
    """Balok meruncing: b=(x0,x1,y0,y1) alas, t=(x0,x1,y0,y1) atas."""
    return hexa([(b[0], b[2], z0), (b[0], b[3], z0), (b[1], b[3], z0), (b[1], b[2], z0),
                 (t[0], t[2], z1), (t[0], t[3], z1), (t[1], t[3], z1), (t[1], t[2], z1)])


def frustum(c, axis, length, r1, r2=None, n=32):
    """Silinder/kerucut terpancung mulai titik c sepanjang sumbu 'x','y', atau 'z'."""
    r2 = r1 if r2 is None else r2
    th = np.linspace(0, 2 * np.pi, n, endpoint=False)

    def ring(u, r):
        a, b = r * np.cos(th), r * np.sin(th)
        if axis == "x":
            return np.c_[np.full(n, c[0] + u), c[1] + a, c[2] + b]
        if axis == "y":
            return np.c_[c[0] + a, np.full(n, c[1] + u), c[2] + b]
        return np.c_[c[0] + a, c[1] + b, np.full(n, c[2] + u)]

    def cen(u):
        p = np.array(c, float)
        p["xyz".index(axis)] += u
        return p

    v = np.vstack([ring(0, r1), ring(length, r2), cen(0), cen(length)])
    i, j, k = [], [], []
    for q in range(n):
        q2 = (q + 1) % n
        i += [q, q2, 2 * n, 2 * n + 1]
        j += [q2, n + q2, q2, n + q]
        k += [n + q, n + q, q, n + q2]
    return dict(x=v[:, 0], y=v[:, 1], z=v[:, 2], i=i, j=j, k=k)


def flame(z0, z1):
    def f(z):
        s = (z - 1.1) / 1.9
        return 5.2 + 0.5 * s, 8.8 - 0.5 * s, 0.12 + 0.23 * s
    a, b = f(z0), f(z1)
    return taper((a[0], a[1], -a[2], a[2]), (b[0], b[1], -b[2], b[2]), z0, z1)


# ============================================================
# 2. DATA KOMPONEN AAS (nama luar -> nama dalam)
# ============================================================
def P(name, desc, meshes, color):
    return dict(name=name, desc=desc, meshes=meshes, color=color)


def K(no, outer, fn, shell, color, label, parts, **kw):
    return dict(no=no, outer=outer, fn=fn, shell=shell, color=color,
                label=label, parts=parts, **kw)


def build_components():
    jaw = lambda x: [box(x, x + 0.1, -0.6, -0.05, 1.0, 3.0), box(x, x + 0.1, 0.05, 0.6, 1.0, 3.0)]
    comps = [
        K(0, "Casing / Rumah Instrumen",
          "Rumah pelindung seluruh bagian optik & atomisasi.",
          [box(-1.2, 18.3, -3, 3, -1.4, 4.2)], "#95A5A6", None,
          [P("Ruang lampu", "Tempat HCL dipasang.", [], "#000"),
           P("Ruang atomisasi", "Tempat burner dan nyala.", [], "#000"),
           P("Ruang optik", "Tempat monokromator dan detektor.", [], "#000")],
          opacity=0.10, casing=True),
        K(1, "Hollow Cathode Lamp (HCL) Cu",
          "Sumber cahaya: memancarkan garis spesifik Cu 324,7 nm.",
          [frustum((0, 0, 2), "x", 3, 0.7)], "#E67E22", (1.5, 0, 3.1),
          [P("Soket / basis lampu", "Penghubung listrik lampu.", [frustum((-0.8, 0, 2), "x", 0.8, 0.45)], "#7F8C8D"),
           P("Katoda berongga (logam Cu)", "Atom Cu terpercik lalu tereksitasi dan memancarkan cahaya.", [frustum((1.0, 0, 2), "x", 1.6, 0.3)], "#B87333"),
           P("Anoda (W/Zr)", "Elektroda positif.", [frustum((0.8, 0, 2.5), "x", 1.8, 0.05)], "#BDC3C7"),
           P("Gas pengisi (Ne/Ar)", "Gas mulia bertekanan rendah yang terionisasi.", [], "#000"),
           P("Jendela kuarsa", "Meneruskan sinar UV.", [frustum((2.95, 0, 2), "x", 0.1, 0.7)], "#AED6F1")]),
        K(2, "Wadah Sampel / Standar Cu",
          "Menampung larutan standar atau sampel Cu.",
          [frustum((2, 0, -3.2), "z", 1.0, 0.5)], "#D5DBDB", (2, 0, -3.5),
          [P("Larutan Cu2+", "Larutan standar/sampel yang dihisap.", [frustum((2, 0, -3.15), "z", 0.55, 0.45)], "#3498DB")]),
        K(3, "Nebulizer",
          "Menghisap larutan dan mengubahnya menjadi aerosol halus.",
          [frustum((2, 0, -0.3), "x", 2.2, 0.28)], "#2E86C1", (3, 0, 0.3),
          [P("Kapiler hisap", "Pipa kecil penghisap larutan.", [frustum((2, 0, -2.7), "z", 2.4, 0.06)], "#F1C40F"),
           P("Nosel / venturi", "Aliran udara cepat menimbulkan vakum penghisap.", [frustum((3.2, 0, -0.3), "x", 0.9, 0.14, 0.06)], "#E74C3C"),
           P("Impact bead", "Memecah tetesan menjadi lebih halus.", [frustum((4.25, 0, -0.3), "x", 0.25, 0.15)], "#ECF0F1")]),
        K(4, "Spray Chamber (Ruang Pengabut)",
          "Mencampur aerosol dengan gas; tetes besar dibuang.",
          [frustum((4, 0, -0.3), "x", 5, 0.75)], "#5DADE2", (6.5, 0, -1.3),
          [P("Flow spoiler (baffle)", "Menyaring tetes besar.", [box(6.0, 6.1, -0.5, 0.5, -0.8, 0.2)], "#2C3E50"),
           P("Drain (saluran limbah)", "Mengalirkan larutan berlebih.", [frustum((8.6, 0, -2.0), "z", 1.0, 0.12)], "#7F8C8D"),
           P("Botol limbah", "Menampung limbah dari drain.", [frustum((8.6, 0, -3.2), "z", 1.2, 0.5)], "#D5DBDB")]),
        K(5, "Burner Head (Kepala Pembakar)",
          "Tempat nyala air-asetilena; celah panjang 10 cm.",
          [box(5, 9, -0.3, 0.3, 0.6, 1.1)], "#566573", (7, 0, 0.0),
          [P("Slot burner", "Celah pelepasan campuran gas.", [box(5.2, 8.8, -0.05, 0.05, 1.1, 1.14)], "#111"),
           P("Leher burner", "Penghubung ke spray chamber.", [frustum((7, 0, 0.2), "z", 0.45, 0.35)], "#7F8C8D")]),
        K(6, "Saluran Gas Udara-Asetilena",
          "Mengalirkan oksidan (udara) dan bahan bakar (C2H2).",
          [frustum((4.7, 0.7, -0.3), "y", 1.6, 0.12), frustum((5.4, 0.7, -0.3), "y", 1.6, 0.12)], "#85929E", (5.0, 2.4, -0.3),
          [P("Selang udara (oksidan)", "Udara tekan sebagai oksidan.", [frustum((4.7, 0.7, -0.3), "y", 1.6, 0.12)], "#3498DB"),
           P("Selang asetilena (bahan bakar)", "Gas bahan bakar C2H2.", [frustum((5.4, 0.7, -0.3), "y", 1.6, 0.12)], "#E74C3C")]),
        K(7, "Nyala (Flame)",
          "Tempat atomisasi: ion Cu2+ menjadi atom Cu0 yang menyerap cahaya.",
          [flame(1.1, 3.0)], "#F39C12", (7, 0, 3.3),
          [P("Zona primer", "Reaksi pembakaran awal.", [flame(1.1, 1.6)], "#3498DB"),
           P("Zona interkonal", "Atomisasi; serapan terjadi di sini.", [flame(1.6, 2.5)], "#E67E22"),
           P("Zona sekunder", "Oksidasi sempurna produk.", [flame(2.5, 3.0)], "#F7DC6F")],
          opacity=0.5),
        K(8, "Monokromator",
          "Memilih panjang gelombang 324,7 nm dan menyingkirkan cahaya lain.",
          [box(10.5, 14.5, -1.3, 1.3, 0.5, 3.5)], "#8E9AAF", (12.5, 0, 3.8),
          [P("Celah masuk (entrance slit)", "Membatasi berkas cahaya masuk.", jaw(10.6), "#2C3E50"),
           P("Kisi difraksi (grating)", "Menguraikan cahaya per panjang gelombang.", [box(11.6, 13.0, -0.75, -0.65, 1.0, 3.0)], "#C39BD3"),
           P("Celah keluar (exit slit)", "Meloloskan hanya garis 324,7 nm.", jaw(14.3), "#2C3E50")]),
        K(9, "Detektor (Photomultiplier Tube)",
          "Mengubah intensitas cahaya menjadi sinyal listrik.",
          [frustum((15, 0, 2), "x", 1.6, 0.55)], "#27AE60", (15.8, 0, 3.0),
          [P("Fotokatoda", "Melepas elektron saat terkena foton.", [frustum((15.05, 0, 2), "x", 0.08, 0.45)], "#F1948A"),
           P("Dinoda", "Menggandakan elektron berantai.",
             [box(x - 0.04, x + 0.04, -0.3, 0.3, 2 + o - 0.15, 2 + o + 0.15)
              for x, o in [(15.4, 0.25), (15.7, -0.25), (16.0, 0.25)]], "#F7DC6F"),
           P("Anoda PMT", "Mengumpulkan elektron menjadi arus.", [frustum((16.2, 0, 2), "x", 0.35, 0.05)], "#ECF0F1")]),
        K(10, "Penguat Sinyal (Amplifier)",
          "Menguatkan dan memproses sinyal detektor.",
          [box(16.9, 17.9, -0.9, 0.9, 1.0, 3.0)], "#1ABC9C", (17.4, 0, 3.4),
          [P("Penguat (lock-in / AC)", "Memisahkan sinyal lampu dari emisi nyala.", [box(17.05, 17.45, -0.6, 0.6, 1.2, 1.8)], "#2C3E50"),
           P("Konverter A/D", "Mengubah sinyal analog menjadi digital.", [box(17.05, 17.45, -0.6, 0.6, 2.2, 2.8)], "#34495E")]),
        K(11, "Komputer & Perangkat Lunak",
          "Menampilkan absorbansi, kurva kalibrasi, dan konsentrasi.",
          [box(19.5, 20.0, -1.6, 1.6, 1.4, 3.6), box(19.6, 19.9, -0.3, 0.3, 0.6, 1.4), box(19.3, 20.2, -0.9, 0.9, 0.5, 0.6)],
          "#34495E", (19.8, 0, 4.0),
          [P("Layar", "Menampilkan data absorbansi.", [box(19.45, 19.5, -1.45, 1.45, 1.6, 3.4)], "#1F618D"),
           P("Perangkat lunak AAS", "Mengatur parameter dan menghitung hasil.", [], "#000")]),
        K(12, "Exhaust Hood (Penghisap Gas Buang)",
          "Membuang gas hasil pembakaran dan uap logam.",
          [taper((5, 9, -1.0, 1.0), (6.4, 7.6, -0.4, 0.4), 3.7, 5.5)], "#AAB7B8", (7, 0, 7.4),
          [P("Saluran buang (duct)", "Pipa menuju ventilasi/fume hood.", [frustum((7, 0, 5.5), "z", 1.5, 0.35)], "#7F8C8D")]),
    ]
    return comps


COMPONENTS = build_components()
BEAM = np.array([(3, 0, 2), (10.65, 0, 2), (12.3, -0.65, 2), (14.35, 0, 2), (15, 0, 2)], float)
CAMERAS = {
    "Isometrik": dict(eye=dict(x=1.2, y=-1.9, z=0.9)),
    "Depan": dict(eye=dict(x=0.0, y=-2.6, z=0.2)),
    "Atas": dict(eye=dict(x=0.0, y=-0.01, z=2.8)),
    "Samping kiri": dict(eye=dict(x=-2.2, y=-0.6, z=0.5)),
}


def wrap(t):
    return textwrap.fill(t, 42).replace("\n", "<br>")


def mesh(m, color, opacity, hover):
    return go.Mesh3d(**m, color=color, opacity=opacity, hoverinfo="text", hovertext=hover,
                     flatshading=True, showlegend=False,
                     lighting=dict(ambient=0.55, diffuse=0.8, specular=0.2, roughness=0.6))


def build_figure(show_inner, show_casing, show_beam, show_labels, selected, camera):
    fig = go.Figure()
    for c in COMPONENTS:
        if c.get("casing") and not show_casing:
            continue
        focus = selected == "Semua" or selected == c["no"]
        has_parts = any(p["meshes"] for p in c["parts"])
        inner_here = focus and (show_inner or selected != "Semua") and has_parts
        op = c.get("opacity", 0.95)
        if inner_here:
            op = min(op, 0.15)
        if not focus:
            op = min(op, 0.08)
        hover = f"<b>{c['no']}. {c['outer']}</b><br>{wrap(c['fn'])}"
        for m in c["shell"]:
            fig.add_trace(mesh(m, c["color"], op, hover))
        if inner_here:
            for p in c["parts"]:
                ph = f"<b>{p['name']}</b><br><i>isi dari: {c['outer']}</i><br>{wrap(p['desc'])}"
                for m in p["meshes"]:
                    fig.add_trace(mesh(m, p["color"], 1.0, ph))
    if show_beam:
        fig.add_trace(go.Scatter3d(x=BEAM[:, 0], y=BEAM[:, 1], z=BEAM[:, 2], mode="lines",
                                   line=dict(color="#8E44AD", width=6), name="Berkas cahaya",
                                   hoverinfo="text", hovertext="Berkas cahaya Cu 324,7 nm (skematik)",
                                   showlegend=False))
    if show_labels:
        L = [c for c in COMPONENTS if c["label"]]
        fig.add_trace(go.Scatter3d(x=[c["label"][0] for c in L], y=[c["label"][1] for c in L],
                                   z=[c["label"][2] for c in L], mode="text",
                                   text=[f"<b>{c['no']}</b>" for c in L],
                                   textfont=dict(size=16, color="#111"), hoverinfo="skip",
                                   showlegend=False))
    ax = dict(visible=False)
    fig.update_layout(
        height=620, margin=dict(l=0, r=0, t=0, b=0), paper_bgcolor="#F4F6F7",
        scene=dict(xaxis=ax, yaxis=ax, zaxis=ax, aspectmode="data", bgcolor="#F4F6F7",
                   camera=CAMERAS[camera]),
        uirevision=camera,
    )
    return fig


def tabel_komponen():
    rows = [{"No": c["no"], "Nama luar (komponen utama)": c["outer"],
             "Nama dalam (isi / penyusun)": "; ".join(p["name"] for p in c["parts"]) or "-",
             "Fungsi": c["fn"]} for c in COMPONENTS]
    return pd.DataFrame(rows)


# ============================================================
# 3. HALAMAN
# ============================================================
st.title("🔬 Penetapan Kadar Tembaga (Cu) dengan AAS")
st.caption("Atomic Absorption Spectrophotometry (Spektrofotometri Serapan Atom) - media belajar interaktif")

tab1, tab2, tab3, tab4 = st.tabs(["📖 Teori", "🧊 Instrumen 3D", "🧪 Prosedur", "🧮 Kalkulator"])

# ---------------- TAB 1: TEORI ----------------
with tab1:
    st.subheader("Prinsip dasar")
    st.markdown(
        "Atom Cu bebas dalam nyala menyerap cahaya pada panjang gelombang yang khas "
        "(**324,7 nm**). Makin banyak atom Cu, makin besar cahaya yang diserap. "
        "Hubungan ini mengikuti **Hukum Lambert-Beer**:"
    )
    st.latex(r"A = \log\frac{I_0}{I_t} = \varepsilon \cdot b \cdot c")
    st.markdown(
        "- **A**: absorbansi  \n- **I₀ / Iₜ**: intensitas cahaya sebelum / sesudah melewati nyala  \n"
        "- **ε**: konstanta serapan, **b**: panjang jalur nyala, **c**: konsentrasi  \n\n"
        "Konsentrasi sampel ditentukan dari **kurva kalibrasi** (absorbansi vs konsentrasi standar):"
    )
    st.latex(r"A = m\,C + b \;\Rightarrow\; C = \frac{A-b}{m}")
    st.subheader("Alur kerja AAS")
    st.markdown(
        "**Lampu HCL Cu → Nyala (atomisasi) → Monokromator → Detektor (PMT) → Penguat → Komputer.**  \n"
        "Sampel cair dihisap nebulizer, dikabutkan di spray chamber, lalu masuk ke nyala udara-asetilena "
        "melalui burner head."
    )
    st.info("Buka tab **Instrumen 3D** untuk melihat posisi dan isi tiap komponen.")

# ---------------- TAB 2: 3D ----------------
with tab2:
    st.subheader("Model 3D instrumen AAS (skematik)")
    st.caption("Putar dengan menyeret, zoom dengan scroll/cubit, arahkan kursor ke komponen untuk melihat namanya.")
    opsi = {"Semua": "Semua"}
    opsi.update({f"{c['no']}. {c['outer']}": c["no"] for c in COMPONENTS if c["no"] > 0})
    c1, c2 = st.columns(2)
    pilih = c1.selectbox("Sorot komponen", list(opsi.keys()))
    kamera = c2.selectbox("Sudut pandang", list(CAMERAS.keys()))
    t1, t2, t3, t4 = st.columns(4)
    inner = t1.toggle("Bagian dalam (X-ray)", value=False)
    casing = t2.toggle("Casing", value=True)
    beam = t3.toggle("Berkas cahaya", value=True)
    labels = t4.toggle("Nomor", value=True)

    st.plotly_chart(build_figure(inner, casing, beam, labels, opsi[pilih], kamera))

    sel = opsi[pilih]
    if sel == "Semua":
        st.markdown("#### Struktur: nama luar → nama dalam")
        st.dataframe(tabel_komponen(), hide_index=True)
    else:
        c = next(x for x in COMPONENTS if x["no"] == sel)
        st.markdown(f"#### {c['no']}. {c['outer']}")
        st.write(c["fn"])
        st.markdown("**Isi / bagian dalam:**")
        st.dataframe(pd.DataFrame([{"Nama dalam": p["name"], "Fungsi": p["desc"]} for p in c["parts"]]),
                     hide_index=True)
    st.caption("Model bersifat skematik untuk pembelajaran; bentuk dan ukuran asli berbeda tiap merek alat.")

# ---------------- TAB 3: PROSEDUR ----------------
with tab3:
    st.subheader("Prosedur umum penetapan kadar Cu (AAS nyala)")
    st.markdown("""
**1. Larutan induk Cu 1000 mg/L**  
Larutkan ±3,9293 g CuSO₄·5H₂O (atau 1,000 g logam Cu dalam HNO₃ pekat) dengan air bebas ion, lalu tepatkan dalam labu takar 1 L.

**2. Larutan standar kerja**  
Encerkan larutan induk bertahap menjadi seri standar, misalnya 0 - 1 - 2 - 3 - 4 - 5 mg/L, dalam matriks asam yang sama dengan sampel (mis. HNO₃ 0,5%).

**3. Preparasi sampel**  
Destruksi basah dengan HNO₃ pekat (sesuai SOP), dinginkan, saring bila perlu, pindahkan kuantitatif ke labu takar dan tepatkan. Lakukan juga **blanko** reagen.

**4. Kondisi alat (acuan umum, ikuti manual alat)**
""")
    st.table(pd.DataFrame({
        "Parameter": ["Panjang gelombang", "Lampu", "Nyala", "Lebar celah", "Arus lampu"],
        "Nilai umum": ["324,7 nm", "HCL Cu", "Udara-asetilena (oksidasi, biru)", "Sesuai manual alat", "Sesuai rekomendasi lampu"],
    }))
    st.markdown("""
**5. Pengukuran**  
Nol-kan alat dengan blanko, ukur standar dari konsentrasi terendah ke tertinggi, lalu sampel (replikat). Bilas dengan blanko di antara pengukuran.

**6. Perhitungan**  
Buat kurva kalibrasi, hitung C sampel dari persamaan regresi, lalu koreksi faktor pengenceran dan massa sampel (lihat tab **Kalkulator**).
""")
    st.warning("Keselamatan: asetilena mudah terbakar, HNO₃ pekat korosif. Gunakan APD, pastikan exhaust aktif, dan ikuti SOP laboratorium.")

# ---------------- TAB 4: KALKULATOR ----------------
with tab4:
    st.subheader("1) Data kurva kalibrasi")
    st.caption("Nilai awal hanyalah contoh. Ganti dengan data praktikum Anda (baris bisa ditambah/dihapus).")
    awal = pd.DataFrame({"Konsentrasi (mg/L)": [0.0, 1.0, 2.0, 3.0, 4.0, 5.0],
                         "Absorbansi": [0.002, 0.045, 0.088, 0.131, 0.172, 0.214]})
    cal = st.data_editor(awal, num_rows="dynamic", key="kal").dropna()

    if len(cal) < 3:
        st.warning("Masukkan minimal 3 titik kalibrasi.")
        st.stop()

    x = cal.iloc[:, 0].astype(float).to_numpy()
    y = cal.iloc[:, 1].astype(float).to_numpy()
    m, b = np.polyfit(x, y, 1)
    yhat = m * x + b
    ss_res = float(((y - yhat) ** 2).sum())
    ss_tot = float(((y - y.mean()) ** 2).sum())
    r2 = 1 - ss_res / ss_tot if ss_tot > 0 else float("nan")
    sy = (ss_res / (len(x) - 2)) ** 0.5
    if m <= 0:
        st.error("Slope kurva tidak positif. Periksa data kalibrasi.")
        st.stop()
    lod, loq = 3.3 * sy / m, 10 * sy / m

    k1, k2, k3, k4 = st.columns(4)
    k1.metric("Slope (m)", f"{m:.4f}")
    k2.metric("Intersep (b)", f"{b:.4f}")
    k3.metric("R²", f"{r2:.4f}")
    k4.metric("LOD / LOQ (mg/L)", f"{lod:.3f} / {loq:.3f}")
    st.latex(rf"A = {m:.4f}\,C {'+' if b >= 0 else '-'} {abs(b):.4f}")
    if r2 < 0.995:
        st.info("R² di bawah 0,995, pertimbangkan membuat ulang standar atau memeriksa outlier.")

    st.subheader("2) Data sampel")
    s1, s2 = st.columns(2)
    teks = s1.text_input("Absorbansi sampel (replikat, pisah spasi atau ;)", "0.105 0.108 0.103")
    massa = s2.number_input("Massa sampel (g)", min_value=0.0001, value=1.0000, step=0.0100, format="%.4f")
    s3, s4 = st.columns(2)
    vol = s3.number_input("Volume akhir larutan sampel (mL)", min_value=0.1, value=50.0, step=1.0)
    fp = s4.number_input("Faktor pengenceran", min_value=1.0, value=1.0, step=1.0)

    try:
        a_s = np.array([float(t.replace(",", ".")) for t in re.split(r"[;\s]+", teks.strip()) if t])
    except ValueError:
        a_s = np.array([])
    if a_s.size == 0:
        st.warning("Isi absorbansi sampel dengan angka.")
        st.stop()

    c_s = (a_s - b) / m                      # mg/L terukur
    kadar = c_s * vol * fp / massa           # mg/kg
    rata, sd = kadar.mean(), (kadar.std(ddof=1) if kadar.size > 1 else 0.0)
    rsd = sd / rata * 100 if rata else float("nan")

    hasil = pd.DataFrame({"Replikat": range(1, len(a_s) + 1), "Absorbansi": a_s,
                          "C terukur (mg/L)": c_s, "Kadar Cu (mg/kg)": kadar})
    st.dataframe(hasil, hide_index=True)
    r1, r2c, r3 = st.columns(3)
    r1.metric("Kadar Cu rata-rata", f"{rata:.2f} mg/kg")
    r2c.metric("SD", f"{sd:.2f}")
    r3.metric("%RSD", f"{rsd:.2f}%")
    st.latex(r"\text{Kadar (mg/kg)} = \frac{C\,(\text{mg/L}) \times V\,(\text{mL}) \times FP}{m\,(\text{g})}")
    if c_s.max() > x.max() or c_s.min() < x.min():
        st.warning("Ada sampel di luar rentang kalibrasi. Encerkan sampel lalu ukur ulang.")

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x, y=y, mode="markers", name="Standar", marker=dict(size=9)))
    xx = np.linspace(min(x.min(), c_s.min(), 0), max(x.max(), c_s.max()), 50)
    fig.add_trace(go.Scatter(x=xx, y=m * xx + b, mode="lines", name="Regresi"))
    fig.add_trace(go.Scatter(x=c_s, y=a_s, mode="markers", name="Sampel",
                             marker=dict(size=11, symbol="diamond", color="#C0392B")))
    fig.update_layout(xaxis_title="Konsentrasi Cu (mg/L)", yaxis_title="Absorbansi",
                      height=420, margin=dict(l=10, r=10, t=30, b=10))
    st.plotly_chart(fig)
    st.download_button("⬇️ Unduh hasil (CSV)", hasil.to_csv(index=False).encode("utf-8"),
                       file_name="hasil_kadar_cu.csv", mime="text/csv")

    with st.expander("Kalkulator pengenceran (C₁·V₁ = C₂·V₂)"):
        d1, d2, d3 = st.columns(3)
        c_awal = d1.number_input("C₁ larutan induk (mg/L)", min_value=0.0001, value=1000.0)
        c_akhir = d2.number_input("C₂ yang diinginkan (mg/L)", min_value=0.0001, value=5.0)
        v_akhir = d3.number_input("V₂ labu takar (mL)", min_value=0.1, value=100.0)
        st.success(f"Pipet **{c_akhir * v_akhir / c_awal:.3f} mL** larutan induk, lalu tepatkan hingga {v_akhir:g} mL.")
