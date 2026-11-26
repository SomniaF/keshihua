# -*- coding: utf-8 -*-
"""嘉兴大学本科招生专业结构旭日图

专业清单：嘉兴大学教务处《嘉兴大学普通高等学校本科专业设置一览表》
https://jwc.zjxu.edu.cn/jgsz/zysz.htm （抓取日期 2026-11-19）
招生状态：仅保留 2026 年实际招生的 48 个本科专业（学校官网“学校简介”及
2026 年招办访谈口径，含 3 个艺术类专业；停招/未招生专业已剔除）。
"""
import colorsys
from pathlib import Path

import plotly.graph_objects as go
import plotly.io as pio

ROOT = "嘉兴大学"
FONT = "Microsoft YaHei"

# 学院简介中的常用简称（用于图上显示，悬停仍显示全称）
SHORT_NAMES = {
    "马克思主义学院（中共党史党建学院）": "马克思主义学院",
    "机械工程学院（机器人工程学院）": "机械工程学院",
}

# (学院, 专业名称, 专业代码, 授予学位门类, 专业类名称)
MAJORS = [
    ("经济学院", "经济学", "020101", "经济学", "经济学类"),
    ("经济学院", "金融学", "020301K", "经济学", "金融学类"),
    ("经济学院", "跨境电子商务", "120803T", "管理学", "电子商务类"),
    ("经济学院", "数字经济", "020109T", "经济学", "经济学类"),
    ("商学院", "会计学", "120203K", "管理学", "工商管理类"),
    ("商学院", "人力资源管理", "120206", "管理学", "工商管理类"),
    ("商学院", "财务管理", "120204", "管理学", "工商管理类"),
    ("商学院", "工商管理", "120201K", "管理学", "工商管理类"),
    ("马克思主义学院（中共党史党建学院）", "中国共产党历史", "030502", "法学", "马克思主义理论类"),
    ("信息科学与工程学院", "电子信息工程", "080701", "工学", "电子信息类"),
    ("信息科学与工程学院", "通信工程", "080703", "工学", "电子信息类"),
    ("信息科学与工程学院", "低空技术与工程", "083203TK", "工学", "交叉工程类"),
    ("机械工程学院（机器人工程学院）", "智能制造工程", "080213T", "工学", "机械类"),
    ("机械工程学院（机器人工程学院）", "机械设计制造及其自动化", "080202", "工学", "机械类"),
    ("机械工程学院（机器人工程学院）", "电气工程及其自动化", "080601", "工学", "电气类"),
    ("机械工程学院（机器人工程学院）", "机器人工程", "080803T", "工学", "自动化类"),
    ("人工智能学院", "计算机科学与技术", "080901", "工学", "计算机类"),
    ("人工智能学院", "人工智能", "080717T", "工学", "电子信息类"),
    ("数据科学学院", "数学与应用数学", "070101", "理学", "数学类"),
    ("数据科学学院", "应用统计学", "071202", "理学", "统计学类"),
    ("数据科学学院", "数据科学与大数据技术", "080910T", "工学", "计算机类"),
    ("数据科学学院", "金融数学", "020305T", "经济学", "金融学类"),
    ("医学院", "临床医学", "100201K", "医学", "临床医学类"),
    ("医学院", "护理学", "101101K", "理学", "护理学类"),
    ("医学院", "药学", "100701", "理学", "药学类"),
    ("医学院", "麻醉学", "100202TK", "医学", "临床医学类"),
    ("设计学院", "服装设计与工程", "081602", "工学", "纺织类"),
    ("设计学院", "工业设计", "080205", "工学", "机械类"),
    ("设计学院", "视觉传达设计", "130502", "艺术学", "设计学类"),
    ("设计学院", "环境设计", "130503", "艺术学", "设计学类"),
    ("设计学院", "数字媒体艺术", "130508", "艺术学", "设计学类"),
    ("生物与化学工程学院", "应用化学", "070302", "工学", "化学类"),
    ("生物与化学工程学院", "化学工程与工艺", "081301", "工学", "化工与制药类"),
    ("生物与化学工程学院", "制药工程", "081302", "工学", "化工与制药类"),
    ("生物与化学工程学院", "环境工程", "082502", "工学", "环境科学与工程类"),
    ("材料与纺织工程学院", "纺织工程", "081601", "工学", "纺织类"),
    ("材料与纺织工程学院", "高分子材料与工程", "080407", "工学", "材料类"),
    ("材料与纺织工程学院", "轻化工程", "081701", "工学", "轻工类"),
    ("材料与纺织工程学院", "新能源材料与器件", "080414T", "工学", "材料类"),
    ("建筑工程学院", "工程管理", "120103", "工学", "管理科学与工程类"),
    ("建筑工程学院", "建筑环境与能源应用工程", "081002", "工学", "土木类"),
    ("建筑工程学院", "土木工程", "081001", "工学", "土木类"),
    ("文法学院", "汉语言文学", "050101", "文学", "中国语言文学类"),
    ("文法学院", "法学", "030101K", "法学", "法学类"),
    ("文法学院", "知识产权", "030102T", "法学", "法学类"),
    ("外国语学院", "英语", "050201", "文学", "外国语言文学类"),
    ("教育学院", "小学教育", "040107", "教育学", "教育学类"),
    ("教育学院", "体育教育", "040201", "教育学", "体育学类"),
]

def _hsl_hex(hue, sat, light):
    r, g, b = colorsys.hls_to_rgb(hue / 360, light, sat)
    return "#%02X%02X%02X" % (round(r * 255), round(g * 255), round(b * 255))


