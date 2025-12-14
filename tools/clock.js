// Clock script extracted from Python HTML embed
// This file expects the following DOM elements to exist in the host HTML:
// - #analog_clock_jst
// - #analog_clock_utc
// - #analog_clock_other
// - #digital_clock_display_jst
// - #digital_clock_display_utc
// - #digital_clock_display_other
// The placeholder /*OTHER_OFFSET_PLACEHOLDER*/ will be replaced by Python with the numeric offset.

// three chart containers (JST / UTC / Other)
const chartDomJst = document.getElementById("analog_clock_jst");
const chartDomUtc = document.getElementById("analog_clock_utc");
const chartDomOther = document.getElementById("analog_clock_other");
const myChartJst = chartDomJst ? echarts.init(chartDomJst) : null;
const myChartUtc = chartDomUtc ? echarts.init(chartDomUtc) : null;
const myChartOther = chartDomOther ? echarts.init(chartDomOther) : null;

const digitalClockDomJst = document.getElementById("digital_clock_display_jst");
const digitalClockDomUtc = document.getElementById("digital_clock_display_utc");
const digitalClockDomOther = document.getElementById(
  "digital_clock_display_other"
);

// JST is fixed
const jstOffsetHours = 9;

// otherOffsetHours placeholder: replaced by Python with numeric offset
const otherOffsetHours =
  typeof OTHER_OFFSET_PLACEHOLDER !== "undefined"
    ? OTHER_OFFSET_PLACEHOLDER
    : -8;

// City label placeholder: replaced by Python with a JS string literal for the "other" timezone
const cityLabel =
  typeof CITY_LABEL_PLACEHOLDER !== "undefined"
    ? CITY_LABEL_PLACEHOLDER
    : "Other (UTC)";

// アナログ時計のオプション
const option = {
  series: [
    // 1. 時計盤
    {
      type: "gauge",
      startAngle: 90,
      endAngle: -270,
      min: 0,
      max: 12,
      splitNumber: 4,
      axisLine: { lineStyle: { width: 10 } },
      axisTick: { show: false },
      splitLine: { length: 15, lineStyle: { width: 3 } },
      axisLabel: {
        distance: 15,
        fontSize: 18,
        formatter: function (value) {
          if (value === 0) {
            return "";
          }
          return value;
        },
      },
      pointer: { show: false },
      detail: { show: false },
      animation: false,
    },
    // 2. 時針
    {
      type: "gauge",
      startAngle: 90,
      endAngle: -270,
      min: 0,
      max: 12,
      axisLine: { show: false },
      axisTick: { show: false },
      splitLine: { show: false },
      axisLabel: { show: false },
      pointer: { width: 8, length: "60%" },
      detail: { show: false },
      animation: false,
      data: [{ value: 0 }],
    },
    // 3. 分針
    {
      type: "gauge",
      startAngle: 90,
      endAngle: -270,
      min: 0,
      max: 60,
      axisLine: { show: false },
      axisTick: { show: false },
      splitLine: { show: false },
      axisLabel: { show: false },
      pointer: { width: 4, length: "80%" },
      detail: { show: false },
      animation: false,
      data: [{ value: 0 }],
    },
    // 4. 秒針
    {
      type: "gauge",
      startAngle: 90,
      endAngle: -270,
      min: 0,
      max: 60,
      splitNumber: 12,
      axisLine: { show: false },
      axisTick: {
        show: true,
        splitNumber: 5,
        length: 8,
        lineStyle: { width: 1 },
      },
      splitLine: { show: true, length: 12, lineStyle: { width: 2 } },
      axisLabel: { show: false },
      pointer: { width: 2, length: "90%", itemStyle: { color: "red" } },
      detail: { show: false },
      animation: false,
      data: [{ value: 0 }],
    },
  ],
};

if (myChartJst) myChartJst.setOption(option);
if (myChartUtc) myChartUtc.setOption(option);
if (myChartOther) myChartOther.setOption(option);

