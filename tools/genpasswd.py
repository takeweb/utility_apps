import random
import string
import streamlit as st


def main():
    # --- アプリの基本設定 ---
    st.set_page_config(page_title="パスワード生成アプリ", page_icon="🔐")

    st.title("🔐 パスワードジェネレーター")

    # パスワード生成オプションの設定
    length = st.slider("パスワードの長さ", 8, 32, 16)
    include_numbers = st.checkbox("数字を含める", value=True)
    include_special_chars = st.checkbox("特殊文字を含める", value=True)

    # st.text_input の代わりにこれを使う
    selected_special_chars = ""
    if include_special_chars:
        all_special_chars = list(string.punctuation)
        selected_list = st.multiselect(
            "含める特殊文字を選択してください",
            options=all_special_chars,
            default=all_special_chars,  # デフォルトで全て選択
        )
        # st.multiselect はリストを返すので、文字列に結合する
        selected_special_chars = "".join(selected_list)

    if st.button("パスワード生成！！"):
        password = generate_password(
            length, include_numbers, include_special_chars, selected_special_chars
        )
        if password:
            col1, col2 = st.columns([2, 3])
            col1.success("生成されたパスワード:")
            col2.code(password)
        else:
            st.error(
                "Cannot generate password. Please select at least one character type (or add special characters)."
            )


def generate_password(
    length, include_numbers, include_special_chars, selected_special_chars
):
    characters = string.ascii_letters

    if include_numbers:
        characters += string.digits

    # CheckboxがON で、かつ text_input に何かしらの文字が入力されている場合
    if include_special_chars and selected_special_chars:
        characters += selected_special_chars

    # もし使用可能な文字が空だった場合（例：全部OFFにして記号も空にした）
    if not characters:
        return None  # エラー処理のためにNoneを返す

    password = "".join(random.choice(characters) for _ in range(length))
    return password
