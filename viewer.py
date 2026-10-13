import json
from pathlib import Path

import streamlit.components.v1 as components

ROOT = Path(__file__).resolve().parent.parent
COMPONENTS = json.loads((ROOT / "data" / "components.json").read_text("utf-8"))


def build_html(cfg):
    s = ROOT / "static"
    h = (s / "aas3d.html").read_text("utf-8")
    return (h.replace("/*CSS*/", (s / "aas3d.css").read_text("utf-8"))
             .replace("/*DATA*/", "window.CFG=" + json.dumps(cfg, ensure_ascii=False) + ";")
             .replace("/*JS*/", (s / "aas3d.js").read_text("utf-8")))


def render(runs, params, height=780):
    cfg = dict(runs=runs, params=params, parts=COMPONENTS)
    components.html(build_html(cfg), height=height)
