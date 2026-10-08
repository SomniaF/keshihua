# -*- coding: utf-8 -*-
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.patches import FancyBboxPatch
import matplotlib.font_manager as fm
from datetime import datetime
import numpy as np

plt.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'SimHei', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

tasks = [
    ("制定计划", "2022/3/1",  "2022/3/12", 51),
    ("方案设计", "2022/3/13", "2022/3/21", 32),
    ("资源调配", "2022/3/22", "2022/4/1",  21),
    ("第一阶段", "2022/4/2",  "2022/4/15", 85),
    ("第二阶段", "2022/4/16", "2022/5/10", 36),
    ("第三阶段", "2022/5/11", "2022/5/25", 68),
    ("项目总结", "2022/5/26", "2022/6/2",  68),
]

BG_COLOR     = "#1A1F3A"
BAR_COLOR    = "#3498DB"
BAR_LIGHT    = "#1758A8"
GRID_COLOR   = "#a8b0d8"
TEXT_COLOR   = "#ffffff"
TITLE_COLOR  = "#ffffff"
AXIS_COLOR   = "#e8eaf6"
VALUE_COLOR  = "#C8CCE0"

fig_w = 14.68 / 2.54
fig_h = 10.47 / 2.54
fig, ax = plt.subplots(figsize=(fig_w, fig_h), dpi=150, facecolor=BG_COLOR)
ax.set_facecolor(BG_COLOR)

n = len(tasks)
bar_height = 0.55
y_positions = list(range(n))[::-1]

tick_labels = ["2022/3/1", "2022/3/16", "2022/3/31", "2022/4/15",
               "2022/4/30", "2022/5/15", "2022/5/30", "2022/6/14"]
axis_start = datetime.strptime("2022/3/1", "%Y/%m/%d")
span_days = 15

def date_pos(d):
    return (d - axis_start).days / span_days

for i, (name, start, end, pct) in enumerate(tasks):
    s = datetime.strptime(start, "%Y/%m/%d")
    e = datetime.strptime(end,   "%Y/%m/%d")
    y = y_positions[i]
    left = date_pos(s)
    width = date_pos(e) - left

    ax.barh(y, width, left=left, height=bar_height,
            color=BAR_LIGHT, edgecolor="none", zorder=3)

    done_width = width * pct / 100.0
    ax.barh(y, done_width, left=left, height=bar_height,
            color=BAR_COLOR, edgecolor="none", zorder=4)

    ax.text(left + width/2, y, f"{pct}%",
            ha="center", va="center", color=VALUE_COLOR,
            fontsize=9, fontweight="bold", zorder=5)

    ax.text(-0.3, y, name, ha="right", va="center",
            color=TEXT_COLOR, fontsize=9, zorder=5)

ax.set_yticks([])
ax.set_ylim(-0.8, n - 0.2)

ax.set_xlim(-1.35, 7.05)
ax.set_xticks(range(len(tick_labels)))
ax.set_xticklabels(tick_labels)
ax.xaxis.tick_top()
ax.tick_params(axis="x", colors=AXIS_COLOR, labelsize=8)
for label in ax.get_xticklabels():
    label.set_rotation(0)

ax.grid(axis="x", color=GRID_COLOR, linestyle="--", linewidth=0.8, alpha=0.7, zorder=1)
ax.set_axisbelow(True)

for spine in ax.spines.values():
    spine.set_visible(False)

ax.set_title("2022年化妆品类目采购项目进度", color=TITLE_COLOR,
             fontsize=18, fontweight="bold", pad=20)

plt.tight_layout()
plt.savefig("甘特图样例.png", dpi=150, facecolor=BG_COLOR, bbox_inches="tight")
plt.show()
print("已生成: 甘特图样例.png")