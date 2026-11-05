# -*- coding: utf-8 -*-
"""南丁格尔圆环图：2022年上半各年龄段人数分布"""
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

ages     = ['[20,30)', '[30,40)', '[40,50)', '>=50']
percents = [37.5, 29.2, 20.8, 12.5]
total_pct = sum(percents)
colors   = ['#76409C', '#3E6BAA', '#1AB8A0', '#D8B241']

fig_w = 14.68 / 2.54
fig_h = 10.47 / 2.54
fig = plt.figure(figsize=(fig_w, fig_h), facecolor=bg_color)
ax = fig.add_axes([0.0, 0.06, 1.0, 0.86])
ax.set_facecolor(bg_color)
ax.set_aspect('equal')
ax.axis('off')

cx = 0.0
cy = 0.0
w     = 0.38
R_in  = 3.0

n = len(ages)

# 各颜色层数：紫5、蓝4、绿3、黄2，统一内径由内向外画
rings_count = [5, 4, 3, 2]

# 各颜色按累计占比从90°顺时针占据不同角度区域
start_angles = {}
acc = 90
for i in range(n):
    start_angles[i] = acc
    acc -= 360.0 * percents[i] / total_pct

for i in range(n):
    start = start_angles[i]
    angle = 360.0 * percents[i] / total_pct
    end   = start - angle

    for k in range(rings_count[i]):
        r_layer_out = R_in + (k + 1) * w
        wedge = Wedge((cx, cy), r_layer_out, end, start,
                      width=w, facecolor=colors[i], edgecolor='none')
        ax.add_patch(wedge)

    r_label = R_in + rings_count[i] * w
    mid_deg = (start + end) / 2
    mid_rad = np.radians(mid_deg)
    x1 = cx + r_label * np.cos(mid_rad)
    y1 = cy + r_label * np.sin(mid_rad)

    x2 = cx + (r_label + 0.5) * np.cos(mid_rad)
    y2 = cy + (r_label + 0.5) * np.sin(mid_rad)
    if np.cos(mid_rad) >= 0:
        x3 = x2 + 3.2
    else:
        x3 = x2 - 3.2
    ax.plot([x1, x2, x3], [y1, y2, y2],
            color=colors[i], linewidth=0.75, zorder=5)
    ax.scatter([x1], [y1], s=10, color=colors[i], zorder=6)

    ha = 'left' if np.cos(mid_rad) >= 0 else 'right'
    dx = 0.05 if ha == 'left' else -0.05
    ax.text(x3 + dx, y2 + 0.80, ages[i],
            ha=ha, va='bottom', fontproperties=f_label,
            color=text_color, zorder=7)
    pct_color = text_color if i == 3 else colors[i]
    ax.text(x3 + dx, y2 + 0.12, f'{percents[i]}%',
            ha=ha, va='bottom', fontproperties=f_label,
            color=pct_color, zorder=7)

ax.set_xlim(-9.2, 9.2)
ax.set_ylim(-9.2, 9.2)

fig.text(0.062, 0.94, '2022年上半各年龄段人数分布', ha='left', va='top',
         fontproperties=f_title, color=text_color)
fig.text(0.062, 0.86,
         '公司平均年龄32.5，20-30员工比例最高占比37.5%',
         ha='left', va='top', fontproperties=f_sub, color=text_color)
fig.text(0.062, 0.035,
         '*注：数据来源于公司人力资源系统，统计日期截至2022.06.30',
         ha='left', va='bottom', fontproperties=f_note, color=text_color)

plt.savefig('南丁格尔圆环.png', facecolor=bg_color, dpi=150)
print('done')