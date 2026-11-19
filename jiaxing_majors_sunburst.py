# -*- coding: utf-8 -*-
"""嘉兴大学本科专业结构旭日图

数据来源：嘉兴大学教务处《嘉兴大学普通高等学校本科专业设置一览表》
https://jwc.zjxu.edu.cn/jgsz/zysz.htm （抓取日期 2026-11-19）
各专业已与 15 个学院官网“学院简介”逐院核对。
"""
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
    ("经济学院", "国际经济与贸易", "020401", "经济学", "经济与贸易类"),
    ("经济学院", "跨境电子商务", "120803T", "管理学", "电子商务类"),
    ("经济学院", "数字经济", "020109T", "经济学", "经济学类"),
    ("商学院", "会计学", "120203K", "管理学", "工商管理类"),
    ("商学院", "人力资源管理", "120206", "管理学", "工商管理类"),
    ("商学院", "财务管理", "120204", "管理学", "工商管理类"),
    ("商学院", "市场营销", "120202", "管理学", "工商管理类"),
    ("商学院", "信息管理与信息系统", "120102", "管理学", "管理科学与工程类"),
    ("商学院", "工商管理", "120201K", "管理学", "工商管理类"),
    ("商学院", "物流管理", "120601", "管理学", "物流管理与工程类"),
    ("马克思主义学院（中共党史党建学院）", "中国共产党历史", "030502", "法学", "马克思主义理论类"),
    ("信息科学与工程学院", "电子信息工程", "080701", "工学", "电子信息类"),
    ("信息科学与工程学院", "通信工程", "080703", "工学", "电子信息类"),
    ("信息科学与工程学院", "低空技术与工程", "083203TK", "工学", "交叉工程类"),
    ("机械工程学院（机器人工程学院）", "车辆工程", "080207", "工学", "机械类"),
    ("机械工程学院（机器人工程学院）", "智能制造工程", "080213T", "工学", "机械类"),
    ("机械工程学院（机器人工程学院）", "机械设计制造及其自动化", "080202", "工学", "机械类"),
    ("机械工程学院（机器人工程学院）", "电气工程及其自动化", "080601", "工学", "电气类"),
    ("机械工程学院（机器人工程学院）", "机器人工程", "080803T", "工学", "自动化类"),
    ("机械工程学院（机器人工程学院）", "材料成型及控制工程", "080203", "工学", "机械类"),
    ("人工智能学院", "计算机科学与技术", "080901", "工学", "计算机类"),
    ("人工智能学院", "网络工程", "080903", "工学", "计算机类"),
    ("人工智能学院", "软件工程", "080902", "工学", "计算机类"),
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
    ("设计学院", "服装与服饰设计", "130505", "艺术学", "设计学类"),
    ("设计学院", "数字媒体艺术", "130508", "艺术学", "设计学类"),
    ("生物与化学工程学院", "应用化学", "070302", "工学", "化学类"),
    ("生物与化学工程学院", "化学工程与工艺", "081301", "工学", "化工与制药类"),
    ("生物与化学工程学院", "制药工程", "081302", "工学", "化工与制药类"),
    ("生物与化学工程学院", "生物工程", "083001", "工学", "生物工程类"),
    ("生物与化学工程学院", "环境工程", "082502", "工学", "环境科学与工程类"),
    ("材料与纺织工程学院", "纺织工程", "081601", "工学", "纺织类"),
    ("材料与纺织工程学院", "高分子材料与工程", "080407", "工学", "材料类"),
    ("材料与纺织工程学院", "轻化工程", "081701", "工学", "轻工类"),
    ("材料与纺织工程学院", "非织造材料与工程", "081603T", "工学", "纺织类"),
    ("材料与纺织工程学院", "新能源材料与器件", "080414T", "工学", "材料类"),
    ("建筑工程学院", "工程管理", "120103", "工学", "管理科学与工程类"),
    ("建筑工程学院", "建筑环境与能源应用工程", "081002", "工学", "土木类"),
    ("建筑工程学院", "土木工程", "081001", "工学", "土木类"),
    ("建筑工程学院", "建筑学", "082801", "工学", "建筑类"),
    ("文法学院", "汉语言文学", "050101", "文学", "中国语言文学类"),
    ("文法学院", "汉语国际教育", "050103", "文学", "中国语言文学类"),
    ("文法学院", "法学", "030101K", "法学", "法学类"),
    ("文法学院", "知识产权", "030102T", "法学", "法学类"),
    ("外国语学院", "英语", "050201", "文学", "外国语言文学类"),
    ("外国语学院", "日语", "050207", "文学", "外国语言文学类"),
    ("教育学院", "学前教育", "040106", "教育学", "教育学类"),
    ("教育学院", "小学教育", "040107", "教育学", "教育学类"),
    ("教育学院", "体育教育", "040201", "教育学", "体育学类"),
]

DEGREE_COLORS = {
    "工学": "#4E79A7",
    "管理学": "#F28E2B",
    "经济学": "#59A14F",
    "医学": "#E15759",
    "理学": "#76B7B2",
    "文学": "#B07AA1",
    "法学": "#EDC948",
    "艺术学": "#FF9DA7",
    "教育学": "#9C755F",
}


def build_data():
    colleges = []
    for college, *_ in MAJORS:
        if college not in colleges:
            colleges.append(college)

    ids = [ROOT]
    labels = [ROOT]
    parents = [""]
    values = [len(MAJORS)]
    colors = ["#6B7280"]
    full_names = ["嘉兴大学"]
    details = [f"{len(colleges)} 个学院 · {len(MAJORS)} 个本科专业"]

    for college in colleges:
        major_rows = [m for m in MAJORS if m[0] == college]
        degree_count = {}
        for m in major_rows:
            degree_count[m[3]] = degree_count.get(m[3], 0) + 1
        main_degree = max(degree_count, key=degree_count.get)

        ids.append(college)
        labels.append(SHORT_NAMES.get(college, college))
        parents.append(ROOT)
        values.append(len(major_rows))
        colors.append(DEGREE_COLORS[main_degree])
        full_names.append(college)
        detail = "，".join(f"{d}学位{c}个" for d, c in degree_count.items())
        details.append(f"共 {len(major_rows)} 个本科专业（{detail}）")

        for _, major, code, degree, major_class in major_rows:
            ids.append(f"{college}/{major}")
            labels.append(major)
            parents.append(college)
            values.append(1)
            colors.append(DEGREE_COLORS[degree])
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
            textfont=dict(size=13, family=FONT, color="white"),
        )
    )

    counts = {}
    for m in MAJORS:
        counts[m[3]] = counts.get(m[3], 0) + 1
    legend_items = sorted(counts.items(), key=lambda kv: -kv[1])

    def chips(items):
        return "<br>".join(
            f"<span style='color:{DEGREE_COLORS[d]}'>■</span> {d} {c} 个"
            for d, c in items
        )

    half = (len(legend_items) + 1) // 2
    college_count = len({m[0] for m in MAJORS})

    fig.update_layout(
        title=dict(
            text=(
                "<b>嘉兴大学本科专业结构</b>"
                f"<br><sup>{college_count} 个学院 · {len(MAJORS)} 个本科专业"
                " · 按授予学位门类着色 · 数据来源：嘉兴大学教务处《本科专业设置一览表》</sup>"
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