import streamlit as st
import streamlit.components.v1 as components
# import matplotlib.pyplot as plt
# import numpy as np
from datetime import datetime
import time
import locale
import pytz
from lunardate import LunarDate
from supabase import Client
# from streamlit_echarts import st_echarts
# from streamlit_autorefresh import st_autorefresh
from libs.supabase_client import get_supabase_client
from tools.wareki import convert_seireki_2_wareki

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

def plot_all_clocks_js_only(jst_offset_hours=9):
    """
    デジタル時計とアナログ時計の両方をJSで自己更新する
    HTMLコンポーネントを「1回だけ」描画する関数
    （アナログ秒針をデジタルと同期させ、体感ズレを解消）
    """

    html_code = f"""
    <script src="https://cdn.jsdelivr.net/npm/echarts@5.5.0/dist/echarts.min.js"></script>

    <div id="digital_clock_display" style="
        font-family: 'Consolas', 'Menlo', 'Monaco', 'monospace';
        font-size: 1.1rem;
        padding-bottom: 1rem;
    ">
        現在時刻: --:--:--
    </div>

    <div id="analog_clock_chart" style="width: 100%; height: 400px;"></div>

    <script>
        var chartDom = document.getElementById('analog_clock_chart');
        var myChart = echarts.init(chartDom);
        var digitalClockDom = document.getElementById('digital_clock_display');

        const jstOffsetHours = {jst_offset_hours};

        // アナログ時計のオプション
        var option = {{
            series: [
                // 1. 時計盤
                {{
                    type: "gauge", startAngle: 90, endAngle: -270,
                    min: 0, max: 12, splitNumber: 4,
                    axisLine: {{ lineStyle: {{ width: 10 }} }},
                    axisTick: {{ show: false }},
                    splitLine: {{ length: 15, lineStyle: {{ width: 3 }} }},
                    axisLabel: {{
                        distance: 15, fontSize: 18,
                        formatter: function(value) {{
                            if (value === 0) {{ return ''; }} return value;
                        }}
                    }},
                    pointer: {{ show: false }}, detail: {{ show: false }},
                    animation: false,
                }},
                // 2. 時針
                {{
                    type: "gauge", startAngle: 90, endAngle: -270,
                    min: 0, max: 12, axisLine: {{ show: false }},
                    axisTick: {{ show: false }}, splitLine: {{ show: false }},
                    axisLabel: {{ show: false }},
                    pointer: {{ width: 8, length: "60%" }},
                    detail: {{ show: false }}, animation: false,
                    data: [{{ value: 0 }}]
                }},
                // 3. 分針
                {{
                    type: "gauge", startAngle: 90, endAngle: -270,
                    min: 0, max: 60, axisLine: {{ show: false }},
                    axisTick: {{ show: false }}, splitLine: {{ show: false }},
                    axisLabel: {{ show: false }},
                    pointer: {{ width: 4, length: "80%" }},
                    detail: {{ show: false }}, animation: false,
                    data: [{{ value: 0 }}]
                }},
                // 4. 秒針 (ズレ修正済み)
                {{
                    type: "gauge",
                    startAngle: 90, endAngle: -270,
                    min: 0, max: 60,
                    "splitNumber": 12, // 5秒ごと
                    "axisLine": {{ "show": false }},
                    "axisTick": {{
                        "show": true, "splitNumber": 5, "length": 8, // 1秒ごと
                        "lineStyle": {{ "width": 1 }}
                    }},
                    "splitLine": {{
                        "show": true, "length": 12, "lineStyle": {{ "width": 2 }}
                    }},
                    "axisLabel": {{ "show": false }},
                    "pointer": {{ "width": 2, "length": "90%", "itemStyle": {{ "color": "red" }} }},
                    "detail": {{ "show": false }}, "animation": false,
                    "data": [{{ value: 0 }}]
                }}
            ]
        }};

        myChart.setOption(option);

        // --- 時計を更新する関数 ---
        function updateAllClocks() {{

            // JST計算
            const localNow = new Date();
            const localOffsetMinutes = localNow.getTimezoneOffset();
            const utcMillis = localNow.getTime() + (localOffsetMinutes * 60 * 1000);
            const jstMillis = utcMillis + (jstOffsetHours * 60 * 60 * 1000);
            const now = new Date(jstMillis);

            // アナログ時計の計算
            const h = (now.getHours() % 12) + now.getMinutes() / 60;
            const m = now.getMinutes() + now.getSeconds() / 60;

            // ----------------------------------------------------
            // 修正点：ミリ秒を切り捨て、デジタル時計と同期させる
            const s = now.getSeconds() + 1;
            // ----------------------------------------------------

            myChart.setOption({{
                series: [
                    {{}},
                    {{ data: [{{ value: h }}] }},
                    {{ data: [{{ value: m }}] }},
                    {{ data: [{{ value: s }}] }},
                ]
            }});

            // デジタル時計の計算
            const digital_h = String(now.getHours()).padStart(2, '0');
            const digital_m = String(now.getMinutes()).padStart(2, '0');
            const digital_s = String(now.getSeconds() + 1).padStart(2, '0');

            digitalClockDom.innerText = `現在時刻: ${{digital_h}}:${{digital_m}}:${{digital_s}}`;
        }}

        // --- 遅延蓄積を解消する再帰ループ ---
        function tick() {{
            // 1. 「次の秒の0ミリ秒」までの遅延を計算
            const now = new Date();
            const millis = now.getMilliseconds();
            const delay = 1000 - millis;

            // 2. 計算した遅延後に「更新と次のタイマーセット」を実行
            setTimeout(() => {{
                // 3. ほぼ0ミリ秒時点で時刻を更新（描画）
                updateAllClocks();

                // 4. 次のタイマー（tick自身）をセット
                tick();
            }}, delay);
        }}

        // 最初のタイマーだけセット
        tick();

    </script>
    """

    components.html(html_code, height=450)


