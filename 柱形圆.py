# -*- coding: utf-8 -*-
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
from matplotlib.patches import FancyBboxPatch, Circle
from matplotlib.lines import Line2D

f_title  = FontProperties(family='Microsoft YaHei', size=18, weight='bold')
f_sub    = FontProperties(family='Microsoft YaHei', size=11, weight='normal')
f_dlabel = FontProperties(family='Calibri', size=10)
f_xlabel = FontProperties(family='Microsoft YaHei', size=9)
f_ylabel = FontProperties(family='Calibri', size=10)
f_note   = FontProperties(family='Microsoft YaHei', size=9)
f_plabel = FontProperties(family='Calibri', size=9, weight='bold')

regions = ['华北', '华南', '东北', '西北', '西南', '华东']
sales   = [2354, 1902, 3524, 2698, 2896, 2563]
yoy     = [12, 25, 16, 21, 18, 25]

x = list(range(len(regions)))

bg_color   = '#1A1F3A'
text_color = '#FFFFFF'
bar_color  = '#E8505B'
dot_color  = '#1E5BB8'

fig_w = 14.68 / 2.54
fig_h = 10.47 / 2.54
fig, ax = plt.subplots(figsize=(fig_w, fig_h), dpi=150)
fig.patch.set_facecolor(bg_color)
ax.set_facecolor(bg_color)

bar_width = 0.34
bars = ax.bar(x, sales, width=bar_width, color=bar_color, zorder=3)

for xi, v in zip(x, sales):
    ax.text(xi, v + 120, f'{v:,}', ha='center', va='bottom',
            fontproperties=f_dlabel, color=text_color, fontsize=10, zorder=5)

dot_y = 4900
for xi, v in zip(x, yoy):
    ms = v * 1.2
    ax.plot(xi, dot_y, 'o', markersize=ms, markerfacecolor=dot_color,
            markeredgecolor='none', zorder=5)
    ax.text(xi, dot_y, f'{v}%', ha='center', va='center',
            family='Microsoft YaHei', fontsize=9,
            color='#FFFFFF', zorder=6)

ax.set_xticks(x)
ax.set_xticklabels(regions, fontproperties=f_xlabel, color=text_color)
ax.set_yticks([])
ax.set_ylim(0, 5800)
ax.set_xlim(-0.5, len(regions) - 0.5)

ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_visible(False)
ax.spines['bottom'].set_visible(True)
ax.spines['bottom'].set_color('#4A5170')
ax.spines['bottom'].set_linewidth(0.8)
ax.tick_params(axis='x', length=0, pad=6)
ax.tick_params(axis='y', length=0, pad=6)

fig.text(0.05, 0.94, '各区域上半年销量以同比', ha='left', va='top',
         fontproperties=f_title, color=text_color)
fig.text(0.05, 0.86, '东北区域销量持续保持第一，华东和华南同比去年增长最多', ha='left', va='top',
         fontproperties=f_sub, color=text_color)

fig.text(0.05, 0.04, '*注：数据来源于公司销售系统，统计日期截至2022.06.30',
         ha='left', va='bottom', fontproperties=f_note, fontsize=8, color=text_color)

plt.subplots_adjust(left=0.13, right=0.87, top=0.83, bottom=0.22)
plt.savefig('柱形圆.png', facecolor=bg_color, dpi=150)
print('saved 柱形圆.png')