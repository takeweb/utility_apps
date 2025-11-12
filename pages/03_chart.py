import streamlit as st
import tools.math.fibonacci as fibonacci
import tools.math.sin as sin
import tools.math.cos as cos
import tools.math.tan as tan
import tools.math.kaprekar as kaprekar

def main():
    st.title("数学グラフアプリ")
    fibonacci.gen_chart()
    sin.gen_sine_chart(1000)
    sin.gen_arcsine_chart(1000)
    cos.gen_cosine_chart(1000)
    cos.gen_arccosine_chart(1000)
    tan.gen_tangent_chart()
    tan.gen_arctangent_chart()
    kaprekar.gen_chart()

if __name__ == "__main__":
    main()
