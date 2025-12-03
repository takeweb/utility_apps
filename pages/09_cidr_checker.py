import streamlit as st
import ipaddress

from tools.cidr_checker import calculate_subnet_mask


# --- アプリの基本設定 ---
st.set_page_config(page_title="IPアドレス・CIDRチェック", page_icon="🔢")

# --- タイトル ---
st.title("🔢 IPアドレス・CIDRチェック")
st.caption("IPアドレスとCIDR表記の相互変換およびネットワーク情報の表示を行います。")

# --- 入力フィールド ---
st.subheader("1. IPアドレスを入力")
ip_input = st.text_input(
    "IPアドレスを入力してください (例: 192.168.1.0)", value="192.168.1.0"
)

st.subheader("2. サブネットマスクを選択")
prefix_length = st.slider(
    "サブネットマスクの長さ (CIDR)", min_value=0, max_value=32, value=24, step=1
)

# --- サブネットマスクの表示 ---
if "prefix_length" in locals():
    binary_mask, decimal_mask = calculate_subnet_mask(prefix_length)
    with st.expander("**サブネットマスクの情報**", expanded=True):
        st.write(f"- **サブネットマスク (2進数):** {binary_mask}")
        st.write(f"- **サブネットマスク (10進数):** {decimal_mask}")

if ip_input:
    try:
        # 入力を解析
        ip_cidr_input = f"{ip_input}/{prefix_length}"
        network = ipaddress.ip_network(ip_cidr_input, strict=False)

        # ネットワーク情報を取得
        network_address = network.network_address
        broadcast_address = network.broadcast_address
        num_addresses = network.num_addresses

        # ホスト範囲を直接計算
        if num_addresses > 2:
            first_host = network.network_address + 1
            last_host = network.broadcast_address - 1
            host_range = (first_host, last_host)
        else:
            host_range = ("N/A", "N/A")

        # ホスト数をカンマ区切りでフォーマット
        formatted_host_count = f"{num_addresses - 2:,}" if num_addresses > 2 else "0"

        # 結果を表示
        with st.expander("**ネットワーク情報**", expanded=True):
            st.write(f"- **ネットワークアドレス:** {network_address}")
            st.write(f"- **ブロードキャストアドレス:** {broadcast_address}")
            st.write(f"- **ホスト数:** {formatted_host_count}")
            st.write(f"- **ホスト範囲:** {host_range[0]} 〜 {host_range[1]}")

    except ValueError:
        st.error("無効なIPアドレスが入力されました。正しい形式で入力してください。")
