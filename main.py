import streamlit as st


def main():
    st.title("ユーティリティアプリへようこそ！")
    st.write("サイドバー、または以下のリンクから移動できます。")

    # ページ本文中に他のページへのリンクを設置
    st.page_link(
        "pages/00_cheatsheet.py", label="「Markdown Cheat Sheet」はこちら", icon="🛠️"
    )
    st.page_link("pages/01_clock.py", label="時計アプリはこちら", icon="🕰️")
    st.page_link(
        "pages/02_wareki.py", label="西暦・和暦 相互変換アプリはこちら", icon="📅"
    )
    st.page_link("pages/03_math_charts.py", label="数学グラフアプリはこちら", icon="📊")
    st.page_link(
        "pages/04_base_converter.py", label="基数変換アプリはこちら", icon="🔢"
    )
    st.page_link(
        "pages/05_password_generator.py",
        label="パスワード生成アプリはこちら",
        icon="🔐",
    )
    st.page_link(
        "pages/06_unix_permission.py",
        label="UNIXパーミッション変換アプリはこちら",
        icon="🛃",
    )
    st.page_link("pages/07_color_display.py", label="色表示アプリはこちら", icon="🎨")
    st.page_link(
        "pages/08_ascii_converter.py", label="ASCII変換アプリはこちら", icon="🔤"
    )
    st.page_link(
        "pages/09_cidr_checker.py",
        label="IPアドレス・CIDRチェックアプリはこちら",
        icon="🌐",
    )
    st.page_link(
        "pages/10_cron_generator.py",
        label="Cron文字列ジェネレーターはこちら",
        icon="⏰",
    )
    st.page_link(
        "pages/11_ieee754_visualizer.py",
        label="IEEE 754 可視化ツールはこちら",
        icon="⚙️",
    )

    st.divider()  # 区切り線

    st.write("メインページのコンテンツ...")


if __name__ == "__main__":
    main()
