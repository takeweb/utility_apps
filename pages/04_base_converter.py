import streamlit as st
import re
from tools.base_converter import (
    convert_bin_to_dec_hex,
    convert_dec_to_bin_hex,
    convert_hex_to_bin_dec,
    convert_q88_to_dec,
    convert_dec_to_q88,
)

# --- アプリの基本設定 ---
st.set_page_config(page_title="基数変換アプリ", page_icon="🔢")

# --- タイトル ---
st.title("🔢 基数変換アプリ")
st.caption("2進数、10進数、16進数、および固定小数点の変換を行います。")

# --- 変換モードの選択 ---
st.subheader("1. 変換モードを選択")

options = [
    ("10進数 を 2進/16進 へ", "DEC_TO_BIN_HEX"),
    ("2進数 を 10進/16進 へ", "BIN_TO_DEC_HEX"),
    ("16進数 を 2進/10進 へ", "HEX_TO_BIN_DEC"),
    ("16進 固定小数点 (8.8) を 10進 へ", "FIXED88_TO_DEC"),
    ("10進数 を 16進 固定小数点 (8.8) へ", "DEC_TO_FIXED88"),
]

mode = st.radio(
    "何を変換しますか？",
    options,
    format_func=lambda x: x[0],
    horizontal=True,
    label_visibility="collapsed",
)