def print_date(supabase: Client):
    locale.setlocale(locale.LC_TIME, "ja_JP.UTF-8")
    today = datetime.today()

    wareki = convert_seireki_2_wareki(supabase, today.year, today.month, today.day)
    wareki_year = wareki.split("年")[0]

    rokuyo = calculate_rokuyo(today)

    # strftime()メソッドを使って日付と曜日をフォーマット
    formatted_month_date_ja = today.strftime("%m月%d日(%a)")
    formatted_date_ja = f"{today.year}({wareki_year})年{formatted_month_date_ja} {rokuyo}"
    st.title(formatted_date_ja)


def draw_clock():
    """
    Streamlit上にアナログ時計を表示する。
    """
    # Supabaseクライアントの初期化
    supabase_client = get_supabase_client()

    icon = "https://upload.wikimedia.org/wikipedia/commons/thumb/9/94/24_hour_Clock_symbols_icon_11.png/960px-24_hour_Clock_symbols_icon_11.png"

    st.set_page_config(page_title="時計アプリ", page_icon=icon, layout="centered")
    st.logo(icon)
    # st.title("時計アプリ")

    # st_autorefresh(interval=1000, key="clock_autorefresh")
    # count = st_autorefresh(interval=1000, limit=None, key="clock_refresh")

    print_date(supabase_client)

    # 時計をリアルタイムで更新
    # placeholder1 = st.empty()

    # アナログ時計の表示
    # plot_clock()
    plot_all_clocks_js_only(jst_offset_hours=9)

    # while True:
    #     now = get_tz_time("Asia/Tokyo")
    #     with placeholder1.container():
    #         # デジタル時計の表示
    #         digital_time = now.strftime("%H:%M:%S")
    #         st.text(f"現在時刻: {digital_time}")

        # with placeholder2.container():
            # アナログ時計の表示
            # plot_clock(now=now)
            # plot_clock(now, count)
        #     fig = plot_clock(now)
        #     st.pyplot(fig, width="content")
        #     plt.close(fig)  # 図を閉じてメモリを解放

        # time.sleep(1)


if __name__ == "__main__":
    # if "initialized" not in st.session_state:
    #     st.session_state["initialized"] = True
    #     st_autorefresh(interval=1000, limit=None, key="clock_refresh")

    draw_clock()
