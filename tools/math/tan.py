import numpy as np
import matplotlib.pyplot as plt
import streamlit as st

def gen_chart():
    st.write("### Tangent Wave")

    # スライダーで範囲と分割数を選択
    x_min = st.slider('X軸の最小値', -10, 0, -10, key="x_min_tan")
    x_max = st.slider('X軸の最大値', 0, 10, 10, key="x_max_tan")
    num_points = st.slider('プロットする点の数', 100, 1000, 500, key="num_points_tan")

    # xの値を生成（発散点を避ける）
    x = np.linspace(x_min, x_max, num_points)
    x = x[np.abs(np.cos(x)) > 1e-2]  # 発散点を除外
    y_tan = np.tan(x)

    # グラフ描画
    fig, ax = plt.subplots()
    ax.plot(x, y_tan, label='tan(x)', color='green')
    ax.set_title('Tangent Wave')
    ax.set_xlabel('x')
    ax.set_ylabel('tan(x)')
    ax.axhline(0, color='black', linewidth=0.5, linestyle='--')
    ax.axvline(0, color='black', linewidth=0.5, linestyle='--')
    ax.legend()
    st.pyplot(fig)
