import pandas as pd
import streamlit as st


def render():
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
