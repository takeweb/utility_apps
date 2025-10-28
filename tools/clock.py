import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime
import time
import locale
import pytz
import io

def get_tz_time():
    # タイムゾーン「Asia/Tokyo」のオブジェクトを取得
    jst = pytz.timezone("Asia/Tokyo")

    # タイムゾーンを指定して現在時刻を取得
    now_tz = datetime.now(jst)

    return now_tz

def plot_clock():
    """
    時計を描画する関数
    """
    now = get_tz_time()
    second = now.second
    minute = now.minute + second / 60.0
    hour = now.hour % 12 + minute / 60.0

    fig, ax = plt.subplots(figsize=(4, 4))
    ax.set_xlim(-1.5, 1.5)
    ax.set_ylim(-1.5, 1.5)
    ax.set_aspect('equal')
    ax.axis('off')

    # 文字盤の背景色を設定
    circle = plt.Circle((0, 0), 1.2, color='#f0f0f0', ec='black', lw=2, zorder=0)
    ax.add_artist(circle)

    # 時計の目盛り（内側にずらす）
    for i in range(12):
        angle = 2 * np.pi * i / 12
        x = np.sin(angle)
        y = np.cos(angle)
        ax.text(1.0 * x, 1.0 * y, str(i if i != 0 else 12),
                ha='center', va='center', fontsize=12)

    # 時針
    hour_angle = 2 * np.pi * hour / 12
    ax.plot([0, 0.6 * np.sin(hour_angle)], [0, 0.6 * np.cos(hour_angle)],
            color='black', linewidth=6, label='Hour')

    # 分針
    minute_angle = 2 * np.pi * minute / 60
    ax.plot([0, 0.8 * np.sin(minute_angle)], [0, 0.8 * np.cos(minute_angle)],
            color='blue', linewidth=4, label='Minute')

    # 秒針
    second_angle = 2 * np.pi * second / 60
    ax.plot([0, 0.9 * np.sin(second_angle)], [0, 0.9 * np.cos(second_angle)],
            color='red', linewidth=2, label='Second')
    return fig

def print_date():
    locale.setlocale(locale.LC_TIME, 'ja_JP.UTF-8')
    today = datetime.today()

    # strftime()メソッドを使って日付と曜日をフォーマット
    # %Y: 年、%m: 月、%d: 日、%A: 完全な曜日名
    formatted_date_ja = today.strftime("%Y年%m月%d日(%a)")
    st.write(formatted_date_ja)

def draw_clock():
    """
    Streamlit上にアナログ時計を表示する。
    """
    st.set_page_config(layout="centered")
    st.title("時計アプリ")

    print_date()

    # 時計をリアルタイムで更新
    placeholder1 = st.empty()
    placeholder2 = st.empty()

    while True:
        with placeholder1.container():
            # デジタル時計の表示
            now = get_tz_time()
            digital_time = now.strftime('%H:%M:%S')
            st.text(f"現在時刻: {digital_time}")

        with placeholder2.container():
            fig = plot_clock()
            st.pyplot(fig, width='content')
            # buf = io.BytesIO()
            # fig.savefig(buf, format="png", bbox_inches='tight', pad_inches=0)
            # buf.seek(0)

            # # ★ 提案B: 幅を 300px に固定して表示
            # st.image(buf, width=500)

            plt.close(fig)  # 図を閉じてメモリを解放

        time.sleep(1)

if __name__ == "__main__":
    draw_clock()
