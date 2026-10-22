# -*- coding: utf-8 -*-
"""玉玦图：多层带缺口环形图（年龄分布）"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
from matplotlib.patches import Wedge
import numpy as np

plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei']
plt.rcParams['axes.unicode_minus'] = False

f_title  = FontProperties(family='Microsoft YaHei', size=20, weight='bold')
f_sub    = FontProperties(family='Microsoft YaHei', size=14, weight='normal')
f_dlabel = FontProperties(family='Calibri', size=10)
f_legend = FontProperties(family='Microsoft YaHei', size=10)
f_note   = FontProperties(family='Microsoft YaHei', size=9)

bg_color   = '#1A1F3A'
text_color = '#FFFFFF'

labels  = ['[20,30)', '[30,40)', '[40,50)', '>=50']
percents = [37.5, 29.2, 20.8, 12.5]
arc_pcts = [75, 58, 42, 25]
auxs     = [12.5, 20.8, 29.2, 37.5]
colors   = ['#EC5C4D', '#F7AC3A', '#4E8C7A', '#1A78C8']

fig_w = 14.68 / 2.54
fig_h = 10.47 / 2.54
fig = plt.figure(figsize=(fig_w, fig_h), facecolor=bg_color)
ax = fig.add_axes([0.12, 0.10, 0.76, 0.78])
ax.set_facecolor(bg_color)
ax.set_aspect('equal')
ax.axis('off')

cx, cy = 0, -0.1
R_out = 1.0
ring_w = 0.16
gap = 0.01

for i in range(len(labels)):
    r = R_out - i * (ring_w + gap)
    fill_span = arc_pcts[i] / 100.0 * 360.0
    start = 90.0

    w_fill = Wedge((cx, cy), r, start - fill_span, start, width=ring_w,
                   facecolor=colors[i], edgecolor=bg_color, linewidth=1.2, zorder=4)
    ax.add_patch(w_fill)

    end_theta = np.radians(start - fill_span)
    lx = cx + (r - ring_w / 2) * np.cos(end_theta)
    ly = cy + (r - ring_w / 2) * np.sin(end_theta)
    ax.text(lx, ly, f'{percents[i]}%', ha='center', va='center',
            fontproperties=f_dlabel, color=text_color, zorder=5)

    ax.text(cx - 0.25, cy + r - 0.08, labels[i], ha='center', va='center',
            fontproperties=f_legend, color=text_color, zorder=6)

ax.set_xlim(-1.25, 1.25)
ax.set_ylim(-1.25, 1.25)


fig.text(0.062, 0.94, '2022年上半年龄分布', ha='left', va='top',
         fontproperties=f_title, color=text_color)
fig.text(0.062, 0.86, '公司平均年龄32.5，23-30员工比例最高', ha='left', va='top',
         fontproperties=f_sub, color=text_color)
fig.text(0.062, 0.035, '*注：数据来源于公司人力资源系统，统计日期截至2022.06.30',
         ha='left', va='bottom', fontproperties=f_note, color=text_color)

plt.savefig('玉玦.png', facecolor=bg_color, dpi=150)
print('done')