# --- メインの処理 ---
match mode[1]:
    case "DEC_TO_BIN_HEX":
        # 10進数 → 2進/16進
        st.divider()
        st.subheader("2. ビット数を選択")
        bit_length = st.slider("2進数でのビット数", min_value=4, max_value=16, value=16, step=4)  # ビット数の設定

        st.divider()
        st.subheader("3. 数値を入力")
        decimal_input = st.text_input("変換したい10進数を入力してください", placeholder="例: 45", key="dec_in")

        if decimal_input:
            try:
                # 変換関数の呼び出し
                binary_output, hex_output = convert_dec_to_bin_hex(int(decimal_input), bit_length)

                st.subheader("変換結果")
                col1, col2 = st.columns(2)
                col1.metric("2進数 (Binary)", binary_output)
                col2.metric("16進数 (Hexadecimal)", hex_output)

            except ValueError:
                st.warning("有効な10進数（半角数字）を入力してください。")

    case "BIN_TO_DEC_HEX":
        # 2進数 → 10進/16進
        st.divider()
        st.subheader("2. 数値を入力")
        binary_input = st.text_input(
            "変換したい2進数を入力してください (例: 101101 または 0b101101)",
            placeholder="例: 101101 または 0b101101",
            key="bin_in",
        )

        if binary_input:
            binary_input_cleaned = binary_input.strip()
            if binary_input_cleaned.startswith(("0b", "0B")):
                binary_input_cleaned = binary_input_cleaned[2:]

            if re.match(r"^[01]+$", binary_input_cleaned) and binary_input_cleaned:
                try:
                    # 変換関数の呼び出し
                    (decimal_signed, decimal_unsigned, hex) = convert_bin_to_dec_hex(
                        binary_input_cleaned
                    )

                    st.subheader("変換結果")
                    col1, col2, col3 = st.columns(3)
                    col1.metric("10進数 (Signed Decimal)", decimal_signed)
                    col2.metric("10進数 (Unsigned Decimal)", decimal_unsigned)
                    col3.metric("16進数 (Hexadecimal)", hex)

                except ValueError:
                    st.error("数値が大きすぎるか、変換中にエラーが発生しました。")
                except Exception as e:
                    st.error(f"予期しないエラーが発生しました: {e}")
            elif not binary_input_cleaned:
                pass
            else:
                st.warning("入力は0と1のみにしてください。")

    case "HEX_TO_BIN_DEC":
        # 16進数 → 2進/10進
        st.divider()
        st.subheader("2. 数値を入力")
        hex_input = st.text_input(
            "変換したい16進数を入力してください (例: 0x1973)",
            placeholder="例: 1973 または 0x1973",
            key="hex_in",
        )

        if hex_input:
            hex_input_cleaned = hex_input.strip()

            if hex_input_cleaned.startswith(("0x", "0X")):
                hex_input_cleaned = hex_input_cleaned[2:]

            if re.match(r"^[0-9a-fA-F]+$", hex_input_cleaned) and hex_input_cleaned:
                try:
                    # 変換関数の呼び出し
                    binary_output, decimal_value_signed, decimal_value_unsigned = (
                        convert_hex_to_bin_dec(hex_input_cleaned)
                    )

                    st.subheader("変換結果")
                    col1, _ = st.columns([3, 1])  # col1を広くするための調整
                    col1.metric("2進数 (Binary)", binary_output)
                    col2, col3 = st.columns(2)
                    col2.metric("10進数 (Signed Decimal)", decimal_value_signed)
                    col3.metric("10進数 (Unsigned Decimal)", decimal_value_unsigned)

                except ValueError:
                    st.error("数値が大きすぎるか、変換中にエラーが発生しました。")
                except Exception as e:
                    st.error(f"予期しないエラーが発生しました: {e}")

    case "FIXED88_TO_DEC":
        # 16進 固定小数点 (8.8) → 10進
        st.divider()
        st.subheader("2. 数値を入力")
        q88_input = st.text_input(
            "変換したい16進固定小数点(8.8)の値を入力 (例: 0x1973)",
            placeholder="16進数 4桁で入力 (0x, . は自動除去) (例: 0x1973)",
            key="q88_in",
        )

        if q88_input:
            cleaned_input = q88_input.strip().replace(".", "")

            if cleaned_input.startswith(("0x", "0X")):
                cleaned_input = cleaned_input[2:]

            if not re.match(r"^[0-9a-fA-F]+$", cleaned_input) and cleaned_input:
                st.warning("入力は有効な16進数（0-9, a-f, A-F）にしてください。")

            elif len(cleaned_input) != 4:
                st.warning("固定小数点8.8形式は、16進数4桁 (例: C9A0) で入力してください。")

            else:
                try:
                    # 変換関数の呼び出し
                    (
                        final_decimal_value,
                        integer_part_dec,
                        fractional_part_dec_int,
                        fractional_part_dec,
                    ) = convert_q88_to_dec(cleaned_input)
                    integer_part_hex = cleaned_input[0:2]
                    fractional_part_hex = cleaned_input[2:4]

                    st.subheader("変換結果 (10進数)")
                    st.metric("10進数 (Decimal)", f"{final_decimal_value:.10f}")

                    with st.expander("計算詳細"):
                        st.text(f"入力 (16進): {cleaned_input}")
                        st.text(
                            f"整数部 (16進): {integer_part_hex} -> (10進): {integer_part_dec}"
                        )
                        st.text(
                            f"小数部 (16進): {fractional_part_hex} -> (10進整数): {fractional_part_dec_int}"
                        )
                        st.text(
                            f"小数部 (10進): {fractional_part_dec_int} / 256 = {fractional_part_dec}"
                        )
                        st.text(
                            f"合計 (10進): {integer_part_dec} + {fractional_part_dec} = {final_decimal_value}"
                        )
                except Exception as e:
                    st.error(f"変換中にエラーが発生しました: {e}")

    case "DEC_TO_FIXED88":
        # 10進数 を 16進 固定小数点 (8.8) へ
        st.divider()
        st.subheader("2. 数値を入力")
        decimal_input = st.text_input(
            "変換したい10進数を入力してください (例: 25.44)",
            placeholder="例: 25.44",
            key="dec_to_q88",
        )

        if decimal_input:
            try:
                decimal_value = float(decimal_input)

                if decimal_value < -128 or decimal_value >= 128:
                    st.warning("入力値は-128以上128未満である必要があります。")
                else:
                    # 変換関数の呼び出し
                    q88_hex, integer_part, fractional_part_hex_int, fractional_part = (
                        convert_dec_to_q88(decimal_value)
                    )
                    fractional_part_hex = int(round(fractional_part * 256))

                    st.subheader("変換結果 (16進 固定小数点 8.8)")
                    st.metric("16進数 (Hexadecimal)", q88_hex)

                    with st.expander("計算詳細"):
                        st.text(f"入力 (10進): {decimal_input}")
                        st.text(f"整数部: {integer_part} -> (16進): {integer_part:02X}")
                        st.text(
                            f"小数部: {fractional_part} -> (16進整数): {fractional_part_hex:02X}"
                        )
                        st.text(f"合計 (16進): {q88_hex}")

            except ValueError:
                st.error("有効な10進数を入力してください。")

    case _:
        st.error("不正な mode_code")
