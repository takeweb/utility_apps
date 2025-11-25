import streamlit as st

# --- アプリの基本設定 ---
st.set_page_config(page_title="UNIXパーミッション変換アプリ", page_icon="🛃")

# --- タイトル ---
st.title("🛃 UNIXパーミッション変換アプリ")
st.caption(
    "R, W, X のチェックボックスでパーミッションを計算、または数値からパーミッションを確認できます。"
)

st.divider()  # 区切り線

# --- チェックボックスから数値を計算 ---
st.subheader("1. チェックボックスから数値を計算")

col1, col2, col3 = st.columns(3)

with col1:
    st.text("所有者 (Owner)")
    owner_r = st.checkbox("読み取り (R)", key="owner_r")
    owner_w = st.checkbox("書き込み (W)", key="owner_w")
    owner_x = st.checkbox("実行 (X)", key="owner_x")

with col2:
    st.text("グループ (Group)")
    group_r = st.checkbox("読み取り (R)", key="group_r")
    group_w = st.checkbox("書き込み (W)", key="group_w")
    group_x = st.checkbox("実行 (X)", key="group_x")

with col3:
    st.text("その他 (Others)")
    others_r = st.checkbox("読み取り (R)", key="others_r")
    others_w = st.checkbox("書き込み (W)", key="others_w")
    others_x = st.checkbox("実行 (X)", key="others_x")

if st.button("計算"):
    owner_value = (4 if owner_r else 0) + (2 if owner_w else 0) + (1 if owner_x else 0)
    group_value = (4 if group_r else 0) + (2 if group_w else 0) + (1 if group_x else 0)
    others_value = (
        (4 if others_r else 0) + (2 if others_w else 0) + (1 if others_x else 0)
    )

    permission_value = f"{owner_value}{group_value}{others_value}"
    st.success(f"計算結果: {permission_value}")

st.divider()

# --- 数値からパーミッションを確認 ---
st.subheader("2. 数値からパーミッションを確認")

permission_input = st.text_input(
    "パーミッション数値を入力 (例: 755)", max_chars=3, key="perm_input"
)

if st.button("確認"):
    if permission_input.isdigit() and len(permission_input) == 3:
        owner_value = int(permission_input[0])
        group_value = int(permission_input[1])
        others_value = int(permission_input[2])

        owner_perm = f"{'R' if owner_value & 4 else '-'}{'W' if owner_value & 2 else '-'}{'X' if owner_value & 1 else '-'}"
        group_perm = f"{'R' if group_value & 4 else '-'}{'W' if group_value & 2 else '-'}{'X' if group_value & 1 else '-'}"
        others_perm = f"{'R' if others_value & 4 else '-'}{'W' if others_value & 2 else '-'}{'X' if others_value & 1 else '-'}"

        st.success("パーミッション:")
        st.text(f"所有者 (Owner): {owner_perm}")
        st.text(f"グループ (Group): {group_perm}")
        st.text(f"その他 (Others): {others_perm}")
    else:
        st.error("有効な3桁の数値を入力してください。")
