// Clock script extracted from Python HTML embed
// This file expects the following DOM elements to exist in the host HTML:
// - #analog_clock_chart
// - #digital_clock_display_jst
// - #digital_clock_display_utc
// The placeholder /*JST_OFFSET_PLACEHOLDER*/ will be replaced by Python with the numeric offset.

const chartDom = document.getElementById("analog_clock_chart");
const myChart = echarts.init(chartDom);
const digitalClockDomJst = document.getElementById("digital_clock_display_jst");
const digitalClockDomUtc = document.getElementById("digital_clock_display_utc");

// JST offset placeholder: when embedding from Python, the identifier
// `JST_OFFSET_PLACEHOLDER` will be replaced with a number. To keep
// this file valid JavaScript on its own (for linting/editing), we
// resolve it safely with a fallback of 9 (JST).
const jstOffsetHours =
  typeof JST_OFFSET_PLACEHOLDER !== "undefined" ? JST_OFFSET_PLACEHOLDER : 9;

// City label placeholder: replaced by Python with a JS string literal
const cityLabel =
  typeof CITY_LABEL_PLACEHOLDER !== "undefined"
    ? CITY_LABEL_PLACEHOLDER
    : "JST(UTC+9)";

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

myChart.setOption(option);

// 時計を更新する関数
function updateAllClocks() {
  const localNow = new Date();
  const localOffsetMinutes = localNow.getTimezoneOffset();
  const utcMillis = localNow.getTime() + localOffsetMinutes * 60 * 1000;
  const jstMillis = utcMillis + jstOffsetHours * 60 * 60 * 1000;
  const now = new Date(jstMillis);

  const h = (now.getHours() % 12) + now.getMinutes() / 60;
  const m = now.getMinutes() + now.getSeconds() / 60;
  const s = now.getSeconds();

  myChart.setOption({
    series: [
      {},
      { data: [{ value: h }] },
      { data: [{ value: m }] },
      { data: [{ value: s }] },
    ],
  });

  // デジタル表示
  const digital_h = String(now.getHours()).padStart(2, "0");
  const digital_m = String(now.getMinutes()).padStart(2, "0");
  const digital_s = String(now.getSeconds()).padStart(2, "0");
  digitalClockDomJst.innerText = `${cityLabel}: ${digital_h}:${digital_m}:${digital_s}`;

  const utc_h = String(localNow.getUTCHours()).padStart(2, "0");
  const utc_m = String(localNow.getUTCMinutes()).padStart(2, "0");
  const utc_s = String(localNow.getUTCSeconds()).padStart(2, "0");
  digitalClockDomUtc.innerText = `UTC: ${utc_h}:${utc_m}:${utc_s}`;
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

  digitalClockDomJst.style.color = textColor;
  digitalClockDomUtc.style.color = textColor;
  digitalClockDomJst.style.backgroundColor = backgroundColor;
  digitalClockDomUtc.style.backgroundColor = backgroundColor;
  chartDom.style.backgroundColor = backgroundColor;
}

// 初期起動
tick();

// ダークモード監視
const darkModeMediaQuery = window.matchMedia("(prefers-color-scheme: dark)");
applyDarkModeStyles(darkModeMediaQuery.matches);
darkModeMediaQuery.addEventListener("change", function (event) {
  applyDarkModeStyles(event.matches);
});
