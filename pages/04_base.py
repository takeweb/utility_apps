import streamlit as st
import re

# --- アプリの基本設定 ---
st.set_page_config(page_title="基数変換アプリ", page_icon="🔢")

# --- タイトル ---
st.title("🔢 基数変換アプリ")
st.caption("2進数、10進数、16進数、および固定小数点の変換を行います。")

st.divider()  # 区切り線

# --- 変換モードの選択 ---
st.subheader("1. 変換モードを選択")
mode = st.radio(
    "何を変換しますか？",
    (
        "2進数 を 10進/16進 へ",
        "10進数 を 2進/16進 へ",
        "16進数 を 2進/10進 へ",
        "16進 固定小数点 (8.8) を 10進 へ",
        "10進数 を 16進 固定小数点 (8.8) へ",
    ),
    horizontal=True,
    label_visibility="collapsed",
)

st.divider()

# --- メインの処理 ---
st.subheader("2. 数値を入力")

# モード 1: 2進数 → 10進/16進
if mode == "2進数 を 10進/16進 へ":
    binary_input = st.text_input(
        "変換したい2進数を入力してください",
        placeholder="例: 101101 または 0b101101",
        key="bin_in",
    )

    if binary_input:
        binary_input_cleaned = binary_input.strip()
        if binary_input_cleaned.startswith(("0b", "0B")):
            binary_input_cleaned = binary_input_cleaned[2:]

        if re.match(r"^[01]+$", binary_input_cleaned) and binary_input_cleaned:
            try:
                # 符号付き整数として解釈
                bit_length = 16  # 16ビット固定
                decimal_output = int(binary_input_cleaned, 2)
                if decimal_output & (1 << (bit_length - 1)):
                    decimal_output -= 1 << bit_length

                hex_output = hex(decimal_output & 0xFFFF)

                # 2進数を16桁固定に変更
                binary_output = "0b" + binary_input_cleaned.zfill(16)

                st.subheader("変換結果")
                col1, col2 = st.columns(2)
                col1.metric("10進数 (Decimal)", decimal_output)
                col2.metric("16進数 (Hexadecimal)", hex_output)

            except ValueError:
                st.error("数値が大きすぎるか、変換中にエラーが発生しました。")
            except Exception as e:
                st.error(f"予期しないエラーが発生しました: {e}")
        elif not binary_input_cleaned:
            pass  # 入力が空の場合は何もしない
        else:
            st.warning("入力は0と1のみにしてください。")

# モード 2: 10進数 → 2進/16進 (★修正箇所)
elif mode == "10進数 を 2進/16進 へ":
    decimal_input = st.text_input(
        "変換したい10進数を入力してください", placeholder="例: 45", key="dec_in"
    )

    if decimal_input:
        try:
            decimal_value = int(decimal_input)
            if decimal_value < 0:
                # 負の値の場合の処理（2の補数表現で16桁固定）
                binary_output = "0b" + bin(decimal_value & 0xFFFF)[2:].zfill(16)
                hex_output = hex(decimal_value & 0xFFFF)
            else:
                # 正の値の場合の処理（16桁固定）
                binary_output = "0b" + bin(decimal_value & 0xFFFF)[2:].zfill(16)
                hex_output = hex(decimal_value & 0xFFFF)

            st.subheader("変換結果")
            col1, col2 = st.columns(2)
            col1.metric("2進数 (Binary)", binary_output)
            col2.metric("16進数 (Hexadecimal)", hex_output)

        except ValueError:
            st.warning("有効な10進数（半角数字）を入力してください。")

# モード 3: 16進数 → 2進/10進
elif mode == "16進数 を 2進/10進 へ":
    hex_input = st.text_input(
        "変換したい16進数を入力してください",
        placeholder="例: 1973 または 0x1973",
        key="hex_in",
    )

    if hex_input:
        hex_input_cleaned = hex_input.strip()

        if hex_input_cleaned.startswith(("0x", "0X")):
            hex_input_cleaned = hex_input_cleaned[2:]

        if re.match(r"^[0-9a-fA-F]+$", hex_input_cleaned) and hex_input_cleaned:
            try:
                # 16進 -> 10進（符号付き整数として解釈）
                decimal_value = int(hex_input_cleaned, 16)  # decimal_valueを正しく定義
                bit_length = 16  # 16ビット固定
                if decimal_value & (1 << (bit_length - 1)):
                    decimal_value -= 1 << bit_length

                # 10進 -> 2進
                binary_output = "0b" + bin(decimal_value & 0xFFFF)[2:].zfill(16)

                st.subheader("変換結果")
                col1, col2 = st.columns(2)
                col1.metric("2進数 (Binary)", binary_output)
                col2.metric("10進数 (Decimal)", decimal_value)

            except ValueError:
                st.error("数値が大きすぎるか、変換中にエラーが発生しました。")
            except Exception as e:
                st.error(f"予期しないエラーが発生しました: {e}")

# モード 4: 16進 固定小数点 (8.8) → 10進
elif mode == "16進 固定小数点 (8.8) を 10進 へ":
    q88_input = st.text_input(
        "変換したい16進固定小数点(8.8)の値を入力 (例: C9A0, 0xC9A0, C9.A0)",
        placeholder="16進数 4桁で入力 (0x, . は自動除去)",
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
                integer_part_hex = cleaned_input[0:2]
                integer_part_dec = int(integer_part_hex, 16)

                fractional_part_hex = cleaned_input[2:4]
                fractional_part_dec_int = int(fractional_part_hex, 16)

                fractional_part_dec = fractional_part_dec_int / 256.0

                if integer_part_dec >= 128:  # 符号付き整数として解釈
                    integer_part_dec -= 256

                final_decimal_value = integer_part_dec + fractional_part_dec

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

# モード 5: 10進数 → 16進 固定小数点 (8.8)
elif mode == "10進数 を 16進 固定小数点 (8.8) へ":
    decimal_input = st.text_input(
        "変換したい10進数を入力してください (例: -201.625)",
        placeholder="例: -201.625",
        key="dec_to_q88",
    )

    if decimal_input:
        try:
            decimal_value = float(decimal_input)

            if decimal_value < -128 or decimal_value >= 128:
                st.warning("入力値は-128以上128未満である必要があります。")
            else:
                if decimal_value < 0:
                    decimal_value += 256  # 2の補数表現に変換

                integer_part = int(decimal_value)
                fractional_part = (
                    decimal_value - integer_part
                )  # 修正: int(decimal_input) -> integer_part
                fractional_part_hex = int(round(fractional_part * 256))

                # 丸め処理によるオーバーフローを防ぐ
                if fractional_part_hex == 256:
                    fractional_part_hex = 0
                    integer_part += 1

                q88_hex = f"0x{integer_part:02X}{fractional_part_hex:02X}"

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
