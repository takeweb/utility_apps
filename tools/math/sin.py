import numpy as np
import matplotlib.pyplot as plt
import streamlit as st

def gen_chart():
    st.write("### Sine Wave")
    
    # スライダーで範囲と分割数を選択
    x_min = st.slider('X軸の最小値', -10, 0, -10)
    x_max = st.slider('X軸の最大値', 0, 10, 10)
    num_points = st.slider('プロットする点の数', 100, 1000, 500)
    
    # xの値を生成
    x = np.linspace(x_min, x_max, num_points)
    y = np.sin(x)
    
    # グラフ描画
    fig, ax = plt.subplots()
    ax.plot(x, y, label='sin(x)', color='blue')
    ax.set_title('Sine Wave')
    ax.set_xlabel('x')
    ax.set_ylabel('sin(x)')
    ax.legend()
    st.pyplot(fig)
