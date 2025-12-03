import struct
import streamlit as st

st.set_page_config(page_title="IEEE 754 可視化", page_icon="⚙️")
st.title("⚙️ IEEE 754 浮動小数点 可視化")
st.caption(
    "32-bit(単精度) / 64-bit(倍精度) のビット構成、符号・指数・仮数の分解を確認できます"
)

# 入力
cols = st.columns([2, 1])
with cols[0]:
    num_str = st.text_input("数値を入力 (10進, 科学記法可)", value="3.141592653589793")
with cols[1]:
    mode = st.radio("精度", ["32-bit(単精度)", "64-bit(倍精度)"], horizontal=True)

# 変換ユーティリティ


def float_to_bits_32(f: float) -> str:
    b = struct.pack("!f", f)  # network (= big endian)
    i = struct.unpack("!I", b)[0]
    return f"{i:032b}"


def float_to_bits_64(f: float) -> str:
    b = struct.pack("!d", f)
    i = struct.unpack("!Q", b)[0]
    return f"{i:064b}"


def split_ieee754(bits: str):
    if len(bits) == 32:
        sign = bits[0]
        exponent = bits[1:9]
        mantissa = bits[9:]
        bias = 127
        exp_val = int(exponent, 2)
        frac_val = sum(int(bit) * (2 ** -(i + 1)) for i, bit in enumerate(mantissa))
        kind = "単精度(32)"
    else:
        sign = bits[0]
        exponent = bits[1:12]
        mantissa = bits[12:]
        bias = 1023
        exp_val = int(exponent, 2)
        frac_val = sum(int(bit) * (2 ** -(i + 1)) for i, bit in enumerate(mantissa))
        kind = "倍精度(64)"
    return {
        "kind": kind,
        "sign": sign,
        "exponent": exponent,
        "mantissa": mantissa,
        "bias": bias,
        "exp_val": exp_val,
        "frac_val": frac_val,
    }


# 計算・表示
try:
    value = float(num_str)
    if mode.startswith("32"):
        bits = float_to_bits_32(value)
    else:
        bits = float_to_bits_64(value)

    parts = split_ieee754(bits)

    st.subheader("ビット列")
    st.code(bits)

    # 分解は1行表示
    st.subheader("分解 (sign | exponent | mantissa)")
    st.code(f"{parts['sign']} | {parts['exponent']} | {parts['mantissa']}")

    # 詳細は1行表示
    st.subheader("詳細")
    # col1 を狭め、col2/col3 を広めに配置
    col1, col2, col3 = st.columns([1, 2, 2])
    col1.write(f"符号 (sign): {parts['sign']}")
    col2.write(f"指数 (exponent): {parts['exp_val']} (bias={parts['bias']})")
    col3.write(f"仮数 (mantissa): 長さ {len(parts['mantissa'])}")

    # 特殊値の扱い・数式表示
    exp = parts["exp_val"]
    frac = parts["frac_val"]
    bias = parts["bias"]
    sign = -1 if parts["sign"] == "1" else 1

    if exp == 0 and frac == 0.0:
        st.info("ゼロ (±0)")
    elif exp == (2 ** len(parts["exponent"])) - 1:
        if frac == 0.0:
            st.info("無限大 (±∞)")
        else:
            st.warning("NaN (非数)")
    else:
        if exp == 0:
            # 非正規化数
            e = 1 - bias
            m = frac  # leading 1 なし
            st.markdown("指数が0のため、非正規化数です")
        else:
            # 正規化数
            e = exp - bias
            m = 1.0 + frac
        st.latex(r"x = (-1)^{s} \times m \times 2^{e}")
        st.write(f"s={parts['sign']}, m={m}, e={e}")
        st.write(f"再構成値: {sign * m * (2**e)}")

    # 参考: Pythonのrepr と差分
    st.subheader("Pythonの表示と差分")
    st.write({"入力": num_str, "float": value, "ビット長": len(bits)})
except Exception as e:
    st.error(f"入力の解析に失敗しました: {e}")
    st.caption("数字以外の文字が含まれていないか、形式が正しいか確認してください。")
