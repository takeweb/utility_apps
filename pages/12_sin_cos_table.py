import math
import streamlit as st
import pandas as pd

st.set_page_config(page_title="sin、cosと単位円の角度の関係", page_icon="⚪️")

st.title("sin、cosと単位円の角度の関係")
st.caption("度(°) とラジアン、sin/cos、単位円上の座標を確認する表")

# 設定エリア（上段にまとめる）
settings_cols = st.columns([1, 1, 1, 1])
step = settings_cols[0].selectbox(
    "表示ステップ（度）",
    options=[1, 2, 5, 10, 15, 30],
    index=4,
    help="何度刻みで表を作るかを選択します",
)
show_radians = settings_cols[1].checkbox("ラジアンを表示する", value=True)
show_cos = settings_cols[2].checkbox("cos も表示する", value=True)
show_exact = settings_cols[3].checkbox(
    "主要角の正確値を表示 (例: 30° -> 1/2)", value=True
)

# ハイライト角選択（step に連動）
if "highlight_angle" not in st.session_state:
    st.session_state["highlight_angle"] = 90
angles_for_select = list(range(0, 361, step))
try:
    default_idx = angles_for_select.index(st.session_state["highlight_angle"])
except ValueError:
    default_idx = 0
selection = st.selectbox(
    "ハイライトする角度 (°)", options=angles_for_select, index=default_idx
)
st.session_state["highlight_angle"] = selection
highlight_angle = st.session_state["highlight_angle"]

# 表と単位円を縦に並べて表示 (表 -> 円)
st.subheader(f"0° 〜 360° (step {step}°)")

angles = list(range(0, 361, step))

# 主要角の正確値マップ (sin, cos) を文字列で定義（15°刻み）
exact_map = {
    0: ("0", "1"),
    15: ("(√6-√2)/4", "(√6+√2)/4"),
    30: ("1/2", "√3/2"),
    45: ("√2/2", "√2/2"),
    60: ("√3/2", "1/2"),
    75: ("(√6+√2)/4", "(√6-√2)/4"),
    90: ("1", "0"),
    105: ("(√6+√2)/4", "-(√6-√2)/4"),
    120: ("√3/2", "-1/2"),
    135: ("√2/2", "-√2/2"),
    150: ("1/2", "-√3/2"),
    165: ("(√6-√2)/4", "-(√6+√2)/4"),
    180: ("0", "-1"),
    195: ("-(√6-√2)/4", "-(√6+√2)/4"),
    210: ("-1/2", "-√3/2"),
    225: ("-√2/2", "-√2/2"),
    240: ("-√3/2", "-1/2"),
    255: ("-(√6+√2)/4", "-(√6-√2)/4"),
    270: ("-1", "0"),
    285: ("-(√6+√2)/4", "(√6-√2)/4"),
    300: ("-√3/2", "1/2"),
    315: ("-√2/2", "√2/2"),
    330: ("-1/2", "√3/2"),
    345: ("-(√6-√2)/4", "(√6+√2)/4"),
    360: ("0", "1"),
}

# 表データを作成
rows = []
for deg in angles:
    rad = math.radians(deg)
    s = math.sin(rad)
    c = math.cos(rad)

    if show_exact and deg in exact_map:
        sin_val = exact_map[deg][0]
        cos_val = exact_map[deg][1]
        unit_x = cos_val
        unit_y = sin_val
    else:
        sin_val = f"{s:.6f}"
        cos_val = f"{c:.6f}"
        unit_x = f"{c:.6f}"
        unit_y = f"{s:.6f}"

    row = {
        "deg(°)": deg,
    }
    if show_radians:
        row["rad"] = f"{rad:.6f}"
    row["sin(θ)"] = sin_val
    if show_cos:
        row["cos(θ)"] = cos_val
    row["unit_x (cos)"] = unit_x
    row["unit_y (sin)"] = unit_y

    rows.append(row)

df = pd.DataFrame(rows)

