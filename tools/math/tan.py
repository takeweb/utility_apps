import numpy as np
import matplotlib.pyplot as plt
import streamlit as st


def gen_tangent_wave_chart():  # 引数から num_points を削除
    """Tangent (tan) グラフを描画する関数"""
    with st.expander("**タンジェント波 (tan) グラフ**", expanded=True):
        # スライダーでX軸の範囲を選択
        x_min = st.slider("Tangent: X軸の最小値", -10, 0, -10, key="x_min_tan")
        x_max = st.slider("Tangent: X軸の最大値", 0, 10, 10, key="x_max_tan")

        # プロットする点の数のスライダーを復活
        num_points = st.slider(
            "Tangent: プロットする点の数", 100, 1000, 500, key="num_points_tan"
        )

        # xの値を生成
        x = np.linspace(x_min, x_max, num_points)

        # tan(x) が発散する点 (π/2 + nπ) の近くを除外
        # Filter out points near vertical asymptotes
        x = x[np.abs(np.cos(x)) > 1e-2]
        y_tan = np.tan(x)

        # グラフ描画
        fig, ax = plt.subplots()
        # 連続した線で描画する元の形式に戻します
        ax.plot(
            x, y_tan, label="tan(x)", color="green"
        )  # 'o' から変更, 色を 'green' に戻す
        ax.set_title("Tangent Wave")
        ax.set_xlabel("x")
        ax.set_ylabel("tan(x)")

        ax.legend()
        ax.grid(True)
        st.pyplot(fig)


def gen_arctangent_wave_chart():  # 引数から num_points を削除
    """Arctangent (arctan) グラフを描画する関数"""
    with st.expander("**アークタンジェント波 (arctan) グラフ**", expanded=True):
        # arctan の特徴についての注釈
        st.info(
            "アークタンジェント (arctan) は、すべてのに `x` で定義されます。\n\n"
            "グラフは `y = π/2` (約 1.57) と `y = -π/2` (約 -1.57) の"
            "2本の水平な漸近線に近づいていきます。"
        )

        # スライダーでX軸の範囲を選択
        x_min = st.slider("Arctangent: X軸の最小値", -20, 0, -10, key="x_min_arctan")
        x_max = st.slider("Arctangent: X軸の最大値", 0, 20, 10, key="x_max_arctan")

        # プロットする点の数のスライダーを追加
        num_points = st.slider(
            "Arctangent: プロットする点の数", 100, 1000, 500, key="num_points_arctan"
        )

        # xの値を生成
        x_atan = np.linspace(x_min, x_max, num_points)

        # np.arctan を使って y の値を計算
        y_atan = np.arctan(x_atan)

        # グラフ描画
        fig, ax = plt.subplots()
        ax.plot(x_atan, y_atan, label="arctan(x)", color="orange")

        # 漸近線を点線で描画
        ax.axhline(np.pi / 2, color="gray", linestyle="--", label="y = π/2")
        ax.axhline(-np.pi / 2, color="gray", linestyle="--", label="y = -π/2")

        ax.set_title("Arctangent Wave")
        ax.set_xlabel("x")
        ax.set_ylabel("arctan(x)")
        ax.legend()
        ax.grid(True)
        st.pyplot(fig)
