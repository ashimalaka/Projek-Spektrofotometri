# Penetapan Kadar Cu dengan AAS (Streamlit)

Web interaktif: teori, model 3D instrumen AAS (nama luar & nama dalam komponen), prosedur, dan kalkulator kurva kalibrasi.

## Struktur
```
app.py
requirements.txt
README.md
.gitignore
.streamlit/config.toml
```

## Jalankan lokal
```
pip install -r requirements.txt
streamlit run app.py
```

## Deploy (Streamlit Community Cloud)
1. Upload semua file ke repo GitHub (branch `main`).
2. Buka https://share.streamlit.io, login dengan GitHub, klik **Create app**.
3. Pilih repo, branch `main`, Main file path: `app.py`, lalu **Deploy**.
