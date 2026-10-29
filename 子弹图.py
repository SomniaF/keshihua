# -*- coding: utf-8 -*-
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
from matplotlib.patches import FancyBboxPatch
from matplotlib.lines import Line2D

f_title  = FontProperties(family='Microsoft YaHei', size=18, weight='bold')
f_sub    = FontProperties(family='Microsoft YaHei', size=11, weight='normal')
f_dlabel = FontProperties(family='Calibri', size=10)
f_xlabel = FontProperties(family='Microsoft YaHei', size=9)
f_ylabel = FontProperties(family='Calibri', size=10)
f_note   = FontProperties(family='Microsoft YaHei', size=9)

products  = ['口红', '面膜', '隔离', '防晒', '精华', '面霜']
actual    = [653, 523, 648, 856, 714, 785]
target    = [700, 500, 600, 900, 600, 600]
pass_v    = [600, 600, 600, 600, 600, 600]
good_v    = [200, 200, 200, 200, 200, 200]
excel_v   = [200, 200, 200, 200, 200, 200]

x = list(range(len(products)))

bg_color    = '#1a1a3e'
text_color  = '#ffffff'
sub_color   = '#b8c5d6'
axis_color  = '#4a5568'
pass_color  = '#8fa8c8'
good_color  = '#2a9d8f'
excel_color = '#1e88e5'
actual_color= '#2962ff'
target_color= '#ffc107'

fig_w = 14.68 / 2.54
fig_h = 10.47 / 2.54
fig, ax = plt.subplots(figsize=(fig_w, fig_h), dpi=150)
fig.patch.set_facecolor(bg_color)
ax.set_facecolor(bg_color)

bar_w = 0.34
actual_w = 0.16

ax.bar(x, pass_v, width=bar_w, color=pass_color, zorder=3)
ax.bar(x, good_v, width=bar_w, bottom=pass_v, color=good_color, zorder=3)
ax.bar(x, excel_v, width=bar_w, bottom=[a + b for a, b in zip(pass_v, good_v)],
       color=excel_color, zorder=3)

ax.bar(x, actual, width=actual_w, color=actual_color, zorder=4)

for xi, v in zip(x, target):
    ax.plot([xi - actual_w / 2, xi + actual_w / 2], [v, v],
            color=target_color, linewidth=2.2, zorder=5)

ax.set_xticks(x)
ax.set_xticklabels(products, fontproperties=f_xlabel, color=text_color)
ax.set_yticks([0, 200, 400, 600, 800, 1000, 1200])
ax.tick_params(axis='y', colors=axis_color, labelsize=8, length=0, pad=4)
for label in ax.get_yticklabels():
    label.set_fontproperties(f_ylabel)
    label.set_color(text_color)
ax.set_ylim(0, 1200)
ax.set_xlim(-0.5, len(products) - 0.5)

ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_visible(False)
ax.spines['bottom'].set_color(axis_color)
ax.spines['bottom'].set_linewidth(0.6)
ax.tick_params(axis='x', length=0, pad=6)

fig.text(0.05, 0.94, '2022年上半年各商品销量完成情况', ha='left', va='top',
         fontproperties=f_title, color=text_color)
fig.text(0.05, 0.86, '防晒整体销量最好，达到856，面霜远超目标，超额完成30%', ha='left', va='top',
         fontproperties=f_sub, color=text_color)

y_box = 0.72
box_w = 0.02
box_h = 0.016
bx = 0.14

fig.patches.append(FancyBboxPatch((bx, y_box - box_h / 2), box_w, box_h,
                                  boxstyle='square,pad=0',
                                  facecolor=pass_color, edgecolor='none',
                                  transform=fig.transFigure, zorder=5))
fig.text(bx + box_w + 0.006, y_box, '及格', ha='left', va='center',
         fontproperties=f_xlabel, color=text_color, fontsize=9, zorder=6)

bx2 = bx + box_w + 0.006 + 0.07
fig.patches.append(FancyBboxPatch((bx2, y_box - box_h / 2), box_w, box_h,
                                  boxstyle='square,pad=0',
                                  facecolor=good_color, edgecolor='none',
                                  transform=fig.transFigure, zorder=5))
fig.text(bx2 + box_w + 0.006, y_box, '良好', ha='left', va='center',
         fontproperties=f_xlabel, color=text_color, fontsize=9, zorder=6)

bx3 = bx2 + box_w + 0.006 + 0.07
fig.patches.append(FancyBboxPatch((bx3, y_box - box_h / 2), box_w, box_h,
                                  boxstyle='square,pad=0',
                                  facecolor=excel_color, edgecolor='none',
                                  transform=fig.transFigure, zorder=5))
fig.text(bx3 + box_w + 0.006, y_box, '优秀', ha='left', va='center',
         fontproperties=f_xlabel, color=text_color, fontsize=9, zorder=6)

bx4 = bx3 + box_w + 0.006 + 0.07
fig.patches.append(FancyBboxPatch((bx4, y_box - box_h / 2), box_w, box_h,
                                  boxstyle='square,pad=0',
                                  facecolor=actual_color, edgecolor='none',
                                  transform=fig.transFigure, zorder=5))
fig.text(bx4 + box_w + 0.006, y_box, '实际', ha='left', va='center',
         fontproperties=f_xlabel, color=text_color, fontsize=9, zorder=6)

lx = bx4 + box_w + 0.006 + 0.07
line_len = 0.03
line = Line2D([lx, lx + line_len], [y_box, y_box], color=target_color,
              linewidth=2.0, transform=fig.transFigure, zorder=5)
fig.add_artist(line)
fig.text(lx + line_len + 0.006, y_box, '目标', ha='left', va='center',
         fontproperties=f_xlabel, color=text_color, fontsize=9, zorder=6)

fig.text(0.05, 0.04, '*注：数据来源于公司销售系统，统计日期截至2022.06.30',
         ha='left', va='bottom', fontproperties=f_note, fontsize=8, color=text_color)

plt.subplots_adjust(left=0.10, right=0.95, top=0.71, bottom=0.18)
plt.savefig('子弹图.png', facecolor=bg_color, dpi=150)
print('saved 子弹图.png')