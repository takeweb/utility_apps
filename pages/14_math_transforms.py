import streamlit as st
import math

st.set_page_config(page_title="対数・指数・根変換ツール", page_icon="🔣")
st.title("📈 対数・指数・平方根（任意根）変換ツール")
st.write(
    "小さな対話式ツールです。値を入力して、対数（log）、べき乗（exp）、および任意根（nth root）を確認できます。"
)

tab = st.tabs(["対数 (log)", "指数 (exp)", "根 (root)"])

with tab[0]:
    st.header("対数 (log)")
    x = st.number_input("値 x (>0)", value=10.0, format="%.6g")
    base_choice = st.selectbox(
        "底 (base)", options=["e", "10", "2", "カスタム"], index=1
    )
    if base_choice == "カスタム":
        b = st.number_input("カスタム底 b (b>0, b!=1)", value=3.0, format="%.6g")
    else:
        b = math.e if base_choice == "e" else (10.0 if base_choice == "10" else 2.0)

    if x <= 0 or b <= 0 or abs(b - 1.0) < 1e-12:
        st.error("x>0, b>0 かつ b!=1 の条件を満たしてください。")
    else:
        result = math.log(x, b)
        st.subheader(f"結果: log_{b}({x}) = {result}")
        st.write("計算式: log_b(x) = ln(x) / ln(b)")
        st.write(f"ln(x) = {math.log(x):.6g}, ln(b) = {math.log(b):.6g}")
        # 簡単なテーブル: x の近傍での対数変化
        st.write("近傍の値での比較（x±）")
        deltas = [-0.5, -0.1, 0.1, 0.5]
        rows = []
        for d in deltas:
            xv = max(1e-12, x + d)
            rows.append({"x": xv, f"log_{b}(x)": math.log(xv, b)})
        st.table(rows)

with tab[1]:
    st.header("指数 / べき乗 (exp)")
    base = st.number_input("底 b", value=2.0, format="%.6g")
    exponent = st.number_input("指数 y", value=3.0, format="%.6g")
    try:
        val = base**exponent
        st.subheader(f"結果: {base}^{exponent} = {val}")
        st.write("計算式: b^y = exp(y * ln(b))")
        st.write(f"y * ln(b) = {exponent * math.log(base):.6g}")
    except Exception as e:
        st.error(f"計算できません: {e}")

with tab[2]:
    st.header("根 (nth root)")
    n = st.number_input("根の次数 n (整数≥1)", value=2, min_value=1, step=1)
    v = st.number_input("v（根を求める値）", value=9.0, format="%.6g")
    try:
        # 奇数根は負にも対応する
        if v < 0 and n % 2 == 0:
            st.error("偶数根に負の値は許容されません。")
        else:
            root = math.copysign(abs(v) ** (1.0 / n), v)
            st.subheader(f"結果: {n}√{v} = {root}")
            st.write(f"計算式: v^(1/n) = {v}^(1/{n})")
    except Exception as e:
        st.error(f"計算できません: {e}")

st.caption(
    "注: このページは教育目的の小道具です。厳密な数値解析が必要な場合は専門ライブラリの利用を検討してください。"
)
