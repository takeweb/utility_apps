from datetime import datetime
import pytz
from lunardate import LunarDate


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


def get_month_wamei(month):
    """
    月和名
    """
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
    return month_wamei.get(month, "")


def format_us_date(dt):
    weekday_en = [
        "Mon",
        "Tue",
        "Wed",
        "Thu",
        "Fri",
        "Sat",
        "Sun",
    ]
    month_en = [
        "January",
        "February",
        "March",
        "April",
        "May",
        "June",
        "July",
        "August",
        "September",
        "October",
        "November",
        "December",
    ]

    return f"{weekday_en[dt.weekday()]}, {month_en[dt.month - 1]} {dt.day}, {dt.year}"


def get_zyunisi(year: int) -> str:
    """
    指定された年の十二支を取得する関数。
    :param year: 西暦年
    :return: 十二支（文字列）
    """
    zyunisi_list = [
        "子",
        "丑",
        "寅",
        "卯",
        "辰",
        "巳",
        "午",
        "未",
        "申",
        "酉",
        "戌",
        "亥",
    ]
    index = (year - 4) % 12  # 子年が 4 の年に対応
    return zyunisi_list[index]
