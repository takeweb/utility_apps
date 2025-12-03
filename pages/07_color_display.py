import streamlit as st

# --- アプリの基本設定 ---
st.set_page_config(page_title="色表示アプリ", page_icon="🎨")

# --- タイトル ---
st.title("🎨 色表示アプリ")
st.caption("16進数やRGB値から色を表示します。")

# --- 16進数から色を表示 ---
with st.expander("**16進数から色を表示**", expanded=True):
    hex_color = st.text_input(
        "16進数カラーコードを入力 (例: #FF5733)", placeholder="#RRGGBB", key="hex_input"
    )

    if st.button("16進数で表示", key="hex_button"):
        if hex_color.startswith("#") and len(hex_color) == 7:
            try:
                st.success("入力された色:")
                st.color_picker("色プレビュー", hex_color, disabled=True)
            except ValueError:
                st.error("有効な16進数カラーコードを入力してください。")
        else:
            st.error("有効な16進数カラーコードを入力してください (例: #RRGGBB)。")

# --- RGBから色を表示 ---
with st.expander("**RGBから色を表示**", expanded=True):
    col1, col2, col3 = st.columns(3)

    with col1:
        r = st.number_input("R (赤)", min_value=0, max_value=255, step=1, key="r_input")
    with col2:
        g = st.number_input("G (緑)", min_value=0, max_value=255, step=1, key="g_input")
    with col3:
        b = st.number_input("B (青)", min_value=0, max_value=255, step=1, key="b_input")

    if st.button("RGBで表示", key="rgb_button"):
        try:
            hex_color = f"#{int(r):02X}{int(g):02X}{int(b):02X}"
            st.success("入力された色:")
            st.color_picker("色プレビュー", hex_color, disabled=True)
        except ValueError:
            st.error("有効なRGB値を入力してください。")

# --- 色パレットから色を選択 ---
with st.expander("**色パレットから色を選択**", expanded=True):
    selected_color = st.color_picker("色を選択", "#FFFFFF", key="color_picker")

    if selected_color:
        # 16進数カラーコードを表示
        st.text(f"選択された色 (16進数): {selected_color}")

        # RGB値を計算して表示
        r = int(selected_color[1:3], 16)
        g = int(selected_color[3:5], 16)
        b = int(selected_color[5:7], 16)
        st.text(f"選択された色 (RGB): R={r}, G={g}, B={b}")
