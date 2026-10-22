# -*- coding: utf-8 -*-
"""南丁格尔玫瑰图：2021年各部门人数分布"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
from matplotlib.patches import Wedge
import numpy as np

plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei']
plt.rcParams['axes.unicode_minus'] = False

f_title  = FontProperties(family='Microsoft YaHei', size=18, weight='bold')
f_sub    = FontProperties(family='Microsoft YaHei', size=12, weight='normal')
f_note   = FontProperties(family='Microsoft YaHei', size=9)
f_label  = FontProperties(family='Microsoft YaHei', size=10, weight='bold')
f_pct    = FontProperties(family='Microsoft YaHei', size=9, weight='normal')

bg_color   = '#1A1F3A'
text_color = '#FFFFFF'

departments = ['销售部', '采购部', '工程部', '财务部', '行政部', '人力部']
percents = [29.2, 22.7, 17.5, 13.6, 10.3, 6.7]
colors = ['#D84C67', '#D8B241', '#1AB8A0', '#3E6BAA', '#5DBFE8', '#76409C']

total = 1664
people = [round(total * p / 100) for p in percents]
people[-1] = total - sum(people[:-1])

fig_w = 14.68 / 2.54
fig_h = 10.47 / 2.54
fig = plt.figure(figsize=(fig_w, fig_h), facecolor=bg_color)
ax = fig.add_axes([0.0, 0.06, 1.0, 0.86])
ax.set_facecolor(bg_color)
ax.set_aspect('equal')
ax.axis('off')

n = len(departments)
start = 90

r = 2.0

cx = 0.0
cy = -2.7

for i in range(n):
    angle = 360.0 * percents[i] / 100
    end = start - angle
    w = Wedge((cx, cy), r, end, start, facecolor=colors[i], edgecolor='none')
    ax.add_patch(w)

    mid_deg = (start + end) / 2
    mid_rad = np.radians(mid_deg)
    x1 = cx + r * np.cos(mid_rad)
    y1 = cy + r * np.sin(mid_rad)
    if i in (3, 4, 5):
        x2 = x1 - 0.6
        y2 = y1
        ax.plot([x1, x2], [y1, y2], color=colors[i], linewidth=0.75, zorder=5)
    else:
        x_mid = cx + (r + 0.3) * np.cos(mid_rad)
        y_mid = cy + (r + 0.3) * np.sin(mid_rad)
        if np.cos(mid_rad) >= 0:
            x2 = x_mid + 0.45
        else:
            x2 = x_mid - 0.45
        y2 = y_mid
        ax.plot([x1, x_mid, x2], [y1, y_mid, y2], color=colors[i], linewidth=0.75, zorder=5)

    if i == 0:
        ax.scatter([x1], [y1], s=10, color=colors[i], zorder=6)

    start = end

ax.set_xlim(-2.8, 2.8)
ax.set_ylim(-5.5, 0.1)

fig.text(0.062, 0.94, '2021年各部门人数分布', ha='left', va='top',
         fontproperties=f_title, color=text_color)
fig.text(0.062, 0.86,
         f'公司总人数{total}，销售部人数最多451，占比{percents[0]}%',
         ha='left', va='top', fontproperties=f_sub, color=text_color)
fig.text(0.062, 0.035,
         '*注：数据来源于公司人力资源系统，统计日期截至2022.01.01',
         ha='left', va='bottom', fontproperties=f_note, color=text_color)

plt.savefig('南丁格尔圆饼.png', facecolor=bg_color, dpi=150)
print('done')