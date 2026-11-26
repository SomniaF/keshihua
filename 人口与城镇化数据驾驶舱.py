# -*- coding: utf-8 -*-
"""中国人口与城镇化数据驾驶舱（数据来源：国家统计局历年统计公报）"""
import base64
import math
import time
from pathlib import Path

import plotly.graph_objects as go

FONT = "Microsoft YaHei"
BG = "#F4F6F9"
C_MAIN = "#2F7EA8"
C_ACCENT = "#E08A5F"
C_GREEN = "#5B9A6E"
C_PURPLE = "#7F5FA8"
C_GOLD = "#C9922E"
C_RED = "#C0504D"
C_MUTED = "#8A97A6"

YEARS = list(range(2014, 2026))

POP_TOTAL = [136782, 137462, 138271, 139008, 139538, 140005, 141212, 141260, 141175, 140967, 140828, 140489]
POP_ADD = [710, 680, 809, 737, 530, 467, 1207, 48, -85, -208, -139, -339]
BIRTH_RATE = [12.37, 12.07, 12.95, 12.43, 10.94, 10.48, 8.52, 7.52, 6.77, 6.39, 6.77, 5.63]
DEATH_RATE = [7.16, 7.11, 7.09, 7.11, 7.13, 7.14, 7.07, 7.18, 7.37, 7.87, 7.76, 8.04]
NATURAL_RATE = [5.21, 4.96, 5.86, 5.32, 3.81, 3.34, 1.45, 0.34, -0.60, -1.48, -0.99, -2.41]
URBAN_RATE = [54.77, 56.10, 57.35, 58.52, 59.58, 60.60, 63.89, 64.72, 65.22, 66.16, 67.00, 67.89]

AGE_015 = [17.5, 17.6, 17.7, 17.8, 17.8, 17.8, 17.95, 18.6, 18.1, 17.6, 17.1, 16.4]
AGE_1659 = [67.0, 66.3, 65.6, 64.9, 64.3, 64.0, 63.35, 62.5, 62.0, 61.3, 60.9, 60.6]
AGE_60 = [15.5, 16.1, 16.7, 17.3, 17.9, 18.1, 18.70, 18.9, 19.8, 21.1, 22.0, 23.0]
AGE_65 = [10.1, 10.5, 10.8, 11.4, 11.9, 12.6, 13.50, 14.2, 14.9, 15.4, 15.6, 15.9]

EMPLOYED = [77253, 77451, 77603, 77640, 77586, 77471, 75064, 74652, 73351, 74041, 73439, 72504]
URBAN_EMPLOYED = [39310, 40410, 41428, 42462, 43419, 44247, 46271, 46773, 45931, 47032, 47345, 47535]
MIGRANT = [27395, 27747, 28171, 28652, 28836, 29077, 28560, 29251, 29562, 29753, 29973, 30115]
MIGRANT_PAY = [None, 3072, 3275, 3485, 3721, 3962, 4072, 4432, 4615, 4780, 4961, 5075]


def base_layout(fig, height=330, margin=None):
    fig.update_layout(
        height=height,
        margin=margin or dict(l=58, r=54, t=26, b=44),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family=FONT, size=11.5, color="#2B3A4A"),
        legend=dict(orientation="h", x=0, y=1.16, font=dict(size=10.5),
                    bgcolor="rgba(255,255,255,0)", borderwidth=0),
        hoverlabel=dict(font=dict(family=FONT, size=11)),
    )
    fig.update_xaxes(showgrid=False, zeroline=False, linecolor="#DCE3EA",
                     tickfont=dict(size=10.5, color=C_MUTED))
    fig.update_yaxes(showgrid=True, gridcolor="#EDF1F5", zeroline=False,
                     tickfont=dict(size=10.5, color=C_MUTED))
    return fig


def tick_years():
    return dict(tickmode="array", tickvals=YEARS[::2] + [2025])


