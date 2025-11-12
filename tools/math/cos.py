import numpy as np
import matplotlib.pyplot as plt
import streamlit as st

def gen_cosine_chart(num_points):
    """Cosine (cos) グラフを描画する関数"""
    with st.expander("**コサイン波 (cos) グラフ**", expanded=True):
        # スライダーでX軸の範囲を選択 (Select X-axis range with sliders)
        x_min = st.slider('Cosine: X軸の最小値', -10, 0, -10, key="x_min_cos")
        x_max = st.slider('Cosine: X軸の最大値', 0, 10, 10, key="x_max_cos")

        # xの値を生成 (Generate x values for cos)
        x = np.linspace(x_min, x_max, num_points)
        y_cos = np.cos(x)

        # グラフ描画 (Plotting the cos graph)
        fig, ax = plt.subplots()
        ax.plot(x, y_cos, label='cos(x)', color='blue') # 色を青に変更（お好みで）
        ax.set_title('Cosine Wave')
        ax.set_xlabel('x')
        ax.set_ylabel('cos(x)')
        ax.legend()
        ax.grid(True)
        st.pyplot(fig)

def gen_arccosine_chart(num_points):
    """Arccosine (arccos) グラフを描画する関数"""
    with st.expander("**アークコサイン波 (arccos) グラフ**", expanded=True):
        # arccos の定義域 ([-1, 1]) についての注釈
        st.info(
            "アークコサイン (arccos) も、入力 (x) の範囲が **-1 から 1** の間でのみ定義されます。\n\n"
            "そのため、このグラフは x = -1 から x = 1 の範囲で固定して描画しています。"
        )

        # arccos用のxの値を生成 (-1 から 1 の範囲で)
        # Generate x values for arccos (fixed range [-1, 1])
        x_acos = np.linspace(-1, 1, num_points)

        # np.arccos を使って y の値を計算
        y_acos = np.arccos(x_acos)

        # グラフ描画 (Plotting the arccos graph)
        fig, ax = plt.subplots()
        ax.plot(x_acos, y_acos, label='arccos(x)', color='green') # 色を緑に設定
        ax.set_title('Arccosine Wave')
        ax.set_xlabel('x')
        ax.set_ylabel('arccos(x)')
        ax.legend()
        ax.grid(True)
        st.pyplot(fig)
