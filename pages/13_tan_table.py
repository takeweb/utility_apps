import streamlit as st
import pandas as pd
from libs.tan_utils import build_tan_rows, highlight_row_func, render_slope_figure

st.set_page_config(page_title="tan と角度の関係 (clean)", page_icon="📐")
st.title("tan と角度の関係 — 傾き表示")
st.caption(
    "度(°) とラジアン、tan(θ) を 15°刻みで表示します。cos=0 の角度では tan は未定義になります。"
)

# UI
step = 15
cols = st.columns([1, 1])
show_radians = cols[0].checkbox("ラジアン表示有り", value=True)
show_exact = cols[1].checkbox("計算式表示", value=True)

if "highlight_angle_tan" not in st.session_state:
    st.session_state["highlight_angle_tan"] = 30

angles = list(range(0, 361, step))
# スライダーで角度を選択（step に従う）
st.slider(
    "ハイライトする角度 (°)",
    min_value=0,
    max_value=360,
    step=step,
    key="highlight_angle_tan",
)
highlight_angle = int(st.session_state["highlight_angle_tan"])

# 表示縮尺（視覚用）は 1 固定
visual_scale = 1.0

# Build table
rows, _ = build_tan_rows(step=step, show_radians=show_radians, show_exact=show_exact)
df = pd.DataFrame(rows)
st.subheader("tan(θ) 一覧（15°刻み）")

# Render slope figure (matplotlib fallback handled inside utils)
try:
    fig = render_slope_figure(
        highlight_angle=highlight_angle, visual_scale=visual_scale
    )
    st.pyplot(fig)
except Exception:
    st.info(
        "matplotlib/numpy が無いため傾き可視化は表示されません。テーブルは表示されます。"
    )

# Table with highlight
styler_func = highlight_row_func(highlight_angle)
try:
    styler = df.style.apply(styler_func, axis=1)
    st.write(styler)
except Exception:
    st.table(rows)

st.caption(
    "付記: tan の未定義角度は 'undef' と表示しています。visual_scale は表示のみを縮小します（軸の数値は変わりません）。"
)