def fig_pop():
    from plotly.subplots import make_subplots
    add_colors = [C_RED if v < 0 else "#7FB6D8" for v in POP_ADD]
    fig = make_subplots(rows=2, cols=1, shared_xaxes=True, vertical_spacing=0.09,
                        row_heights=[0.62, 0.38])
    fig.add_trace(go.Scatter(x=YEARS, y=POP_TOTAL, name="年末总人口", mode="lines+markers",
                             fill="tozeroy", fillcolor="rgba(156,201,232,.20)",
                             line=dict(color=C_MAIN, width=2.8), marker=dict(size=5),
                             hovertemplate="%{x}年 总人口 %{y:,} 万人<extra></extra>"), row=1, col=1)
    fig.add_trace(go.Bar(x=YEARS, y=POP_ADD, name="比上年增加", marker_color=add_colors, width=0.58,
                         hovertemplate="%{x}年 增量 %{y:+,} 万人<extra></extra>"), row=2, col=1)
    fig.add_annotation(x=2020, y=POP_TOTAL[6], text="七普口径 141212", showarrow=True, arrowhead=2,
                       ax=-36, ay=-34, arrowcolor=C_MUTED, font=dict(size=9.5, color=C_MUTED),
                       row=1, col=1)
    fig.add_annotation(x=2022, y=-85, text="2022 年首次负增长", showarrow=True, arrowhead=2,
                       ax=-8, ay=-36, arrowcolor=C_RED, font=dict(size=10, color=C_RED), row=2, col=1)
    fig.update_yaxes(range=[130000, 143000], tickformat=",", row=1, col=1)
    fig.update_yaxes(range=[-500, 1400], tickformat="+,", tickvals=[-400, -200, 0, 400, 800, 1200],
                     row=2, col=1)
    fig.update_xaxes(**tick_years())
    fig.update_xaxes(showticklabels=True, row=2, col=1)
    return base_layout(fig, 400, dict(l=64, r=36, t=30, b=40))


def fig_rates():
    fig = go.Figure()
    for name, ys, color, dash in (
        ("出生率", BIRTH_RATE, C_MAIN, None),
        ("死亡率", DEATH_RATE, C_ACCENT, None),
        ("自然增长率", NATURAL_RATE, C_PURPLE, "dot"),
    ):
        fig.add_trace(go.Scatter(x=YEARS, y=ys, name=name, mode="lines+markers",
                                 line=dict(color=color, width=2.4, dash=dash), marker=dict(size=5),
                                 hovertemplate="%{x}年 " + name + " %{y:.2f}‰<extra></extra>"))
    fig.add_hline(y=0, line=dict(color="#B7C1CC", width=1))
    fig.add_annotation(x=2022, y=-0.6, text="2022 年自然增长率转负", showarrow=True, arrowhead=2,
                       ax=26, ay=-42, arrowcolor=C_PURPLE, font=dict(size=10, color=C_PURPLE))
    fig.update_yaxes(range=[-3.5, 14], ticksuffix="‰")
    fig.update_xaxes(**tick_years())
    return base_layout(fig, 330)


def fig_urban():
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=YEARS, y=URBAN_RATE, name="常住人口城镇化率", mode="lines",
                             fill="tozeroy", fillcolor="rgba(156,201,232,.35)",
                             line=dict(color=C_MAIN, width=2.8),
                             hovertemplate="%{x}年 城镇化率 %{y:.2f}%<extra></extra>"))
    fig.add_annotation(x=2014, y=URBAN_RATE[0] + 2.2, text=f"{URBAN_RATE[0]:.2f}%", showarrow=False,
                       font=dict(size=11, color=C_MAIN))
    fig.add_annotation(x=2025, y=URBAN_RATE[-1] + 2.2, text=f"{URBAN_RATE[-1]:.2f}%", showarrow=False,
                       font=dict(size=11.5, color=C_MAIN))
    fig.update_yaxes(range=[50, 72], ticksuffix="%")
    fig.update_xaxes(**tick_years())
    return base_layout(fig, 330)


