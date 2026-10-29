# -*- coding: utf-8 -*-
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
from matplotlib.patches import FancyBboxPatch

f_title  = FontProperties(family='Microsoft YaHei', size=20, weight='bold')
f_sub    = FontProperties(family='Microsoft YaHei', size=14, weight='normal')
f_dlabel = FontProperties(family='Calibri', size=10)
f_xlabel = FontProperties(family='Microsoft YaHei', size=9)
f_ylabel = FontProperties(family='Calibri', size=10)
f_note   = FontProperties(family='Microsoft YaHei', size=9)

products = ['口红', '面膜', '隔离', '防晒', '精华', '面霜']
actual   = [653, 523, 648, 856, 714, 785]
target   = [700, 500, 600, 900, 600, 600]

x = list(range(len(products)))

bg_color   = '#1A1F3A'
text_color = '#FFFFFF'
bar_color  = '#0070C0'
frame_color = '#8A90B0'

fig_w = 14.68 / 2.54
fig_h = 10.47 / 2.54
fig, ax = plt.subplots(figsize=(fig_w, fig_h), dpi=150)
fig.patch.set_facecolor(bg_color)
ax.set_facecolor(bg_color)

bar_width = 0.30
actual_width = 0.20

ax.bar(x, target, width=bar_width, facecolor='none',
       edgecolor=frame_color, linewidth=1.2, zorder=3)
ax.bar(x, actual, width=actual_width, color=bar_color, zorder=4)

for xi, v in zip(x, actual):
    ax.text(xi, v + 40, f'{v}', ha='center', va='bottom',
            fontproperties=f_dlabel, color=text_color, fontsize=10, zorder=5)

ax.set_xticks(x)
ax.set_xticklabels(products, fontproperties=f_xlabel, color=text_color)
ax.set_yticks([])
ax.set_ylim(0, 1050)
ax.set_xlim(-0.5, len(products) - 0.5)

ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_visible(False)
ax.spines['bottom'].set_visible(False)
ax.tick_params(axis='x', length=0, pad=6)
ax.tick_params(axis='y', length=0, pad=6)

fig.text(0.05, 0.94, '2022年上半年各商品销量完成情况', ha='left', va='top',
         fontproperties=f_title, color=text_color)
fig.text(0.05, 0.86, '防晒整体销量最好，达到856，面霜远超目标，超额完成30%', ha='left', va='top',
         fontproperties=f_sub, color=text_color)

y_box = 0.76
box_w = 0.02
box_h = 0.016
bx = 0.13

fig.patches.append(FancyBboxPatch((bx, y_box - box_h / 2), box_w, box_h,
                                  boxstyle='square,pad=0',
                                  facecolor='none', edgecolor=frame_color,
                                  linewidth=1.2,
                                  transform=fig.transFigure, zorder=5))
fig.text(bx + box_w + 0.008, y_box, '目标销量', ha='left', va='center',
         fontproperties=f_xlabel, color=text_color, fontsize=9, zorder=6)

bx2 = bx + box_w + 0.008 + 0.16
fig.patches.append(FancyBboxPatch((bx2, y_box - box_h / 2), box_w, box_h,
                                  boxstyle='square,pad=0',
                                  facecolor=bar_color, edgecolor='none',
                                  transform=fig.transFigure, zorder=5))
fig.text(bx2 + box_w + 0.008, y_box, '实际销量', ha='left', va='center',
         fontproperties=f_xlabel, color=text_color, fontsize=9, zorder=6)

fig.text(0.05, 0.04, '*注：数据来源于公司销售系统，统计日期截至2022.06.30',
         ha='left', va='bottom', fontproperties=f_note, fontsize=8, color=text_color)

plt.subplots_adjust(left=0.13, right=0.87, top=0.71, bottom=0.22)
plt.savefig('目标柱形图.png', facecolor=bg_color, dpi=150)
print('saved 目标柱形图.png')