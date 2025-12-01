import streamlit as st
from tools.ascii_converter import (
    convert_string_to_ascii_binary_hex,
    convert_ascii_to_string,
    convert_binary_to_string,
    convert_hex_to_string,
)

# --- アプリの基本設定 ---
st.set_page_config(page_title="ASCII変換アプリ", page_icon="🔤")

# --- タイトル ---
st.title("🔤 ASCII変換アプリ")
st.caption("文字列をASCIIコード、2進数、16進数に相互変換します。")

st.divider()  # 区切り線

# --- 変換モードの選択 ---
st.subheader("1. 変換モードを選択")
mode = st.radio(
    "何を変換しますか？",
    (
        "文字列 を ASCII/2進/16進 へ",
        "ASCII を 文字列 へ",
        "2進数 を 文字列 へ",
        "16進数 を 文字列 へ",
    ),
    horizontal=True,
    label_visibility="collapsed",
)

st.divider()

# --- メインの処理 ---
st.subheader("2. 入力")

if mode == "文字列 を ASCII/2進/16進 へ":
    input_string = st.text_input("変換したい文字列を入力してください")

    if input_string:
        ascii_codes, binary_codes, hex_codes = convert_string_to_ascii_binary_hex(
            input_string
        )

        # ASCIIコードと元の文字を対応付けたリストを作成
        ascii_with_chars = [
            f"{char}: ({ascii_code})"
            for char, ascii_code in zip(input_string, ascii_codes)
        ]

        # 2進数と元の文字を対応付けたリストを作成
        binary_with_chars = [
            f"{char}: ({binary_code})"
            for char, binary_code in zip(input_string, binary_codes)
        ]

        # 16進数と元の文字を対応付けたリストを作成
        hex_with_chars = [
            f"{char}: ({hex_code})" for char, hex_code in zip(input_string, hex_codes)
        ]

        st.subheader("変換結果")
        col1, col2, col3 = st.columns(3)
        col1.write("**ASCIIコード:**")
        col1.code("".join(map(str, ascii_codes)))
        col1.code("\n".join(ascii_with_chars))
        col2.write("**2進数:**")
        col2.code("".join(map(str, binary_codes)))
        col2.code("\n".join(binary_with_chars))
        col3.write("**16進数:**")
        col3.code("".join(map(str, hex_codes)))
        col3.code("\n".join(hex_with_chars))

elif mode == "ASCII を 文字列 へ":
    ascii_input = st.text_input("ASCIIコードを入力してください (例: 656667)")

    if ascii_input:
        # 入力文字列を2文字ずつに分割
        ascii_codes = [ascii_input[i : i + 2] for i in range(0, len(ascii_input), 2)]
        result = convert_ascii_to_string(ascii_codes)

        if result is not None:
            st.subheader("変換結果")
            st.write("**文字列:**", result)
        else:
            st.error("無効なASCIIコードが含まれています。")

elif mode == "2進数 を 文字列 へ":
    binary_input = st.text_input(
        "2進数を入力してください (例: 010000010100001001000011)"
    )

    if binary_input:
        # 入力文字列を8文字ずつに分割
        binary_codes = [binary_input[i : i + 8] for i in range(0, len(binary_input), 8)]
        result = convert_binary_to_string(binary_codes)

        if result is not None:
            st.subheader("変換結果")
            st.write("**文字列:**", result)
        else:
            st.error("無効な2進数が含まれています。")

elif mode == "16進数 を 文字列 へ":
    hex_input = st.text_input("16進数を入力してください (例: 414243)")

    if hex_input:
        # 入力文字列を2文字ずつに分割
        hex_codes = [hex_input[i : i + 2] for i in range(0, len(hex_input), 2)]
        result = convert_hex_to_string(hex_codes)

        if result is not None:
            st.subheader("変換結果")
            st.write("**文字列:**", result)
        else:
            st.error("無効な16進数が含まれています。")
