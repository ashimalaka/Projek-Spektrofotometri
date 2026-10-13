# Penetapan Kadar Cu dengan AAS (Streamlit)

Media belajar interaktif: teori, model 3D AAS yang bisa dibuka-tutup (nama luar & dalam komponen),
animasi pengapian nyala dan aspirasi sampel, input konsentrasi, serta analisis data kalibrasi Cu.

## Struktur
```
app.py                  # entry point (tab)
core/instrument.py      # model respons AAS (garis, arus lampu, celah, nyala, laju hisap, derau)
core/calibration.py     # regresi, LOD/LOQ, konsentrasi karakteristik, kadar mg/kg, CI 95%
core/viewer.py          # merakit HTML 3D (css + js + data) untuk Streamlit
views/                  # teori.py, instrumen.py, analisis.py, prosedur.py
static/aas3d.*          # scene Three.js (html, css, js terpisah)
data/components.json    # daftar komponen: nama luar -> nama dalam
```

## Jalankan lokal
```
pip install -r requirements.txt
streamlit run app.py
```
Model 3D memuat Three.js dari cdn.jsdelivr.net, jadi perlu internet.

## Cara pakai
1. Tab **Instrumen 3D**: atur kondisi alat, isi tabel konsentrasi (blanko/standar/sampel), klik *Terapkan*.
2. Di panel 3D: geser *Tutup atas* / *Pintu atomisasi*, aktifkan *Bedah komponen* untuk melihat isi dalam.
3. Klik **Nyalakan** (urutan: exhaust, udara, asetilena, igniter), lalu **Hisap & ukur** atau **Jalankan semua**.
4. Tab **Analisis Data Cu**: kurva kalibrasi, LOD/LOQ, residual, dan kadar Cu sampel.

## Deploy (Streamlit Community Cloud)
Upload semua file ke GitHub, lalu deploy dengan Main file path `app.py`.