def fig_age():
    fig = go.Figure()
    for name, ys, color in (
        ("0—15 岁", AGE_015, "#A8D5BA"),
        ("16—59 岁", AGE_1659, "#9CC9E8"),
        ("60 岁及以上", AGE_60, "#F0C38E"),
    ):
        fig.add_trace(go.Scatter(x=YEARS, y=ys, name=name, mode="lines", stackgroup="one",
                                 line=dict(width=0.6, color="white"), fillcolor=color,
                                 hovertemplate=name + " %{y:.1f}%<extra></extra>"))
    fig.add_annotation(x=2025, y=100 - AGE_60[-1] / 2, text=f"{AGE_60[-1]:.1f}%", showarrow=False,
                       xanchor="right", xshift=-8, font=dict(size=11, color="#7A5116"))
    fig.add_annotation(x=2025, y=100 - AGE_60[-1] - AGE_1659[-1] / 2, text=f"{AGE_1659[-1]:.1f}%",
                       showarrow=False, xanchor="right", xshift=-8, font=dict(size=11, color="#1F4E6B"))
    fig.update_yaxes(range=[0, 100], ticksuffix="%")
    fig.update_xaxes(**tick_years())
    return base_layout(fig, 330, dict(l=54, r=30, t=30, b=44))


def fig_65():
    colors = ["#C97B84" if v >= 14 else "#E6B7BB" for v in AGE_65]
    fig = go.Figure(go.Bar(x=YEARS, y=AGE_65, marker_color=colors, width=0.58,
                           text=[f"{v:.1f}" for v in AGE_65], textposition="inside",
                           insidetextanchor="middle", textfont=dict(size=9.5, color="#5A2B31"),
                           hovertemplate="%{x}年 65 岁及以上占比 %{y:.1f}%<extra></extra>"))
    fig.add_hline(y=14, line=dict(color=C_RED, width=1.2, dash="dash"))
    fig.add_annotation(x=0.02, y=0.97, xref="paper", yref="paper", showarrow=False, xanchor="left",
                       text="虚线 = 14% 深度老龄化线", font=dict(size=9.5, color=C_RED))
    fig.update_yaxes(range=[8, 18], ticksuffix="%")
    fig.update_xaxes(**tick_years())
    return base_layout(fig, 330, dict(l=58, r=30, t=30, b=44))


def fig_employed():
    share = [u / e * 100 for u, e in zip(URBAN_EMPLOYED, EMPLOYED)]
    fig = go.Figure()
    fig.add_trace(go.Bar(x=YEARS, y=EMPLOYED, name="就业人员总量", marker_color="#A9C9DE", width=0.6,
                         hovertemplate="%{x}年 就业人员 %{y:,} 万人<extra></extra>"))
    fig.add_trace(go.Scatter(x=YEARS, y=share, name="城镇就业占比", yaxis="y2", mode="lines+markers",
                             line=dict(color=C_GREEN, width=2.4), marker=dict(size=5),
                             hovertemplate="%{x}年 城镇占比 %{y:.1f}%<extra></extra>"))
    fig.update_layout(
        yaxis=dict(range=[68000, 82000], tickformat=","),
        yaxis2=dict(range=[48, 70], overlaying="y", side="right", showgrid=False, ticksuffix="%",
                    tickvals=[50, 55, 60, 65, 70],
                    tickfont=dict(size=10, color=C_GREEN)))
    fig.update_xaxes(**tick_years())
    return base_layout(fig, 330, dict(l=64, r=60, t=30, b=44))


