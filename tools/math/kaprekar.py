import streamlit as st
import matplotlib.pyplot as plt
from collections import Counter
import pandas as pd


def is_kaprekar_number(n: int) -> bool:
    """
    カプレカ数を判定する関数。
    カプレカ数とは、平方数を2つの部分に分けたとき、
    その和が元の数に等しくなる数のこと。

    例: 45 の場合
    45^2 = 2025
    2025 を 20 と 25 に分けると 20 + 25 = 45
    よって 45 はカプレカ数。

    Args:
        n (int): 判定する整数。

    Returns:
        bool: n がカプレカ数であれば True、それ以外は False。
    """
    if n < 1:
        return False

    if n == 1:
        return True

    # n の平方数を文字列として取得
    square = str(n ** 2)

    # 文字列を2つの部分に分割して判定
    for i in range(1, len(square)):
        left = int(square[:i]) if square[:i] else 0
        right = int(square[i:]) if square[i:] else 0
        # 右側が 0 の場合は無視
        if right == 0:
            continue
        if left + right == n:
            return True

    return False


def find_kaprekar_numbers(max_digits: int) -> list:
    """
    指定された桁数までのカプレカ数をすべて返す関数。

    Args:
        max_digits (int): 最大桁数。

    Returns:
        list: カプレカ数のリスト。
    """
    kaprekar_numbers = []
    upper_limit = 10 ** max_digits

    for n in range(1, upper_limit):
        if is_kaprekar_number(n):
            kaprekar_numbers.append(n)

    return kaprekar_numbers


def gen_chart():
    """
    カプレカ数をグラフ表示し、データフレームで表示する。
    """
    with st.expander("**カプレカ数 (Kaprekar Numbers) グラフ**", expanded=True):


        max_digits = st.slider("最大桁数を選択", min_value=1, max_value=6, value=4)
        st.write(f"{max_digits}桁までのカプレカ数を表示します。")

        kaprekar_numbers = find_kaprekar_numbers(max_digits)

        # カプレカ数をデータフレームで表示
        with st.expander("**カプレカ数の詳細**", expanded=True):
            df = pd.DataFrame({
                "桁数": [len(str(num)) for num in kaprekar_numbers],
                "Kaprekar Numbers": kaprekar_numbers
            }).reset_index(drop=True)
            st.write("生成されたカプレカ数:")
            st.dataframe(df, width='stretch')

        # 桁数ごとの件数をカウント
        digit_counts = Counter(len(str(num)) for num in kaprekar_numbers)

        # グラフの作成
        plt.figure(figsize=(10, 6))
        plt.bar(digit_counts.keys(), digit_counts.values(), tick_label=[f"{d}桁" for d in digit_counts.keys()])
        plt.xlabel("桁数")
        plt.ylabel("件数")
        plt.title(f"桁数ごとのカプレカ数 (最大 {max_digits} 桁)")

        # グリッド（格子線）をY軸に追加
        plt.grid(axis='y', linestyle='--', alpha=0.7)

        # Streamlitでグラフを表示
        st.pyplot(plt)
