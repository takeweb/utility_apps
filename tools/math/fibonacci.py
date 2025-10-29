import streamlit as st
import matplotlib.pyplot as plt
import matplotlib_fontja  # noqa: F401
from typing import List

def generate_fibonacci(n: int) -> List[int]:
    """
    フィボナッチ数列を生成する関数

    Args:
        n (int): 生成するフィボナッチ数列の要素数

    Returns:
        list: フィボナッチ数列
    """
    if n <= 0:
        return []
    elif n == 1:
        return [0]
    elif n == 2:
        return [0, 1]

    fibonacci = [0, 1]
    for i in range(2, n):
        fibonacci.append(fibonacci[-1] + fibonacci[-2])
    return fibonacci

def gen_chart():
    st.write("### フィボナッチ数列")
    n = st.slider('フィボナッチ数列の要素数を選択してください', 1, 30, 10)
    fibonacci_sequence = generate_fibonacci(n)
    st.write(f"フィボナッチ数列（最初の{n}項）: {fibonacci_sequence}")

    # フィボナッチ数列のグラフ描画
    fig, ax = plt.subplots()
    ax.plot(range(n), fibonacci_sequence, marker='o')
    ax.set_title('フィボナッチ数列のグラフ')
    ax.set_xlabel('項の番号')
    ax.set_ylabel('値')
    st.pyplot(fig)

