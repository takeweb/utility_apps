import numpy as np
import matplotlib.pyplot as plt
import streamlit as st

def gen_chart():
    st.write("### Cosine Wave")

    # スライダーで範囲と分割数を選択
    x_min = st.slider('X軸の最小値', -10, 0, -10, key="x_min_cos")
    x_max = st.slider('X軸の最大値', 0, 10, 10, key="x_max_cos")
    num_points = st.slider('プロットする点の数', 100, 1000, 500, key="num_points_cos")

    # xの値を生成
    x = np.linspace(x_min, x_max, num_points)
    y_cos = np.cos(x)

    # グラフ描画
    fig, ax = plt.subplots()
    ax.plot(x, y_cos, label='cos(x)', color='red')
    ax.set_title('Cosine Wave')
    ax.set_xlabel('x')
    ax.set_ylabel('cos(x)')
    ax.legend()
    st.pyplot(fig)
