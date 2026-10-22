# -*- coding: utf-8 -*-
"""跑道图：环形径向条形图（各部门人数）"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
from matplotlib.patches import Wedge, Circle, Rectangle
import numpy as np

plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei']
plt.rcParams['axes.unicode_minus'] = False

f_title  = FontProperties(family='Microsoft YaHei', size=20, weight='bold')
f_sub    = FontProperties(family='Microsoft YaHei', size=14, weight='normal')
f_note   = FontProperties(family='Microsoft YaHei', size=9)
f_legend = FontProperties(family='DengXian', size=7, weight='normal')

bg_color   = '#1A1F3A'
text_color = '#FFFFFF'

departments = ['人力部', '行政部', '财务部', '工程部', '采购部', '销售部']
people = [130, 226, 238, 293, 326, 451]
colors = ['#8B4CB8', '#4A7FC9', '#3BC9E8', '#4DE8B8', '#FFD24D', '#FF5A7A']

total = sum(people)
full_scale = 832
start = 90

fig_w = 14.68 / 2.54
fig_h = 10.47 / 2.54
fig = plt.figure(figsize=(fig_w, fig_h), facecolor=bg_color)
ax = fig.add_axes([0.0, 0.06, 1.0, 0.86])
ax.set_facecolor(bg_color)
ax.set_aspect('equal')
ax.axis('off')

n = len(departments)
ring_w = 0.16
gap = 0.05
r0 = 1.25
cx = -0.5
cy = -0.15

for i in range(n):
    r_inner = r0 + i * (ring_w + gap)
    r_outer = r_inner + ring_w
    r_mid = r_inner + ring_w / 2
    angle = 360.0 * people[i] / full_scale
    end = start - angle
    w = Wedge((cx, cy), r_outer, end, start, width=ring_w,
              facecolor=colors[i], edgecolor='none')
    ax.add_patch(w)


R = r0 + n * (ring_w + gap)
ax.set_xlim(-R - 0.9, R + 0.7)
ax.set_ylim(-R - 0.2, R + 0.8)

for i in range(n):
    r_mid_i = r0 + i * (ring_w + gap) + ring_w / 2
    ax.text(cx - R + 2.33, cy + r_mid_i, f'{departments[i]} {people[i]}',
            ha='right', va='center', fontproperties=f_legend, color=text_color)

fig.text(0.062, 0.94, '2022年上半年各部门人数', ha='left', va='top',
         fontproperties=f_title, color=text_color)
fig.text(0.062, 0.86,
         f'公司总人数{total}，销售部人数最多{people[-1]}，占比{people[-1]/total*100:.0f}%',
         ha='left', va='top', fontproperties=f_sub, color=text_color)
fig.text(0.062, 0.035,
         '*注：数据来源于公司人力资源系统，统计日期截至2022.06.30',
         ha='left', va='bottom', fontproperties=f_note, color=text_color)

plt.savefig('跑道.png', facecolor=bg_color, dpi=150)
print('done')
