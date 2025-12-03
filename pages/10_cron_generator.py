import streamlit as st


# 単一選択、範囲選択、カスタム入力の切り替え関数
def select_single_range_or_custom(label, options):
    st.divider()  # 区切り線
    st.markdown(f"### {label}の選択")
    selection_type = st.radio(
        "選択タイプを選んでください",
        ["単一選択", "範囲選択", "カスタム入力"],
        horizontal=True,
        key=f"{label}_selection_type",  # 一意のキーを追加
        label_visibility="collapsed",
    )
    if selection_type == "単一選択":
        return st.selectbox(label, options, index=0)
    elif selection_type == "範囲選択":
        # 範囲選択の際に `'*'` を除外
        range_options = [opt for opt in options if opt != "*"]
        cols = st.columns(2)
        with cols[0]:
            from_value = st.selectbox(
                f"{label} (From)", range_options, index=0, key=f"{label}_from"
            )
        with cols[1]:
            to_value = st.selectbox(
                f"{label} (To)",
                range_options,
                index=len(range_options) - 1,
                key=f"{label}_to",
            )
        # 結果を統一して返す
        return f"{from_value}-{to_value}"

    elif selection_type == "カスタム入力":
        # カスタム入力も統一形式で返す
        custom_value = st.text_input(f"{label} (カスタム入力)", value="")
        # フィールド直下にエラーを出すためのプレースホルダ
        st.session_state[f"{label}_error_slot"] = st.empty()
        return custom_value


# 単一選択、範囲選択、カスタム入力の切り替え関数
def select_single_range_or_customw2(label, options):
    st.divider()  # 区切り線
    st.markdown(f"### {label}の選択")
    selection_type = st.radio(
        "選択タイプを選んでください",
        ["単一選択", "範囲選択", "カスタム入力"],
        horizontal=True,
        key=f"{label}_selection_type",  # 一意のキーを追加
        label_visibility="collapsed",
    )
    if selection_type == "単一選択":
        value = st.selectbox(label, list(options.keys()), index=0)
        return options[value]
    elif selection_type == "範囲選択":
        # 範囲選択の際に `'*'` を除外
        range_options = [opt for opt in options.keys() if opt != "*"]
        cols = st.columns(2)
        with cols[0]:
            from_value = st.selectbox(
                f"{label} (From)", range_options, index=0, key=f"{label}_from"
            )
        with cols[1]:
            to_value = st.selectbox(
                f"{label} (To)",
                range_options,
                index=len(range_options) - 1,
                key=f"{label}_to",
            )
        # 結果を統一して返す
        return f"{options[from_value]}-{options[to_value]}"

    elif selection_type == "カスタム入力":
        # カスタム入力も統一形式で返す
        custom_value = st.text_input(f"{label} (カスタム入力)", value="")
        # フィールド直下にエラーを出すためのプレースホルダ
        st.session_state[f"{label}_error_slot"] = st.empty()
        return custom_value


# --- アプリの基本設定 ---
st.set_page_config(page_title="Cron文字列ジェネレーター", page_icon="⏰")

# --- タイトル ---
st.title("⏰ Cron文字列ジェネレーター")
st.caption("Cron形式のスケジュール文字列を簡単に生成します。")

# --- 入力フィールド ---
st.subheader("1. スケジュールを設定")

# Cron形式の切り替え
cron_type = st.radio("**Cron形式を選択**", options=["Unix", "Spring"], index=0)

# 秒の選択 (Spring cron用)
if cron_type == "Spring":
    second = select_single_range_or_custom("秒", ["*"] + [str(i) for i in range(60)])

# 分、時、日、月、曜日の選択
minute = select_single_range_or_custom("分", ["*"] + [str(i) for i in range(60)])
hour = select_single_range_or_custom("時", ["*"] + [str(i) for i in range(24)])
day = select_single_range_or_custom("日", ["*"] + [str(i) for i in range(1, 32)])

# 月の選択肢に偶数月と奇数月を追加
month_options = ["*"] + [str(i) for i in range(1, 13)]
month = select_single_range_or_custom("月", month_options)

weekday_options = {
    "*": "*",
    "日曜": "0",
    "月曜": "1",
    "火曜": "2",
    "水曜": "3",
    "木曜": "4",
    "金曜": "5",
    "土曜": "6",
}
# 曜日の選択肢を取得する際に、キーと値を表示形式に変換
# weekday_options_display = [f"{key} ({value})" for key, value in weekday_options.items()]
weekday = select_single_range_or_customw2("曜日", weekday_options)

# 選択された値を分解して取得
if weekday:
    st.write(f"変換された曜日の値: {weekday}")  # デバッグ用
else:
    st.error(f"無効な曜日が選択されました: {weekday}")
    weekday = "*"
st.divider()  # 区切り線

# 実行ユーザとコマンドの入力フィールド
st.subheader("2. 実行ユーザとコマンドを設定")
user = st.text_input("実行ユーザ", value="root")
command = st.text_input("実行コマンド", value="/path/to/command")
st.divider()  # 区切り線

# --- Cron文字列の生成 ---
if st.button("Cron文字列を生成"):
    # カスタム入力の未入力チェック
    def is_custom_empty(field_label, value):
        sel = st.session_state.get(f"{field_label}_selection_type")
        return sel == "カスタム入力" and (value is None or str(value).strip() == "")

    empty_custom_fields = []
    # Spring の場合は秒もチェック
    if cron_type == "Spring":
        if is_custom_empty("秒", second):
            empty_custom_fields.append("秒")
    if is_custom_empty("分", minute):
        empty_custom_fields.append("分")
    if is_custom_empty("時", hour):
        empty_custom_fields.append("時")
    if is_custom_empty("日", day):
        empty_custom_fields.append("日")
    if is_custom_empty("月", month):
        empty_custom_fields.append("月")
    if is_custom_empty("曜日", weekday):
        empty_custom_fields.append("曜日")

    if empty_custom_fields:
        # 各対象フィールド直下にエラー表示
        for flabel in empty_custom_fields:
            slot = st.session_state.get(f"{flabel}_error_slot")
            if slot is not None:
                slot.error("カスタム入力が未入力です")
        # 生成はスキップ
    else:
        if cron_type == "Unix":
            cron_string = f"{minute} {hour} {day} {month} {weekday} {user} {command}"
        else:  # Spring cron
            cron_string = f"{second} {minute} {hour} {day} {month} {weekday}"

        st.subheader("3. 生成されたCron文字列")
        st.code(cron_string, language="bash")
        st.caption("この文字列をcrontabに追加してください。")
