import streamlit as st
from supabase import Client
from libs.supabase_client import get_supabase_client
from datetime import date, datetime

def get_formatted_date(input_str):
    try:
        # 入力された文字列を「%Y/%m/%d」形式で日付オブジェクトに変換
        # ここで形式が異なると ValueError が発生します
        date_object = datetime.strptime(input_str, "%Y/%m/%d")

        # B. 変換された日付オブジェクトを目的の「YYYY-MM-DD」形式の文字列に変換
        return date_object.strftime("%Y-%m-%d")

    except ValueError:
        # 形式が一致しない場合のエラー処理
        st.error("入力された日付の形式が「YYYY/MM/DD」と異なります。ご確認ください。")

def convert_seireki_2_wareki(supabase, formatted_date):
    res = supabase.rpc("get_era_date", {"seireki_date": formatted_date}).execute()
    if res.data:
        return res.data

@st.cache_data(ttl=3600) # 1時間データをキャッシュ
def fetch_wareki_data(_supabase: Client):
    """
    Supabaseから元号データを取得する。
    start_dateの昇順でソートし、全ての列を取得します。
    """
    try:
        response = _supabase.table("warekis").select("*").order("start_date", desc=False).execute()

        # 取得したデータは response.data にリスト形式で含まれる
        if response.data:
            return response.data
        else:
            st.error("warekisテーブルからデータを取得できませんでした。")
            return []

    except Exception as e:
        st.error(f"Supabaseからのデータ取得中にエラーが発生しました: {e}")
        return []

def main():
    supabase_client = get_supabase_client()

    st.title("西暦→和暦変換")

    # st.text_inputでユーザー入力を受け付ける
    input_str = st.text_input(
        "日付を入力 (形式: yyyy/mm/dd)",
        value=date.today().strftime("%Y/%m/%d"),
        placeholder="例: 2025/10/23"
    )

    # 処理結果を格納するための変数
    formatted_date = None

    # 入力値のバリデーションと変換のロジック
    if input_str:
        formatted_date = get_formatted_date(input_str)
    else:
        # 入力フィールドが空の場合の処理
        st.warning("日付を入力してください。")

    if st.button("↓↓変換↓↓"):
        try:
            # 西暦から和暦への変換処理
            result = convert_seireki_2_wareki(supabase_client, formatted_date)
            if result:
                st.success(result)
            else:
                st.info("データがありません。")
        except Exception as e:
            st.error(f"エラーが発生しました: {e}")

    st.title("和暦→西暦変換")

    # 元号データを取得
    wareki_data = fetch_wareki_data(supabase_client)

    if wareki_data:
        gengo_map = {d['gengo']: d for d in wareki_data}
        gengo_options = list(gengo_map.keys())

        col1, col2 = st.columns(2)

        with col1:
            # 1. 元号のセレクトボックス
            selected_gengo = st.selectbox("元号を選択", gengo_options)

        # 選択された元号の情報と期間から和暦年リストを生成
        era_info = gengo_map.get(selected_gengo)

        if era_info:
            start_date_obj = datetime.strptime(era_info['start_date'], '%Y-%m-%d').date()

            # 終了年の計算: '9999-12-31'は現在の年を使用
            if era_info['end_date'] == '9999-12-31':
                end_date_obj = date.today()
            else:
                end_date_obj = datetime.strptime(era_info['end_date'], '%Y-%m-%d').date()

            # 和暦年数の計算 (西暦終了年 - 西暦開始年 + 1)
            wareki_years_count = end_date_obj.year - start_date_obj.year + 1

            # 整数リスト (1, 2, 3...) を生成
            numerical_years = list(range(1, wareki_years_count + 1))

            # 和暦年の選択肢リストを生成（文字列に変換し、1を「元年」に置き換える）
            wareki_year_options = []
            for year in numerical_years:
                if year == 1:
                    wareki_year_options.append("元年")
                else:
                    wareki_year_options.append(f"{year}年")

            # 初期値を1年（元年）に設定
            default_index = 0

            with col2:
                # 2. 和暦年のセレクトボックス
                selected_wareki_str = st.selectbox(
                    f"{selected_gengo} の年を選択",
                    wareki_year_options,
                    index=default_index
                )

            # 3. 西暦への変換ロジック
            # 選択された文字列から実際の年数(数値)を取得
            if selected_wareki_str == "元年":
                wareki_year_num = 1
            else:
                # 「2年」, 「3年」などの文字列から「年」を除去して整数に変換
                wareki_year_num = int(selected_wareki_str.replace('年', ''))

            # 西暦計算に使用する年数 (例: 元年なら 1)
            start_seireki_year = start_date_obj.year

            # 西暦 = 元号開始年 + 和暦年 - 1
            seireki_year = start_seireki_year + wareki_year_num - 1

            st.success(f"西暦 {seireki_year}年 ")

    else:
        st.info("元号データが見つかりませんでした。Supabaseの設定を確認してください。")

if __name__ == "__main__":
    main()
