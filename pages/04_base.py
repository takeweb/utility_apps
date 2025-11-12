import streamlit as st
import re # 入力バリデーション（検証）用

# --- アプリの基本設定 ---
st.set_page_config(
    page_title="基数変換アプリ",
    page_icon="🔢"
)

# --- タイトル ---
st.title('🔢 基数変換アプリ')
st.caption('2進数、10進数、16進数、および固定小数点の変換を行います。')

st.divider() # 区切り線

# --- 変換モードの選択 ---
st.subheader("1. 変換モードを選択")
mode = st.radio(
    "何を変換しますか？",
    (
        '2進数 を 10進/16進 へ',
        '10進数 を 2進数 へ',
        '16進数 を 2進数 へ',
        '16進 固定小数点 (8.8) を 10進 へ'
    ),
    horizontal=True,
    label_visibility="collapsed"
)

st.divider()

# --- メインの処理 ---
st.subheader("2. 数値を入力")

# モード 1: 2進数 → 10進/16進 (★修正箇所)
if mode == '2進数 を 10進/16進 へ':
    binary_input = st.text_input(
        '変換したい2進数を入力してください',
        placeholder='例: 101101 または 0b101101', # プレースホルダーを修正
        key='bin_in'
    )

    if binary_input:
        # 入力クレンジング
        binary_input_cleaned = binary_input.strip()

        # ★ '0b' または '0B' があれば除去
        if binary_input_cleaned.startswith(('0b', '0B')):
            binary_input_cleaned = binary_input_cleaned[2:]

        # バリデーション (クレンジング後の文字列を使用)
        if re.match(r'^[01]+$', binary_input_cleaned):
            try:
                # 変換 (クレンジング後の文字列を使用)
                decimal_output = int(binary_input_cleaned, 2)
                hex_output = hex(decimal_output)

                st.subheader('変換結果')
                col1, col2 = st.columns(2)
                col1.metric("10進数 (Decimal)", decimal_output)
                col2.metric("16進数 (Hexadecimal)", hex_output)

            except ValueError:
                st.error('数値が大きすぎるか、変換中にエラーが発生しました。')
        else:
            if binary_input_cleaned: # プレフィックス除去後に何か残っている場合
                st.warning('入力は0と1のみにしてください。')

# モード 2: 10進数 → 2進数
elif mode == '10進数 を 2進数 へ':
    decimal_input = st.text_input(
        '変換したい10進数を入力してください',
        placeholder='例: 45',
        key='dec_in'
    )

    if decimal_input:
        try:
            decimal_value = int(decimal_input)
            if decimal_value < 0:
                st.warning("正の整数を入力してください。")
            else:
                binary_output = bin(decimal_value)[2:]
                st.subheader('変換結果')
                st.metric("2進数 (Binary)", binary_output)

        except ValueError:
            st.warning('有効な10進数（半角数字）を入力してください。')

# モード 3: 16進数 → 2進数
elif mode == '16進数 を 2進数 へ':
    hex_input = st.text_input(
        '変換したい16進数を入力してください',
        placeholder='例: 1973 または 0x1973',
        key='hex_in'
    )

    if hex_input:
        hex_input_cleaned = hex_input.strip()

        if hex_input_cleaned.startswith(('0x', '0X')):
            hex_input_cleaned = hex_input_cleaned[2:]

        if re.match(r'^[0-9a-fA-F]+$', hex_input_cleaned):
            try:
                decimal_value = int(hex_input_cleaned, 16)
                binary_shortest = bin(decimal_value)[2:]

                num_hex_digits = len(hex_input_cleaned)
                required_bits = num_hex_digits * 4
                binary_output = binary_shortest.zfill(required_bits)

                st.subheader('変換結果')
                st.metric("2進数 (Binary)", binary_output)

            except ValueError:
                st.warning('有効な16進数を入力してください。')
        else:
            if hex_input_cleaned:
                st.warning('入力は有効な16進数（0-9, a-f, A-F）にしてください。')

# モード 4: 16進 固定小数点 (8.8) → 10進
elif mode == '16進 固定小数点 (8.8) を 10進 へ':
    q88_input = st.text_input(
        '変換したい16進固定小数点(8.8)の値を入力 (例: C9A0, 0xC9A0, C9.A0)',
        placeholder='16進数 4桁で入力 (0x, . は自動除去)',
        key='q88_in'
    )

    if q88_input:
        cleaned_input = q88_input.strip().replace('.', '')

        if cleaned_input.startswith(('0x', '0X')):
            cleaned_input = cleaned_input[2:]

        if not re.match(r'^[0-9a-fA-F]+$', cleaned_input) and cleaned_input:
            st.warning('入力は有効な16進数（0-9, a-f, A-F）にしてください。')

        elif len(cleaned_input) != 4:
            st.warning('固定小数点8.8形式は、16進数4桁 (例: C9A0) で入力してください。')

        else:
            try:
                #

                integer_part_hex = cleaned_input[0:2]
                integer_part_dec = int(integer_part_hex, 16)

                fractional_part_hex = cleaned_input[2:4]
                fractional_part_dec_int = int(fractional_part_hex, 16)

                fractional_part_dec = fractional_part_dec_int / 256.0

                final_decimal_value = integer_part_dec + fractional_part_dec

                st.subheader('変換結果 (10進数)')
                st.metric("10進数 (Decimal)", f"{final_decimal_value:.10f}")

                with st.expander("計算詳細"):
                    st.text(f"入力 (16進): {cleaned_input}")
                    st.text(f"整数部 (16進): {integer_part_hex} -> (10進): {integer_part_dec}")
                    st.text(f"小数部 (16進): {fractional_part_hex} -> (10進整数): {fractional_part_dec_int}")
                    st.text(f"小数部 (10進): {fractional_part_dec_int} / 256 = {fractional_part_dec}")
                    st.text(f"合計 (10進): {integer_part_dec} + {fractional_part_dec} = {final_decimal_value}")

            except Exception as e:
                st.error(f'変換中にエラーが発生しました: {e}')