# 単位円の簡易描画（matplotlib） — まず円を上に表示
try:
    import matplotlib.pyplot as plt
    import numpy as np
    import matplotlib as mpl
    import matplotlib.font_manager as fm

    # システムに存在する日本語対応フォントを候補から探し、見つかればそれを使います。
    candidates = [
        "Hiragino Kaku Gothic ProN",
        "Hiragino Sans",
        "AppleGothic",
        "Noto Sans CJK JP",
        "IPAPGothic",
        "Yu Gothic",
        "TakaoPGothic",
        "VL Gothic",
        "DejaVu Sans",
    ]

    found_font_path = None
    found_font_name = None
    # combine ttf/otf search results
    font_files = fm.findSystemFonts(fontpaths=None, fontext="ttf") + fm.findSystemFonts(
        fontpaths=None, fontext="otf"
    )
    for fp in font_files:
        try:
            name = fm.FontProperties(fname=fp).get_name()
        except Exception:
            continue
        lname = name.lower()
        for cand in candidates:
            if cand.lower() in lname:
                found_font_path = fp
                found_font_name = name
                break
        if found_font_path:
            break

    mpl.rcParams["font.family"] = "sans-serif"
    if found_font_name:
        mpl.rcParams["font.sans-serif"] = [found_font_name, "DejaVu Sans"]
        font_prop = fm.FontProperties(fname=found_font_path)
    else:
        mpl.rcParams["font.sans-serif"] = ["DejaVu Sans"]
        font_prop = None

    # 負号が化けることを防ぐ
    mpl.rcParams["axes.unicode_minus"] = False

    fig, ax = plt.subplots(figsize=(4, 4))
    # 単位円
    theta = np.linspace(0, 2 * np.pi, 400)
    ax.plot(np.cos(theta), np.sin(theta), color="#777777")
    # x/y 軸
    ax.axhline(0, color="#cccccc")
    ax.axvline(0, color="#cccccc")

    # ハイライト点
    ha = math.radians(highlight_angle)
    hx = math.cos(ha)
    hy = math.sin(ha)
    ax.plot([0, hx], [0, hy], color="#1f77b4", linewidth=2)
    ax.scatter([hx], [hy], color="#d62728", zorder=5)

    ax.set_aspect("equal", "box")
    ax.set_xlim(-1.1, 1.1)
    ax.set_ylim(-1.1, 1.1)
    ax.set_xlabel("x = cosθ")
    ax.set_ylabel("y = sinθ")
    # タイトルは matplotlib に描画すると環境依存で文字化けすることがあるため
    # Streamlit 側で描画する（ブラウザのフォントで表示される）
    st.subheader(
        f"単位円 — ハイライト: {highlight_angle}° (cos(θ)={hx:.3f}, sin(θ)={hy:.3f})"
    )
    st.pyplot(fig)
except Exception:
    # matplotlib が無いなどで描画できない場合は、フォールバックで SVG による描画を行います。
    try:
        from streamlit import components

        # SVG を生成して埋め込む
        size = 420
        cx = cy = size // 2
        r = int(size * 0.4)
        ha = math.radians(highlight_angle)
        hx = cx + r * math.cos(ha)
        hy = cy - r * math.sin(ha)

        svg = f'''<svg width="{size}" height="{size}" viewBox="0 0 {size} {size}" xmlns="http://www.w3.org/2000/svg">
  <rect width="100%" height="100%" fill="white" />
  <!-- circle -->
  <circle cx="{cx}" cy="{cy}" r="{r}" stroke="#777777" stroke-width="2" fill="none" />
  <!-- axes -->
  <line x1="0" y1="{cy}" x2="{size}" y2="{cy}" stroke="#cccccc" stroke-width="1" />
  <line x1="{cx}" y1="0" x2="{cx}" y2="{size}" stroke="#cccccc" stroke-width="1" />
  <!-- radius -->
  <line x1="{cx}" y1="{cy}" x2="{hx:.3f}" y2="{hy:.3f}" stroke="#1f77b4" stroke-width="3" />
  <!-- point -->
  <circle cx="{hx:.3f}" cy="{hy:.3f}" r="6" fill="#d62728" />
  <!-- labels -->
  <text x="{cx + r + 8}" y="{cy}" font-size="12" fill="#333">x = cosθ</text>
  <text x="{cx}" y="{cy - r - 8}" font-size="12" fill="#333">y = sinθ</text>
</svg>'''
        components.html(svg, height=size + 20)
        # SVG 上のタイトルも Streamlit 側で表示（SVG 内には日本語を入れない）
        st.subheader(
            f"単位円 — ハイライト: {highlight_angle}° (x={(math.cos(ha)):.3f}, y={(math.sin(ha)):.3f})"
        )
    except Exception:
        st.info(
            "単位円を描画できませんでした（matplotlib/numpy が無く、SVG 埋め込みにも失敗しました）。"
        )

# テーブル表示（ハイライト行）
try:

    def _highlight_row(row):
        try:
            deg = int(row["deg(°)"])
        except Exception:
            return ["" for _ in row]
        if deg == int(highlight_angle):
            return ["background-color: #fff2a8" for _ in row]
        return ["" for _ in row]

    styler = df.style.apply(_highlight_row, axis=1)
    st.write(styler)
except Exception:
    # フォールバック: シンプルなテーブル表示
    st.table(rows)
