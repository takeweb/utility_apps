import streamlit as st
from libs.supabase_client import get_supabase_client
from datetime import date, datetime

def main():
    st.title("西暦→和暦変換")

    # 今日の日付を「yyyy/mm/dd」形式の文字列として初期値に設定
    default_date_str = date.today().strftime("%Y/%m/%d")

    # 1. st.text_inputでユーザー入力を受け付ける
    input_str = st.text_input(
        "日付を入力 (形式: yyyy/mm/dd)",
        value=default_date_str,
        placeholder="例: 2025/10/23"
    )

    # 処理結果を格納するための変数
    formatted_date = None

    # 2. 入力値のバリデーションと変換のロジック
    if input_str:
        try:
            # A. 入力された文字列を「%Y/%m/%d」形式で日付オブジェクトに変換
            #    ここで形式が異なると ValueError が発生します
            date_object = datetime.strptime(input_str, "%Y/%m/%d")

            # B. 変換された日付オブジェクトを目的の「YYYY-MM-DD」形式の文字列に変換
            formatted_date = date_object.strftime("%Y-%m-%d")

        except ValueError:
            # 形式が一致しない場合のエラー処理
            st.error("入力された日付の形式が「YYYY/MM/DD」と異なります。ご確認ください。")

    else:
        # 入力フィールドが空の場合の処理
        st.warning("日付を入力してください。")

    if st.button("↓↓変換↓↓"):
        supabase = get_supabase_client()
        try:
            res = supabase.rpc("get_era_date", {"seireki_date": formatted_date}).execute()

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