def _rel_lum(r, g, b):
    def ch(c):
        return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4
    return 0.2126 * ch(r) + 0.7152 * ch(g) + 0.0722 * ch(b)


def _tone(hue, sat, lum):
    lo, hi = 0.0, 1.0
    for _ in range(30):
        mid = (lo + hi) / 2
        if _rel_lum(*colorsys.hls_to_rgb(hue / 360, mid, sat)) < lum:
            lo = mid
        else:
            hi = mid
    return _hsl_hex(hue, sat, (lo + hi) / 2)


def college_palette(n):
    # 16 色环按位反转顺序取色，相邻学院色相至少相差 67.5°；
    # 再按统一相对亮度校准，避免蓝紫色看着发黑、黄色看着发亮
    slots = [0, 8, 4, 12, 2, 10, 6, 14, 1, 9, 5, 13, 3, 11, 7, 15]
    return [
        (_tone(slots[i % 16] * 22.5, 0.68, 0.34),
         _tone(slots[i % 16] * 22.5, 0.68, 0.55))
        for i in range(n)
    ]


def build_data():
    colleges = []
    for college, *_ in MAJORS:
        if college not in colleges:
            colleges.append(college)

    ids = [ROOT]
    labels = [ROOT]
    parents = [""]
    values = [len(MAJORS)]
    colors = ["#E5E7EB"]
    full_names = ["嘉兴大学"]
    details = [f"{len(colleges)} 个学院 · {len(MAJORS)} 个本科专业"]

    palette = college_palette(len(colleges))

    for idx, college in enumerate(colleges):
        inner_color, major_color = palette[idx]
        major_rows = [m for m in MAJORS if m[0] == college]
        degree_count = {}
        for m in major_rows:
            degree_count[m[3]] = degree_count.get(m[3], 0) + 1

        ids.append(college)
        labels.append(SHORT_NAMES.get(college, college))
        parents.append(ROOT)
        values.append(len(major_rows))
        colors.append(inner_color)
        full_names.append(college)
        detail = "，".join(f"{d}学位{c}个" for d, c in degree_count.items())
        details.append(f"共 {len(major_rows)} 个本科专业（{detail}）")

        for _, major, code, degree, major_class in major_rows:
            ids.append(f"{college}/{major}")
            labels.append(major)
            parents.append(college)
            values.append(1)
            colors.append(major_color)
            full_names.append(college)
            details.append(f"{college} · {degree}学士 · {major_class} · 专业代码 {code}")

    return ids, labels, parents, values, colors, full_names, details


def make_figure():
    ids, labels, parents, values, colors, full_names, details = build_data()

    fig = go.Figure(
        go.Sunburst(
            ids=ids,
            labels=labels,
            parents=parents,
            values=values,
            branchvalues="total",
            maxdepth=3,
            sort=False,
            marker=dict(colors=colors, line=dict(color="white", width=1.5)),
            customdata=list(zip(full_names, details)),
            hovertemplate=(
                "<b>%{customdata[0]}</b><br>%{label}<br>"
                "%{customdata[1]}<extra></extra>"
            ),
            textinfo="label",
            insidetextorientation="radial",
            textfont=dict(size=13, family=FONT, color="#1F2937"),
        )
    )

    colleges = []
    for m in MAJORS:
        if m[0] not in colleges:
            colleges.append(m[0])
    palette = college_palette(len(colleges))
    legend_items = [
        (SHORT_NAMES.get(c, c), sum(1 for m in MAJORS if m[0] == c), palette[i][0])
        for i, c in enumerate(colleges)
    ]

    def chips(items):
        return "<br>".join(
            f"<span style='color:{color}'>■</span> {name} {count} 个"
            for name, count, color in items
        )

    half = (len(legend_items) + 1) // 2
    college_count = len(colleges)

    fig.update_layout(
        title=dict(
            text=(
                "<b>嘉兴大学本科招生专业结构</b>"
                f"<br><sup>{college_count} 个学院 · {len(MAJORS)} 个本科招生专业"
                " · 每个学院一种颜色 · 数据来源：教务处《本科专业设置一览表》× 本科招生网（2026 年招生口径）</sup>"
            ),
            x=0.5,
            xanchor="center",
            font=dict(size=28, family=FONT, color="#1F2937"),
        ),
        font=dict(family=FONT, size=13, color="#374151"),
        paper_bgcolor="white",
        margin=dict(t=130, l=40, r=40, b=40),
        width=2000,
        height=1700,
        annotations=[
            dict(
                text=chips(legend_items[:half]),
                x=0.012, y=0.012, xref="paper", yref="paper",
                showarrow=False, align="left",
                font=dict(size=14, family=FONT),
                bgcolor="rgba(255,255,255,0.85)", borderpad=8,
            ),
            dict(
                text=chips(legend_items[half:]),
                x=0.988, y=0.012, xref="paper", yref="paper",
                showarrow=False, align="right",
                font=dict(size=14, family=FONT),
                bgcolor="rgba(255,255,255,0.85)", borderpad=8,
            ),
        ],
    )
    return fig


if __name__ == "__main__":
    out_dir = Path(__file__).resolve().parent
    fig = make_figure()
    png_path = out_dir / "嘉兴大学本科专业旭日图.png"
    pio.write_image(fig, png_path, format="png", width=2000, height=1700, scale=2)
    print(f"已生成：{png_path}")
