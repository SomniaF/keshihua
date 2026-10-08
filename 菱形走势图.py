# -*- coding: utf-8 -*-
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties

f_title  = FontProperties(family='Microsoft YaHei', size=20, weight='bold')
f_sub    = FontProperties(family='Microsoft YaHei', size=12, weight='normal')
f_dlabel = FontProperties(family='Calibri', size=10, weight='normal')
f_xlabel = FontProperties(family='Microsoft YaHei', size=10)
f_ylabel = FontProperties(family='Calibri', size=10)
f_note   = FontProperties(family='Microsoft YaHei', size=9)

months = ['1月', '2月', '3月', '4月', '5月', '6月', '7月', '8月']
rates  = [53.60, 49.80, 52.70, 70.80, 60.90, 49.60, 58.60, 70.40]

x = list(range(len(months)))
y = rates

bg_color   = '#1A1F3A'
text_color = '#FFFFFF'
line_color = '#E0392B'

fig_w = 14.68 / 2.54
fig_h = 10.47 / 2.54
fig, ax = plt.subplots(figsize=(fig_w, fig_h), dpi=150)
fig.patch.set_facecolor(bg_color)
ax.set_facecolor(bg_color)

ax.set_xticks(x)
ax.set_xticklabels([])
ax.set_yticks([])
ax.set_ylim(0, 84)
ax.set_xlim(-0.6, len(months) - 0.4)

import math
diamond_s = 48
half_h_pt = math.sqrt(diamond_s) / 2.0
half_h_px = half_h_pt * fig.dpi / 72.0
p0 = ax.transData.transform((0, 0))
p1 = ax.transData.transform((0, 1))
delta = half_h_px / abs(p1[1] - p0[1])

for xi, yi in zip(x, y):
    ax.plot([xi, xi], [0, yi - delta], color=line_color, linewidth=0.75, zorder=2)
    ax.scatter(xi, yi, marker='D', s=diamond_s, facecolors='none',
               edgecolors=line_color, linewidths=0.75, zorder=4)
    ax.text(xi, yi + 3.0, f'{yi:.2f}%', ha='center', va='bottom',
            fontproperties=f_dlabel, color=text_color, fontsize=10, zorder=5)

for xi, m in zip(x, months):
    ax.text(xi, -0.04, m, transform=ax.get_xaxis_transform(),
            ha='center', va='top', fontproperties=f_xlabel,
            color=text_color, fontsize=11)

ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_visible(False)
ax.spines['bottom'].set_position('zero')
ax.spines['bottom'].set_color('#A8AEC8')
ax.spines['bottom'].set_linewidth(0.8)
ax.tick_params(axis='x', length=0, pad=8)
ax.tick_params(axis='y', length=0, pad=6)


fig.text(0.05, 0.94, '2022年1-8月公司计划完成率', ha='left', va='top',
         fontproperties=f_title, color=text_color)
fig.text(0.05, 0.86, '公司整体完成率55%，4月和8月超过70%，2月和6月较低未过半',
         ha='left', va='top', fontproperties=f_sub, color=text_color)

fig.text(0.05, 0.04, '*注：数据来源于公司销售系统，统计日期截至2022.08.31',
         ha='left', va='bottom', fontproperties=f_note, fontsize=8, color=text_color)

plt.subplots_adjust(left=0.13, right=0.97, top=0.78, bottom=0.22)
plt.savefig('菱形走势图.png', facecolor=bg_color, dpi=150)
print('saved 菱形走势图.png')