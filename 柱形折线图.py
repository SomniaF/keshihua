# -*- coding: utf-8 -*-
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
from matplotlib.patches import FancyBboxPatch, Circle
from matplotlib.lines import Line2D

f_title  = FontProperties(family='Microsoft YaHei', size=20, weight='bold')
f_sub    = FontProperties(family='Microsoft YaHei', size=14, weight='normal')
f_dlabel = FontProperties(family='Calibri', size=10)
f_xlabel = FontProperties(family='Microsoft YaHei', size=9)
f_ylabel = FontProperties(family='Calibri', size=10)
f_note   = FontProperties(family='Microsoft YaHei', size=9)

years = ['2017', '2018', '2019', '2020', '2021', '2022']
sales = [1603, 2106, 2406, 3265, 3721, 3921]
yoy   = [27, 31, 14, 36, 14, 5]

x = list(range(len(years)))

bg_color   = '#1A1F3A'
text_color = '#FFFFFF'
bar_color  = '#1f77b4'
line_color = '#e87a5d'

fig_w = 14.68 / 2.54
fig_h = 10.47 / 2.54
fig, ax = plt.subplots(figsize=(fig_w, fig_h), dpi=150)
fig.patch.set_facecolor(bg_color)
ax.set_facecolor(bg_color)

bar_width = 0.42
bars = ax.bar(x, sales, width=bar_width, color=bar_color, zorder=3)

ax2 = ax.twinx()
ax2.set_facecolor(bg_color)
ax2.plot(x, yoy, color=line_color, linewidth=1.6, marker='o', markersize=5,
         markerfacecolor=line_color, markeredgecolor=line_color, zorder=4)

for xi, v in zip(x, sales):
    ax.text(xi, v + 120, f'{v:,}', ha='center', va='bottom',
            fontproperties=f_dlabel, color=text_color, fontsize=10, zorder=5)

for xi, v in zip(x, yoy):
    ax2.text(xi, v + 2.2, f'{v}%', ha='center', va='bottom',
             fontproperties=f_dlabel, color=line_color, fontsize=10, zorder=5)

ax.set_xticks(x)
ax.set_xticklabels(years, fontproperties=f_xlabel, color=text_color)
ax.set_yticks([])
ax.set_ylim(0, 6500)
ax.set_xlim(-0.5, len(years) - 0.5)

ax2.set_yticks([])
ax2.set_ylim(-135, 50)

ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_visible(False)
ax.spines['bottom'].set_visible(False)
ax2.spines['top'].set_visible(False)
ax2.spines['right'].set_visible(False)
ax2.spines['left'].set_visible(False)
ax2.spines['bottom'].set_visible(False)
ax.tick_params(axis='x', length=0, pad=6)
ax.tick_params(axis='y', length=0, pad=6)
ax2.tick_params(axis='y', length=0, pad=6)

fig.text(0.05, 0.94, '近六年销售量及增长率', ha='left', va='top',
         fontproperties=f_title, color=text_color)
fig.text(0.05, 0.86, '平台销量近6年持续增长，但近两年增长率有所放缓', ha='left', va='top',
         fontproperties=f_sub, color=text_color)

y_box = 0.76

box_w = 0.02
box_h = 0.016
bx = 0.70
fig.patches.append(FancyBboxPatch((bx, y_box - box_h / 2), box_w, box_h,
                                  boxstyle='square,pad=0',
                                  facecolor=bar_color, edgecolor='none',
                                  transform=fig.transFigure, zorder=5))
fig.text(bx + box_w + 0.008, y_box, '销售量', ha='left', va='center',
         fontproperties=f_xlabel, color=text_color, fontsize=9, zorder=6)

lx = bx + box_w + 0.008 + 0.06 + 0.03
line_len = 0.026
line = Line2D([lx, lx + line_len], [y_box, y_box], color=line_color,
              linewidth=1.6, transform=fig.transFigure, zorder=5)
fig.add_artist(line)
dot = Circle((lx + line_len / 2, y_box), 0.004, facecolor=line_color,
             edgecolor='none', transform=fig.transFigure, zorder=6)
fig.patches.append(dot)
fig.text(lx + line_len + 0.008, y_box, '同比', ha='left', va='center',
         fontproperties=f_xlabel, color=text_color, fontsize=9, zorder=6)

fig.text(0.05, 0.04, '*注：数据来源于公司销售系统',
         ha='left', va='bottom', fontproperties=f_note, fontsize=8, color=text_color)

plt.subplots_adjust(left=0.13, right=0.87, top=0.71, bottom=0.22)
plt.savefig('柱形折线图.png', facecolor=bg_color, dpi=150)
print('saved 柱形折线图.png')