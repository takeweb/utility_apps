import streamlit as st
from libs.supabase_client import get_supabase_client
from datetime import date

def main():
    st.title("西暦→和暦変換")

    # input_date = st.text_input("日付を入力 (例: 2024-03-15)")
    selected_date = st.date_input("日付を選択", value=date.today())

    # 「YYYY-MM-DD」形式に変換
    input_date = selected_date.strftime("%Y-%m-%d")

    if st.button("取得↓↓"):
        if not input_date:
            st.warning("日付を入力してください。")
            return

        supabase = get_supabase_client()
        try:
            res = supabase.rpc("get_era_date", {"seireki_date": input_date}).execute()

            # res.data が None の場合、res.response から直接取得を試みる
            data = None
            if res.data:
                data = res.data
            elif hasattr(res, "response"):
                try:
                    json_data = res.response.json()
                    st.write(json_data)
                    if isinstance(json_data, list) and len(json_data) > 0:
                        data = json_data[0].get("get_era_date")
                    elif isinstance(json_data, str):
                        data = json_data
                except Exception:
                    pass

            if data:
                st.success(data)
            else:
                st.info("データがありません。")

        except Exception as e:
            st.error(f"エラーが発生しました: {e}")

if __name__ == "__main__":
    main()