def fig_migrant():
    fig = go.Figure()
    fig.add_trace(go.Bar(x=YEARS, y=MIGRANT, name="农民工总量", marker_color="#B7D3E8", width=0.6,
                         hovertemplate="%{x}年 农民工 %{y:,} 万人<extra></extra>"))
    fig.add_trace(go.Scatter(x=YEARS, y=MIGRANT_PAY, name="月均收入", yaxis="y2", mode="lines+markers",
                             line=dict(color=C_GOLD, width=2.4), marker=dict(size=5), connectgaps=False,
                             hovertemplate="%{x}年 月均收入 %{y:,} 元<extra></extra>"))
    fig.update_layout(
        yaxis=dict(range=[26000, 31000], tickformat=","),
        yaxis2=dict(range=[2500, 5800], overlaying="y", side="right", showgrid=False, tickformat=",",
                    tickvals=[2500, 3000, 3500, 4000, 4500, 5000, 5500],
                    tickfont=dict(size=10, color=C_GOLD)))
    fig.update_xaxes(**tick_years())
    return base_layout(fig, 330, dict(l=64, r=56, t=30, b=44))


def kpi_cards():
    gap = POP_ADD[-1]
    return [
        ('年末总人口', f'{POP_TOTAL[-1]:,}', '万人', f'比上年 {gap:+,} 万人', 'down'),
        ('常住人口城镇化率', f'{URBAN_RATE[-1]:.2f}', '%', f'较上年 +{URBAN_RATE[-1] - URBAN_RATE[-2]:.2f} 个百分点', 'up'),
        ('65 岁及以上占比', f'{AGE_65[-1]:.1f}', '%', f'60 岁及以上 {AGE_60[-1]:.1f}%', 'flat'),
        ('人口自然增长率', f'{NATURAL_RATE[-1]:.2f}', '‰', f'出生率 {BIRTH_RATE[-1]:.2f}‰ / 死亡率 {DEATH_RATE[-1]:.2f}‰', 'down'),
        ('农民工总量', f'{MIGRANT[-1]:,}', '万人', f'月均收入 {MIGRANT_PAY[-1]:,} 元', 'flat'),
    ]


def build_kpis():
    html = []
    for label, value, unit, sub, trend in kpi_cards():
        cls = "delta down" if trend == "down" else ("delta flat" if trend == "flat" else "delta")
        html.append(f'<div class="kpi"><div class="kpi-label">{label}</div>'
                    f'<div class="kpi-value">{value}<span class="unit">{unit}</span></div>'
                    f'<div class="{cls}">{sub}</div></div>')
    return "\n".join(html)


def build_html(figures_html):
    return f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>中国人口与城镇化数据驾驶舱</title>
