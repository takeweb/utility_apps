import streamlit as st
import tools.math.fibonacci as fibonacci
import tools.math.sin as sin
import tools.math.cos as cos
import tools.math.tan as tan
import tools.math.kaprekar as kaprekar

st.write("## 1. フィナボッチ数列をグラブ描画してみる")
fibonacci.gen_chart()

st.write("## 2. サインカーブをグラフ描画してみる")
sin.gen_chart()

st.write("## 3. コサインカーブをグラフ描画してみる")
cos.gen_chart()

st.write("## 4. タンジェントカーブをグラフ描画してみる")
tan.gen_chart()

st.write("## 5. カプレカ数を調べてみる")
kaprekar.gen_chart()
