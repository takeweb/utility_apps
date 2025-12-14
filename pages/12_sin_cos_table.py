import math
import streamlit as st
import pandas as pd

st.set_page_config(page_title="sin、cosと単位円の角度の関係", page_icon="⚪️")

st.title("⚪️ sin、cosと単位円の角度の関係")
st.caption("度(°) とラジアン、sin/cos、単位円上の座標を確認する表")

# 設定エリア（上段にまとめる）
settings_cols = st.columns([1, 1, 1])
# 表示ステップは 15° に固定
step = 15
show_radians = settings_cols[0].checkbox("ラジアン表示有り", value=True)
show_cos = settings_cols[1].checkbox("cos表示あり", value=True)
show_exact = settings_cols[2].checkbox(
    "計算式表示",
    value=True,
    help="主要角（15°刻み）の計算式で表示する（√や分数など）。チェックを外すと小数表示になります。",
)

# ハイライト角選択（step に連動） — セレクトボックスからスライダーに変更
# session_state に既定値をセットしてから、slider は key のみ指定する
if "highlight_angle" not in st.session_state:
    st.session_state["highlight_angle"] = 30
# スライダーで角度を選択（step に従う）
st.slider(
    "ハイライトする角度 (°)",
    min_value=0,
    max_value=360,
    step=step,
    key="highlight_angle",
)
highlight_angle = st.session_state["highlight_angle"]

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

# 表と単位円を縦に並べて表示
st.subheader(f"0° 〜 360° (step {step}°)")

# 表データを作成
rows = []
for deg in angles:
    rad = math.radians(deg)
    s = math.sin(rad)
    c = math.cos(rad)

    if show_exact and deg in exact_map:
        sin_val = exact_map[deg][0]
        cos_val = exact_map[deg][1]
    else:
        sin_val = f"{s:.6f}"
        cos_val = f"{c:.6f}"

    row = {
        "deg(°)": deg,
    }
    if show_radians:
        row["rad"] = f"{rad:.6f}"
    row["sin(θ)"] = sin_val
    if show_cos:
        row["cos(θ)"] = cos_val

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

    # マーカーサイズは角度に依らず小さい一定値にする（赤い点を小さく統一）
    s_mark = 30  # matplotlib scatter の s は面積 (points^2)
    r_svg = 3  # SVG での円半径
    # 半径（原点から点へ）
    ax.plot([0, hx], [0, hy], color="#1f77b4", linewidth=2)
    ax.scatter([hx], [hy], color="#d62728", zorder=5, s=s_mark)

    # 直角三角形の辺（x 軸への射影と垂直辺）を描画
    # 横辺: (0,0) -> (hx,0)
    ax.plot([0, hx], [0, 0], color="#2ca02c", linewidth=2)
    # 縦辺: (hx,0) -> (hx,hy)
    ax.plot([hx, hx], [0, hy], color="#2ca02c", linewidth=2)
    # 三角形の内部を薄く塗る（視覚的補助）
    ax.fill([0, hx, hx], [0, 0, hy], color="#2ca02c", alpha=0.08)

    # sin/cos の数値ラベルを追加（日本語やギリシャ文字は環境依存で化ける可能性があるため英字と数値で表示）
    try:
        # 横辺の中央に cos 値を表示
        ax.text(hx / 2.0, -0.06, f"cos={hx:.3f}", ha="center", va="top", fontsize=9)
        # 縦辺の中央に sin 値を表示（x 側に寄せる）
        x_label_pos = hx + 0.03 if hx >= 0 else hx - 0.03
        ax.text(
            x_label_pos,
            hy / 2.0,
            f"sin={hy:.3f}",
            ha="left" if hx >= 0 else "right",
            va="center",
            fontsize=9,
        )
    except Exception:
        pass

    ax.set_aspect("equal", "box")
    ax.set_xlim(-1.1, 1.1)
    ax.set_ylim(-1.1, 1.1)
    # 明示的にオートスケーリングを無効化して、角度変更時に表示領域が変わらないようにする
    try:
        ax.set_autoscale_on(False)
    except Exception:
        try:
            ax.autoscale(False)
        except Exception:
            pass
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

        # SVG 側のマーカーサイズも一定にする（matplotlib と同じサイズ）
        r_svg = 7

        svg = f'''<svg width="{size}" height="{size}" viewBox="0 0 {size} {size}" xmlns="http://www.w3.org/2000/svg">
        <rect width="100%" height="100%" fill="white" />
        <!-- circle -->
        <circle cx="{cx}" cy="{cy}" r="{r}" stroke="#777777" stroke-width="2" fill="none" />
        <!-- axes -->
        <line x1="0" y1="{cy}" x2="{size}" y2="{cy}" stroke="#cccccc" stroke-width="1" />
        <line x1="{cx}" y1="0" x2="{cx}" y2="{size}" stroke="#cccccc" stroke-width="1" />
        <!-- radius -->
        <line x1="{cx}" y1="{cy}" x2="{hx:.3f}" y2="{hy:.3f}" stroke="#1f77b4" stroke-width="3" />
        <!-- right-triangle legs -->
        <line x1="{cx}" y1="{cy}" x2="{hx:.3f}" y2="{cy}" stroke="#2ca02c" stroke-width="3" />
        <line x1="{hx:.3f}" y1="{cy}" x2="{hx:.3f}" y2="{hy:.3f}" stroke="#2ca02c" stroke-width="3" />
        <!-- fill triangle -->
        <polygon points="{cx},{cy} {hx:.3f},{cy} {hx:.3f},{hy:.3f}" fill="#2ca02c" fill-opacity="0.08" />
    <!-- point -->
    <circle cx="{hx:.3f}" cy="{hy:.3f}" r="{r_svg:.3f}" fill="#d62728" />
        <!-- labels -->
        <text x="{cx + r + 8}" y="{cy}" font-size="12" fill="#333">x = cosθ</text>
        <text x="{cx}" y="{cy - r - 8}" font-size="12" fill="#333">y = sinθ</text>
        <!-- numeric labels for cos/sin -->
        <text x="{(cx + hx) / 2.0:.3f}" y="{cy + 18}" font-size="12" fill="#2ca02c" text-anchor="middle">cos={math.cos(ha):.3f}</text>
        <text x="{hx + 12:.3f}" y="{(cy + hy) / 2.0:.3f}" font-size="12" fill="#2ca02c" text-anchor="start">sin={math.sin(ha):.3f}</text>
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
        # Streamlit のテーマを検出して、ライト/ダークで見やすい色を選択
        try:
            theme_base = st.get_option("theme.base")
        except Exception:
            theme_base = "light"

        if theme_base == "dark":
            # ダークモードでは薄いブルー系のハイライト（白文字上で十分なコントラスト）
            highlight_style = "background-color: rgba(31,119,180,0.25);"
        else:
            # ライトモードでは既存の黄色系ハイライト
            highlight_style = "background-color: #fff2a8;"

        if deg == int(highlight_angle):
            return [highlight_style for _ in row]
        return ["" for _ in row]

    styler = df.style.apply(_highlight_row, axis=1)
    st.write(styler)
except Exception:
    # フォールバック: シンプルなテーブル表示
    st.table(rows)
