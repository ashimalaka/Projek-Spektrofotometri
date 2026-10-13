import numpy as np

T95 = {1: 12.71, 2: 4.303, 3: 3.182, 4: 2.776, 5: 2.571, 6: 2.447, 7: 2.365, 8: 2.306, 9: 2.262}


def fit(x, y):
    x, y = np.asarray(x, float), np.asarray(y, float)
    m, b = np.polyfit(x, y, 1)
    yh = m * x + b
    ssr, sst = float(((y - yh) ** 2).sum()), float(((y - y.mean()) ** 2).sum())
    r2 = 1 - ssr / sst if sst > 0 else float("nan")
    n = len(x)
    sy = (ssr / (n - 2)) ** 0.5 if n > 2 else float("nan")
    return dict(m=m, b=b, r2=r2, r=float(np.sign(m)) * abs(r2) ** 0.5, sy=sy, n=n, res=y - yh, x=x, y=y)


def conc(f, a):
    return (np.asarray(a, float) - f["b"]) / f["m"]


def limits(f, sd_blank=None):
    s = sd_blank if sd_blank and sd_blank > 0 else f["sy"]
    return 3 * s / f["m"], 10 * s / f["m"]          # LOD, LOQ (mg/L)


def char_conc(f):
    return 0.0044 / f["m"]                            # konsentrasi karakteristik (1% serapan)


def kadar(c_mgL, vol_mL, fp, massa_g):
    return np.asarray(c_mgL) * vol_mL * fp / massa_g  # mg/kg


def mean_sd_ci(v):
    v = np.asarray(v, float)
    n = len(v)
    sd = v.std(ddof=1) if n > 1 else 0.0
    t = T95.get(n - 1, 1.96)
    return v.mean(), sd, (t * sd / n ** 0.5 if n > 1 else 0.0)
