# -*- coding: utf-8 -*-
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
from matplotlib.patches import Rectangle

f_title  = FontProperties(family='Microsoft YaHei', size=18, weight='bold')
f_sub    = FontProperties(family='Microsoft YaHei', size=11, weight='normal')
f_dlabel = FontProperties(family='Calibri', size=10)
f_xlabel = FontProperties(family='Microsoft YaHei', size=9)
f_ylabel = FontProperties(family='Calibri', size=10)
f_note   = FontProperties(family='Microsoft YaHei', size=9)
f_plabel = FontProperties(family='Calibri', size=9, weight='bold')
f_legend = FontProperties(family='Microsoft YaHei', size=10)

regions  = ['华北', '华南', '东北', '西北', '西南', '华东']
sales22  = [2354, 1902, 3524, 2698, 2896, 2563]
sales21  = [2021, 1563, 3213, 2531, 2631, 2361]
yoy      = [16, 22, 10, 7, 10, 9]

x = list(range(len(regions)))

bg_color    = '#1A1F3A'
text_color  = '#FFFFFF'
bar22_color = '#0070C0'
bar21_color = '#D9534F'
line_color  = '#F0C419'

fig_w = 14.68 / 2.54
fig_h = 10.47 / 2.54
fig, ax = plt.subplots(figsize=(fig_w, fig_h), dpi=150)
fig.patch.set_facecolor(bg_color)
ax.set_facecolor(bg_color)

ax2 = ax.twinx()
ax2.set_facecolor(bg_color)

bar_width = 0.20
offset = bar_width * 0.65
bars22 = ax.bar([xi - offset for xi in x], sales22, width=bar_width,
                color=bar22_color, zorder=3, label='2022')
bars21 = ax.bar([xi + offset for xi in x], sales21, width=bar_width,
                color=bar21_color, zorder=3, label='2021')

for xi, v in zip(x, sales22):
    ax.text(xi - offset, v + 120, f'{v}', ha='center', va='bottom',
            fontproperties=f_dlabel, color=text_color, fontsize=10, zorder=8)
for xi, v in zip(x, sales21):
    ax.text(xi + offset, v + 120, f'{v}', ha='center', va='bottom',
            fontproperties=f_dlabel, color=text_color, fontsize=10, zorder=8)

line = ax2.plot(x, yoy, color=line_color, marker='o', markersize=7,
                markerfacecolor=line_color, markeredgecolor=line_color,
                markeredgewidth=0, linewidth=2, zorder=5, label='同比去年')
for xi, v in zip(x, yoy):
    ax2.text(xi, v + 2.2, f'{v}%', ha='center', va='bottom',
             fontproperties=f_plabel, color=text_color, fontsize=10, zorder=6)

ax.set_xticks(x)
ax.set_xticklabels(regions, fontproperties=f_xlabel, color=text_color)
ax.set_yticks([])
ax.set_ylim(0, 5600)
ax.set_xlim(-0.5, len(regions) - 0.5)

ax2.set_yticks([])
ax2.set_ylim(-100, 45)

for spine in ['top', 'right', 'left']:
    ax.spines[spine].set_visible(False)
ax.spines['bottom'].set_visible(True)
ax.spines['bottom'].set_color('#888888')
ax.spines['bottom'].set_linewidth(0.8)
ax2.spines['top'].set_visible(False)
ax2.spines['right'].set_visible(False)
ax2.spines['left'].set_visible(False)
ax2.spines['bottom'].set_visible(False)
ax.tick_params(axis='x', length=0, pad=6)
ax.tick_params(axis='y', length=0, pad=6)
ax2.tick_params(axis='y', length=0, pad=6)

label_color = '#C8CDD8'
f_box = FontProperties(family='Microsoft YaHei', size=8)
hd_idx = 5
box_x_left = hd_idx - offset - bar_width / 2 + 0.10
box_width = 0.45
box_height = 350
blue_box_y = 1073
red_box_y  = 623
ax.add_patch(Rectangle((box_x_left, blue_box_y), box_width, box_height,
                       facecolor=bg_color, edgecolor=bar22_color,
                       linewidth=1.5, zorder=10))
ax.text(box_x_left + box_width / 2, blue_box_y + box_height / 2, '2022',
        ha='center', va='center', fontproperties=f_box,
        color=label_color, zorder=11)
ax.add_patch(Rectangle((box_x_left, red_box_y), box_width, box_height,
                       facecolor=bg_color, edgecolor=bar21_color,
                       linewidth=1.5, zorder=10))
ax.text(box_x_left + box_width / 2, red_box_y + box_height / 2, '2021',
        ha='center', va='center', fontproperties=f_box,
        color=label_color, zorder=11)

fig.text(0.05, 0.94, '上半年各月商品销量同比去年情况', ha='left', va='top',
         fontproperties=f_title, color=text_color)
fig.text(0.05, 0.86, '2022年相比于2021年销量都有提升，半年整体提升17%', ha='left', va='top',
         fontproperties=f_sub, color=text_color)

fig.text(0.05, 0.04, '*注：数据来源于公司销售系统，统计日期截至2022.06.30',
         ha='left', va='bottom', fontproperties=f_note, fontsize=8, color=text_color)

plt.subplots_adjust(left=0.10, right=0.92, top=0.83, bottom=0.22)
plt.savefig('簇状柱形折线图.png', facecolor=bg_color, dpi=150)
print('saved 簇状柱形折线图.png')