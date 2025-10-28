from datetime import datetime, date
import calendar
import streamlit as st
from supabase import Client
from libs.supabase_client import get_supabase_client

# --- ユーティリティ関数 ---

# 西暦を和暦に変換する関数
def convert_seireki_2_wareki(supabase: Client, year: int, month: int, day: int):
    """西暦の日付を和暦に変換して返します。"""
    try:
        target_date = datetime(year, month, day).strftime("%Y-%m-%d")
        res = supabase.rpc("get_era_date", {"seireki_date": target_date}).execute()

        # 修正: Supabase RPC が和暦文字列を直接返すケースを想定
        if res.data:
            return res.data

        return "日付に対応する元号が見つかりません"

    except ValueError:
        return "正しい日付を入力してください"
    except Exception as e:
        # その他のエラー処理
        return f"変換エラーが発生しました: {e}"

# 和暦を西暦に変換する関数
def convert_wareki_2_seireki(start_seireki_year: int, wareki_year_str: str, month: int, day: int):
    """和暦情報（開始年、年文字列）と月日を西暦に変換して返します。"""
    if wareki_year_str == "元年":
        wareki_year_num = 1
    else:
        # 「2年」, 「3年」などの文字列から「年」を除去して整数に変換
        wareki_year_num = int(wareki_year_str.replace('年', ''))

    # 西暦 = 元号開始年 + 和暦年 - 1
    seireki_year = start_seireki_year + wareki_year_num - 1

    try:
        date_obj = datetime(seireki_year, month, day)
        return date_obj.strftime("%Y年%m月%d日")
    except ValueError:
        return "存在する正しい日付を入力してください"

def create_wareki_year_options(era_info: dict) -> tuple[list[str], int, date]:
    """
    元号情報から和暦年の選択肢リスト（文字列）、デフォルトインデックス、開始日を生成します。
    """
    start_date_obj = datetime.strptime(era_info['start_date'], '%Y-%m-%d').date()

    # 終了年の計算: '9999-12-31'は現在の年を使用
    if era_info['end_date'] == '9999-12-31':
        end_date_obj = date.today()
    else:
        end_date_obj = datetime.strptime(era_info['end_date'], '%Y-%m-%d').date()

    # 和暦年数の計算 (西暦終了年 - 西暦開始年 + 1)
    wareki_years_count = end_date_obj.year - start_date_obj.year + 1

    wareki_year_options = []
    for year in range(1, wareki_years_count + 1):
        if year == 1:
            wareki_year_options.append("元年")
        else:
            wareki_year_options.append(f"{year}年")

    default_index = len(wareki_year_options) - 1

    return wareki_year_options, default_index, start_date_obj

@st.cache_data(ttl=3600) # 1時間データをキャッシュ
def fetch_wareki_data(_supabase: Client):
    """Supabaseから元号データを取得し、start_dateの昇順でソートします。"""
    try:
        response = _supabase.table("warekis").select("*").order("start_date", desc=False).execute()
        if response.data:
            return response.data
        else:
            st.error("warekisテーブルからデータを取得できませんでした。")
            return
    except Exception as e:
        st.error(f"Supabaseからのデータ取得中にエラーが発生しました: {e}")
        return []

# --- Streamlit アプリ本体 ---

def display_streamlit_app():
    # Supabaseクライアントの初期化
    supabase_client = get_supabase_client()

    # 元号データを取得
    wareki_data = fetch_wareki_data(supabase_client)
    gengo_map = {d['gengo']: d for d in wareki_data}
    gengo_options = list(gengo_map.keys())

    # 最後の要素のインデックスをデフォルトにする
    default_index_gengo = len(gengo_options) - 1 if gengo_options else 0

    st.title("西暦・和暦 相互変換アプリ")
    today = datetime.now()

    # --------------------------------------------------------------------------
    ## 西暦から和暦への変換
    # --------------------------------------------------------------------------
    with st.expander("西暦から和暦への変換", expanded=True):
        cols = st.columns(3, gap="small")
        with cols[0]:
            year = st.selectbox("年 (西暦)", options=list(range(today.year, 1860, -1)), index=0, key="seireki_year")
        with cols[1]:
            month = st.selectbox("月", options=list(range(1, 13)), index=today.month - 1, key="seireki_month")
        with cols[2]:
            last_day = calendar.monthrange(year, month)[1]
            day = st.selectbox("日", options=list(range(1, last_day + 1)), index=today.day - 1, key="seireki_day")

        submitted1 = st.button("和暦に変換", key="convert_seireki_2_wareki_btn")

        # 結果表示
        if submitted1:
            wareki_result = convert_seireki_2_wareki(supabase_client, int(year), int(month), int(day))
            if "正しい日付" in wareki_result or "見つかりません" in wareki_result:
                st.error(wareki_result)
            elif "変換エラー" in wareki_result:
                st.exception(wareki_result)
            else:
                st.success(f"和暦: {wareki_result}")

    # --------------------------------------------------------------------------
    ## 和暦から西暦への変換
    # --------------------------------------------------------------------------
     # フォームの制約を外し、コンボの変更で即座に連動させる
    with st.expander("和暦から西暦への変換", expanded=True):
        cols = st.columns(4, gap="small")

        # 元号のセレクトボックス (変更時に即時再実行)
        with cols[0]:
             selected_gengo = st.selectbox("元号を選択", gengo_options, index=default_index_gengo, key="gengo_select_2")

        # 和暦年の計算 (selected_gengo に基づいて連動)
        wareki_year_options = ["---"]
        default_index_wareki = 0
        start_date_obj = None

        era_info = gengo_map.get(selected_gengo)
        if era_info:
            wareki_year_options, default_index_wareki, start_date_obj = create_wareki_year_options(era_info)

        with cols[1]:
            # 和暦年のセレクトボックス (optionsがリアルタイムで更新される)
            selected_wareki_str = st.selectbox(
                f"{selected_gengo} の年を選択",
                wareki_year_options,
                index=default_index_wareki,
                key="wareki_year_select_2"
            )

        with cols[2]:
            month2 = st.selectbox("月", options=list(range(1, 13)), index=today.month - 1, key="wareki_month_2")
        with cols[3]:
            last_day = calendar.monthrange(start_date_obj.year, month2)[1]
            day2 = st.selectbox("日", options=list(range(1, last_day + 1)), index=today.day - 1, key="wareki_day_2")

        # st.button に変更 (押された時のみ処理を実行)
        submitted2 = st.button("西暦に変換", key="convert_wareki_2_seireki_btn")

        # 結果表示
        if submitted2:
            if start_date_obj:
                # ユーザーが「---」を選択している可能性を排除
                if selected_wareki_str == "---":
                    st.error("年を選択してください。")
                else:
                    result = convert_wareki_2_seireki(start_date_obj.year, selected_wareki_str, int(month2), int(day2))
                    if "正しい日付" in result:
                        st.error(result)
                    else:
                        st.success(f"西暦: {result}")
            else:
                st.error("元号データが取得できませんでした。")