// 時計を更新する関数
function updateAllClocks() {
  const localNow = new Date();
  const localOffsetMinutes = localNow.getTimezoneOffset();
  const utcMillis = localNow.getTime() + localOffsetMinutes * 60 * 1000;

  // JST clock
  const jstMillis = utcMillis + jstOffsetHours * 60 * 60 * 1000;
  const nowJst = new Date(jstMillis);
  const hJst = (nowJst.getHours() % 12) + nowJst.getMinutes() / 60;
  const mJst = nowJst.getMinutes() + nowJst.getSeconds() / 60;
  const sJst = nowJst.getSeconds();
  if (myChartJst) {
    myChartJst.setOption({
      series: [
        {},
        { data: [{ value: hJst }] },
        { data: [{ value: mJst }] },
        { data: [{ value: sJst }] },
      ],
    });
  }

  // UTC clock
  const nowUtc = new Date(utcMillis);
  const hUtc = (nowUtc.getHours() % 12) + nowUtc.getMinutes() / 60;
  const mUtc = nowUtc.getMinutes() + nowUtc.getSeconds() / 60;
  const sUtc = nowUtc.getSeconds();
  if (myChartUtc) {
    myChartUtc.setOption({
      series: [
        {},
        { data: [{ value: hUtc }] },
        { data: [{ value: mUtc }] },
        { data: [{ value: sUtc }] },
      ],
    });
  }

  // Other clock (selected offset)
  const otherMillis = utcMillis + otherOffsetHours * 60 * 60 * 1000;
  const nowOther = new Date(otherMillis);
  const hOther = (nowOther.getHours() % 12) + nowOther.getMinutes() / 60;
  const mOther = nowOther.getMinutes() + nowOther.getSeconds() / 60;
  const sOther = nowOther.getSeconds();
  if (myChartOther) {
    myChartOther.setOption({
      series: [
        {},
        { data: [{ value: hOther }] },
        { data: [{ value: mOther }] },
        { data: [{ value: sOther }] },
      ],
    });
  }

  // デジタル表示（JST 固定）
  const digital_h = String(nowJst.getHours()).padStart(2, "0");
  const digital_m = String(nowJst.getMinutes()).padStart(2, "0");
  const digital_s = String(nowJst.getSeconds()).padStart(2, "0");
  if (digitalClockDomJst)
    digitalClockDomJst.innerText = `JST(UTC+9): ${digital_h}:${digital_m}:${digital_s}`;

  // UTC 表示
  const utc_h = String(
    nowUtc.getUTCHours ? nowUtc.getUTCHours() : nowUtc.getHours()
  ).padStart(2, "0");
  const utc_m = String(
    nowUtc.getUTCMinutes ? nowUtc.getUTCMinutes() : nowUtc.getMinutes()
  ).padStart(2, "0");
  const utc_s = String(
    nowUtc.getUTCSeconds ? nowUtc.getUTCSeconds() : nowUtc.getSeconds()
  ).padStart(2, "0");
  if (digitalClockDomUtc)
    digitalClockDomUtc.innerText = `UTC: ${utc_h}:${utc_m}:${utc_s}`;

  // Other（選択されたオフセット）の計算と表示
  const other_h = String(nowOther.getHours()).padStart(2, "0");
  const other_m = String(nowOther.getMinutes()).padStart(2, "0");
  const other_s = String(nowOther.getSeconds()).padStart(2, "0");
  if (digitalClockDomOther) {
    digitalClockDomOther.innerText = `${cityLabel}: ${other_h}:${other_m}:${other_s}`;
  }
}

function tick() {
  const now = new Date();
  const millis = now.getMilliseconds();
  const delay = 1000 - millis;
  setTimeout(() => {
    updateAllClocks();
    tick();
  }, delay);
}

// ダークモードのスタイル適用関数
function applyDarkModeStyles(isDarkMode) {
  const textColor = isDarkMode ? "#FFFFFF" : "#000000";
  const backgroundColor = isDarkMode ? "#333333" : "#FFFFFF";

  if (digitalClockDomJst) {
    digitalClockDomJst.style.color = textColor;
    digitalClockDomJst.style.backgroundColor = backgroundColor;
  }
  if (digitalClockDomUtc) {
    digitalClockDomUtc.style.color = textColor;
    digitalClockDomUtc.style.backgroundColor = backgroundColor;
  }
  if (digitalClockDomOther) {
    digitalClockDomOther.style.color = textColor;
    digitalClockDomOther.style.backgroundColor = backgroundColor;
  }
  if (chartDomJst) chartDomJst.style.backgroundColor = backgroundColor;
  if (chartDomUtc) chartDomUtc.style.backgroundColor = backgroundColor;
  if (chartDomOther) chartDomOther.style.backgroundColor = backgroundColor;
}

// 初期起動
tick();

// ダークモード監視
const darkModeMediaQuery = window.matchMedia("(prefers-color-scheme: dark)");
applyDarkModeStyles(darkModeMediaQuery.matches);
darkModeMediaQuery.addEventListener("change", function (event) {
  applyDarkModeStyles(event.matches);
});
