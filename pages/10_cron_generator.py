import streamlit as st

# --- アプリの基本設定 ---
st.set_page_config(page_title="Cron文字列ジェネレーター", page_icon="⏰")

# --- タイトル ---
st.title("⏰ Cron文字列ジェネレーター")
st.caption("Cron形式のスケジュール文字列を簡単に生成します。")

# --- 入力フィールド ---
st.subheader("1. スケジュールを設定")

# 分、時、日、月、曜日のセレクトボックス
minute = st.selectbox(
    "分 (0-59, *など)", options=["*"] + [str(i) for i in range(60)], index=0
)
hour = st.selectbox(
    "時 (0-23, *など)", options=["*"] + [str(i) for i in range(24)], index=0
)
day = st.selectbox(
    "日 (1-31, *など)", options=["*"] + [str(i) for i in range(1, 32)], index=0
)
month = st.selectbox(
    "月 (1-12, *など)", options=["*"] + [str(i) for i in range(1, 13)], index=0
)

# 曜日の選択肢を名前付きに変更
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
weekday_label = st.selectbox(
    "曜日 (0-6, *など, 0=日曜)", options=weekday_options.keys(), index=0
)
weekday = weekday_options[weekday_label]

# 実行ユーザとコマンドの入力フィールド
st.subheader("2. 実行ユーザとコマンドを設定")
user = st.text_input("実行ユーザ", value="root")
command = st.text_input("実行コマンド", value="/path/to/command")

# --- Cron文字列の生成 ---
if st.button("Cron文字列を生成"):
    cron_string = f"{minute} {hour} {day} {month} {weekday} {user} {command}"
    st.subheader("生成されたCron文字列")
    st.code(cron_string, language="bash")

    st.caption("この文字列をcrontabに追加してください。")