<style>
  * {{ box-sizing: border-box; }}
  body {{ margin: 0; background: {BG}; font-family: "{FONT}", "PingFang SC", sans-serif; color: #1F2D3D; }}
  .page {{ width: 1560px; margin: 0 auto; padding: 26px 30px 30px; }}
  .top {{ display: flex; align-items: flex-end; justify-content: space-between; margin-bottom: 18px; }}
  .top h1 {{ margin: 0; font-size: 27px; letter-spacing: 1px; }}
  .top h1 span {{ color: {C_MAIN}; }}
  .top .sub {{ margin-top: 7px; font-size: 13px; color: {C_MUTED}; }}
  .badge {{ background: #E6F0F5; color: {C_MAIN}; font-size: 12px; padding: 7px 14px; border-radius: 20px; }}
  .kpis {{ display: grid; grid-template-columns: repeat(5, 1fr); gap: 14px; margin-bottom: 20px; }}
  .kpi {{ background: white; border-radius: 12px; padding: 16px 18px; box-shadow: 0 2px 10px rgba(31,60,100,.06);
          border-left: 3px solid {C_MAIN}; }}
  .kpi:nth-child(2) {{ border-left-color: {C_GREEN}; }}
  .kpi:nth-child(3) {{ border-left-color: {C_ACCENT}; }}
  .kpi:nth-child(4) {{ border-left-color: {C_PURPLE}; }}
  .kpi:nth-child(5) {{ border-left-color: {C_GOLD}; }}
  .kpi-label {{ font-size: 12px; color: {C_MUTED}; }}
  .kpi-value {{ font-size: 30px; font-weight: 700; margin: 7px 0 5px; font-variant-numeric: tabular-nums; }}
  .kpi-value .unit {{ font-size: 13px; font-weight: 400; color: {C_MUTED}; margin-left: 4px; }}
  .delta {{ font-size: 11px; color: #2E9E8F; }}
  .delta.down {{ color: #C0504D; }}
  .delta.flat {{ color: {C_MUTED}; }}
  .section {{ display: flex; align-items: center; gap: 10px; margin: 22px 0 12px; }}
  .section .bar {{ width: 4px; height: 17px; background: {C_MAIN}; border-radius: 2px; }}
  .section h2 {{ font-size: 16px; margin: 0; }}
  .section .hint {{ font-size: 12px; color: {C_MUTED}; margin-left: auto; }}
  .grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: 16px; }}
  .card {{ background: white; border-radius: 14px; padding: 16px 18px 8px; box-shadow: 0 2px 12px rgba(31,60,100,.06); }}
  .card.wide {{ grid-column: span 2; }}
  .card h3 {{ font-size: 14px; margin: 0 0 2px; }}
  .card .desc {{ font-size: 11.5px; color: {C_MUTED}; margin-bottom: 4px; }}
  .foot {{ margin-top: 20px; font-size: 11.5px; color: {C_MUTED}; line-height: 1.8; }}
</style>
</head>
<body>
<div class="page">
  <div class="top">
    <div>
      <h1>中国<span>人口与城镇化</span>数据驾驶舱</h1>
      <div class="sub">2014—2025 年 · 总量、自然变动、年龄结构与就业流动 · 共 7 张交互图表</div>
    </div>
    <div class="badge">国家统计局 · 年度统计公报 2014—2025</div>
  </div>

  <div class="kpis">{build_kpis()}</div>

  <div class="section"><div class="bar"></div><h2>01 · 总量与自然变动</h2>
    <div class="hint">总人口、出生死亡与自然增长</div></div>
  <div class="grid">
    <div class="card wide"><h3>年末总人口与年度增量</h3>
      <div class="desc">上图为年末总人口（万人），下图为比上年增量（万人）；2022 年起总人口连续四年下降</div>{figures_html['pop']}</div>
    <div class="card"><h3>出生率、死亡率与自然增长率</h3>
      <div class="desc">千分率（‰）；自然增长率 2022 年由正转负</div>{figures_html['rates']}</div>
    <div class="card"><h3>常住人口城镇化率</h3>
      <div class="desc">城镇常住人口占总人口比重（%），十二年间提高 13.12 个百分点</div>{figures_html['urban']}</div>
  </div>

  <div class="section"><div class="bar"></div><h2>02 · 结构变迁</h2>
    <div class="hint">年龄结构老龄化与城镇化</div></div>
  <div class="grid">
    <div class="card wide"><h3>人口年龄结构（占比 %）</h3>
      <div class="desc">0—15 岁、16—59 岁与 60 岁及以上人口占比的 100% 堆积图</div>{figures_html['age']}</div>
    <div class="card"><h3>65 岁及以上人口占比</h3>
      <div class="desc">占总人口比重（%），红色为跨过 14% 深度老龄化线的年份</div>{figures_html['65']}</div>
    <div class="card"><h3>就业人员总量与城镇就业占比</h3>
      <div class="desc">就业人员（柱，万人）与城镇就业人员占比（线，%）</div>{figures_html['employed']}</div>
  </div>

  <div class="section"><div class="bar"></div><h2>03 · 流动人口</h2>
    <div class="hint">农民工规模与收入</div></div>
  <div class="grid">
    <div class="card wide"><h3>农民工总量与月均收入</h3>
      <div class="desc">农民工总量（柱，万人）与月均收入（线，元）；2014 年公报未披露农民工月均收入，收入线自 2015 年起</div>{figures_html['migrant']}</div>
  </div>

  <div class="foot">
    数据来源：国家统计局《中华人民共和国国民经济和社会发展统计公报》（2014—2025 年）、第七次全国人口普查公报。
    2020 年公报未刊载人口构成表，总人口、城镇化率、年龄结构采用第七次全国人口普查数据（141212 万人、63.89%、65 岁及以上 13.50%），
    出生率 8.52‰、死亡率 7.07‰、自然增长率 1.45‰ 取 2020 年人口变动口径。
    就业人员 2020 年按第七次全国人口普查口径修订，与 2019 年存在口径差异；农民工月均收入自 2015 年起（2014 年公报未披露）。
  </div>
</div>
</body>
</html>"""


def render_html(out_html):
    figs = {
        "pop": fig_pop(),
        "rates": fig_rates(),
        "urban": fig_urban(),
        "age": fig_age(),
        "65": fig_65(),
        "employed": fig_employed(),
        "migrant": fig_migrant(),
    }
    config = {"displaylogo": False, "responsive": True,
              "modeBarButtonsToRemove": ["lasso2d", "select2d", "autoScale2d"]}
    js = None
    out = {}
    for key, fig in figs.items():
        html = fig.to_html(full_html=False, include_plotlyjs=("inline" if js is None else False),
                           config=config, default_width="100%", default_height=fig.layout.height)
        js = True
        out[key] = html
    out_html.write_text(build_html(out), encoding="utf-8")
    return out_html


CHROME_CANDIDATES = [
    r"D:\pachong111\chrome-win64\chrome.exe",
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
]
DRIVER_CANDIDATES = [
    r"D:\chromedriver\chromedriver.exe",
    r"C:\chromedriver\chromedriver.exe",
]


def screenshot(html_path, png_path, expect=7):
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.chrome.service import Service
    from selenium.webdriver.support.ui import WebDriverWait

    chrome = next((p for p in CHROME_CANDIDATES if Path(p).exists()), None)
    driver_bin = next((p for p in DRIVER_CANDIDATES if Path(p).exists()), None)
    opts = Options()
    if chrome:
        opts.binary_location = chrome
    for arg in ("--headless=new", "--disable-gpu", "--no-sandbox", "--hide-scrollbars",
                "--window-size=1600,1200"):
        opts.add_argument(arg)
    service = Service(driver_bin) if driver_bin else Service()
    drv = webdriver.Chrome(service=service, options=opts)
    try:
        drv.get(html_path.as_uri())
        WebDriverWait(drv, 60).until(
            lambda d: d.execute_script(
                "return document.querySelectorAll('.js-plotly-plot').length") >= expect)
        time.sleep(2.5)
        metrics = drv.execute_cdp_cmd("Page.getLayoutMetrics", {})
        size = metrics.get("cssContentSize") or metrics["contentSize"]
        width = math.ceil(size["width"])
        height = math.ceil(size["height"])
        shot = drv.execute_cdp_cmd("Page.captureScreenshot", {
            "format": "png", "captureBeyondViewport": True,
            "clip": {"x": 0, "y": 0, "width": width, "height": height, "scale": 2},
        })
        data = base64.b64decode(shot["data"])
        for attempt in range(3):
            try:
                png_path.write_bytes(data)
                break
            except OSError:
                if attempt == 2:
                    raise
                time.sleep(1)
    finally:
        drv.quit()


if __name__ == "__main__":
    out_dir = Path(__file__).resolve().parent
    html_path = render_html(out_dir / "人口与城镇化数据驾驶舱.html")
    print(f"已生成交互大屏：{html_path}")
    png_path = out_dir / "人口与城镇化数据驾驶舱.png"
    try:
        screenshot(html_path, png_path, expect=7)
        print(f"已生成截图：{png_path}")
    except Exception as exc:
        print(f"截图失败（HTML 仍可用）：{exc}")
