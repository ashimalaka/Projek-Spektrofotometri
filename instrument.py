"""Model sederhana respons AAS nyala untuk Cu (didaktik, bukan alat sungguhan)."""
import numpy as np

LINES = {"324,7 nm (utama)": 1.0, "327,4 nm": 0.5, "217,9 nm": 0.35, "222,6 nm": 0.18, "249,2 nm": 0.06}
BASE_SENS = 0.12  # A per (mg/L) pada kondisi optimum


def sensitivity(p):
    s = BASE_SENS * LINES[p["line"]]
    s *= np.exp(-0.5 * ((p["fuel"] - 0.9) / 0.3) ** 2)      # nyala lean-stoikiometri optimum
    s *= 1 - 0.03 * max(0.0, p["lamp"] - 5)                   # arus tinggi: self-reversal
    s *= 1 - 0.06 * (p["slit"] - 0.5)                         # celah lebar: cahaya lain masuk
    s *= (p["uptake"] / 5) ** 0.6                             # laju hisap
    return float(s)


def true_absorbance(c, p):
    s = sensitivity(p)
    return s * c / (1 + 0.04 * c) + p.get("bg", 0.0)          # kelengkungan di konsentrasi tinggi


def measure(c, p, rng, n=3):
    """Kembalikan n absorbansi replikat untuk larutan berkonsentrasi c (mg/L)."""
    a = true_absorbance(c, p)
    sd = np.hypot(0.0012 * (0.5 / p["slit"]) ** 0.5 * (5 / p["lamp"]) ** 0.5, 0.006 * a)
    return [round(float(a + rng.normal(0, sd)), 4) for _ in range(n)]


def readout(a):
    """Besaran yang ditampilkan alat: %T dan intensitas relatif (I0 = 100)."""
    return dict(T=100 * 10 ** (-a), I0=100.0, It=100 * 10 ** (-a))
