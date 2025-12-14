import streamlit as st
import streamlit.components.v1 as components
from datetime import datetime
import locale
import pytz
from lunardate import LunarDate
from supabase import Client
from libs.supabase_client import get_supabase_client
from tools.wareki import convert_seireki_2_wareki
import os
import json


def get_tz_time(tz_str):
    # 引数で指定されたタイムゾーンのオブジェクトを取得
    tz = pytz.timezone(tz_str)

    # タイムゾーンを指定して現在時刻を取得
    return datetime.now(tz)


def calculate_rokuyo(date):
    # 旧暦に変換
    lunar_date = LunarDate.fromSolarDate(date.year, date.month, date.day)

    # 六曜リスト（旧暦の月と日を合計し、6で割った余りによる）
    rokuyo_list = ["大安", "赤口", "先勝", "友引", "先負", "仏滅"]
    total = lunar_date.month + lunar_date.day
    rokuyo = rokuyo_list[total % 6]
    return rokuyo


def plot_all_clocks_js_only(other_offset_hours=-8, city_label="L.A. (UTC-8)"):
    """
    デジタル時計とアナログ時計の両方をJSで自己更新する
    HTMLコンポーネントを「1回だけ」描画する関数
    （アナログ秒針をデジタルと同期させ、体感ズレを解消）
    """

    # read external JS
    this_dir = os.path.dirname(__file__)
    js_path = os.path.join(this_dir, "clock.js")
    try:
        with open(js_path, "r", encoding="utf-8") as f:
            js_content = f.read()
    except Exception:
        js_content = ""

    # inject offsets and city label into JS placeholders (always run)
    # jst is fixed in JS; replace only the other offset placeholder
    js_content = js_content.replace("OTHER_OFFSET_PLACEHOLDER", str(other_offset_hours))
    # replace CITY_LABEL_PLACEHOLDER with a JS string literal (properly escaped)
    js_content = js_content.replace(
        "CITY_LABEL_PLACEHOLDER", json.dumps(city_label, ensure_ascii=False)
    )

    # layout: three time columns aligned horizontally, and three analog clocks below (JST / UTC / Other)
    html_code = (
        '<script src="https://cdn.jsdelivr.net/npm/echarts@5.5.0/dist/echarts.min.js"></script>'
        + "\n"
        + '<div style="display:flex; gap:1rem; align-items:center; justify-content:space-around; margin-bottom:1rem;">'
        + '<div id="digital_clock_display_jst" style="flex:1; text-align:center; font-family: Consolas, Menlo, Monaco, monospace; font-size:1.1rem; padding:0.5rem;">JST: --:--:--</div>'
        + '<div id="digital_clock_display_utc" style="flex:1; text-align:center; font-family: Consolas, Menlo, Monaco, monospace; font-size:1.1rem; padding:0.5rem;">UTC: --:--:--</div>'
        + '<div id="digital_clock_display_other" style="flex:1; text-align:center; font-family: Consolas, Menlo, Monaco, monospace; font-size:1.1rem; padding:0.5rem;">Other: --:--:--</div>'
        + "</div>"
        + "\n"
        + '<div style="display:flex; gap:1rem; align-items:flex-start; justify-content:space-around; margin-bottom:1rem;">'
        + '<div id="analog_clock_jst" style="flex:1; width:33%; height:300px;"></div>'
        + '<div id="analog_clock_utc" style="flex:1; width:33%; height:300px;"></div>'
        + '<div id="analog_clock_other" style="flex:1; width:33%; height:300px;"></div>'
        + "</div>"
        + "\n\n"
        + "<script>"
        + js_content
        + "</script>"
    )

    components.html(html_code, height=500)


def print_date(supabase: Client):
    locale.setlocale(locale.LC_TIME, "ja_JP.UTF-8")
    today = datetime.today()

    # 標準の日付表示
    formatted_standard_date = today.strftime("%Y年%m月%d日(%a)")

    # 日本語表記の日付
    wareki = convert_seireki_2_wareki(supabase, today.year, today.month, today.day)
    wareki_year = wareki.split("年")[0]

    # 六曜計算
    rokuyo = calculate_rokuyo(today)

    # 月和名
    month_wamei = {
        1: "睦月",
        2: "如月",
        3: "弥生",
        4: "卯月",
        5: "皐月",
        6: "水無月",
        7: "文月",
        8: "葉月",
        9: "長月",
        10: "神無月",
        11: "霜月",
        12: "師走",
    }
    wamei = month_wamei.get(today.month, "")

    formatted_japanese_date = f"{wareki_year}年 {wamei} {rokuyo}"

    col1, col2 = st.columns([3, 2])
    col1.subheader(formatted_standard_date)
    col2.subheader(formatted_japanese_date)


def draw_clock():
    """
    Streamlit上にアナログ時計を表示する。
    """
    icon = "https://upload.wikimedia.org/wikipedia/commons/thumb/9/94/24_hour_Clock_symbols_icon_11.png/960px-24_hour_Clock_symbols_icon_11.png"

    st.set_page_config(page_title="時計アプリ", page_icon=icon, layout="centered")

    # Supabaseクライアントの初期化
    supabase_client = get_supabase_client()

    # 日付表示
    print_date(supabase_client)

    # 時計表示オフセットを選択するセレクトボックス（都市ベース）
    city_to_offset = {
        "ロンドン (UTC+0)": 0,
        "パリ (UTC+1)": 1,
        "カイロ (UTC+2)": 2,
        "モスクワ (UTC+3)": 3,
        "ドバイ (UTC+4)": 4,
        "イスラマバード (UTC+5)": 5,
        "ダッカ (UTC+6)": 6,
        "バンコク (UTC+7)": 7,
        "北京 (UTC+8)": 8,
        "東京 (UTC+9)": 9,
        "シドニー (UTC+10)": 10,
        "ホニソラ (UTC+11)": 11,
        "カムチャッカ (UTC+12)": 12,
        "ベーカー島 (UTC-12)": -12,
        "ミッドウェー島 (UTC-11)": -11,
        "ホノルル (UTC-10)": -10,
        "アラスカ州 (UTC-9)": -9,
        "L.A. (UTC-8)": -8,
        "デンバー (UTC-7)": -7,
        "シカゴ (UTC-6)": -6,
        "ニューヨーク (UTC-5)": -5,
        "サンディエゴ (UTC-4)": -4,
        "ブエノスアイレス (UTC-3)": -3,
        "サウスジョージア (UTC-2)": -2,
        "アルバ諸島 (UTC-1)": -1,
    }

    city_list = list(city_to_offset.keys())
    # デフォルトは L.A.
    default_index = (
        city_list.index("L.A. (UTC-8)") if "L.A. (UTC-8)" in city_list else 0
    )
    selected_city = st.selectbox(
        "表示する都市を選択してください:",
        city_list,
        index=default_index,
        key="clock_offset_select",
    )
    selected_offset = city_to_offset.get(selected_city, -8)

    # デジタル時計＆アナログ時計の表示（選択したオフセットと都市ラベルで）
    plot_all_clocks_js_only(
        other_offset_hours=selected_offset, city_label=selected_city
    )


if __name__ == "__main__":
    draw_clock()
