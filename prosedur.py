import pandas as pd
import streamlit as st


def render():
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
