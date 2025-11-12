import numpy as np
import matplotlib.pyplot as plt
import streamlit as st

def gen_sine_chart(num_points):
    """Sine (sin) グラフを描画する関数"""
    with st.expander("**サイン波 (sin) グラフ**", expanded=True):
        # スライダーでX軸の範囲を選択 (Select X-axis range with sliders)
        x_min_sin = st.slider('Sine: X軸の最小値', -10, 0, -10, key='sin_min')
        x_max_sin = st.slider('Sine: X軸の最大値', 0, 10, 10, key='sin_max')

        # xの値を生成 (Generate x values for sin)
        x_sin = np.linspace(x_min_sin, x_max_sin, num_points)
        y_sin = np.sin(x_sin)

        # グラフ描画 (Plotting the sin graph)
        fig, ax = plt.subplots()
        ax.plot(x_sin, y_sin, label='sin(x)', color='blue')
        ax.set_title('Sine Wave')
        ax.set_xlabel('x')
        ax.set_ylabel('sin(x)')
        ax.legend()
        ax.grid(True)
        st.pyplot(fig)

def gen_arcsine_chart(num_points):
    """Arcsine (arcsin) グラフを描画する関数"""
    with st.expander("**アークサイン波 (arcsin) グラフ**", expanded=True):
        # arcsin の定義域 ([-1, 1]) についての注釈
        st.info(
            "アークサイン (arcsin) は、入力 (x) の範囲が **-1 から 1** の間でのみ定義されます。\n\n"
            "そのため、このグラフは x = -1 から x = 1 の範囲で固定して描画しています。"
        )

        # arcsin用のxの値を生成 (-1 から 1 の範囲で)
        # Generate x values for arcsin (fixed range [-1, 1])
        x_asin = np.linspace(-1, 1, num_points)

        # np.arcsin を使って y の値を計算
        y_asin = np.arcsin(x_asin)

        # グラフ描画 (Plotting the arcsin graph)
        fig, ax = plt.subplots()
        ax.plot(x_asin, y_asin, label='arcsin(x)', color='red')
        ax.set_title('Arcsine Wave')
        ax.set_xlabel('x')
        ax.set_ylabel('arcsin(x)')
        ax.legend()
        ax.grid(True)
        st.pyplot(fig)
