# -*- coding: utf-8 -*-
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
from matplotlib.lines import Line2D
from matplotlib.patches import Patch, Rectangle
import numpy as np

# 字体定义
f_title  = FontProperties(family='Microsoft YaHei', size=20, weight='bold')
f_sub    = FontProperties(family='Microsoft YaHei', size=12, weight='normal')
f_xlabel = FontProperties(family='Microsoft YaHei', size=10)
f_ylabel = FontProperties(family='Calibri', size=10)
f_note   = FontProperties(family='Microsoft YaHei', size=9)
f_legend = FontProperties(family='Microsoft YaHei', size=10)

# 数据
quarters = ['2021Q1', 'Q2', 'Q3', 'Q4', '2022Q1', 'Q2']
sales    = [3121, 4086, 4361, 4601, 4936, 4231]
profit   = [1020, 1421, 1502, 1623, 1781, 1432]

# 尺寸 14.68cm x 10.47cm
fig_w = 14.68 / 2.54
fig_h = 10.47 / 2.54
fig, ax = plt.subplots(figsize=(fig_w, fig_h), dpi=150)

# 颜色
bg_color    = '#1A1F3A'
text_color  = '#FFFFFF'
grid_color  = '#6A71A8'
color_sales  = '#0070C0'   # 销售额 标准蓝
color_profit = '#E74C3C'   # 利润额 红色

fig.patch.set_facecolor(bg_color)
ax.set_facecolor(bg_color)

# 双系列柱状图：组间间隙 219%，同组蓝红重叠一小部分，红色盖住蓝色
bar_w = 1 / (1 + 2.19)          # 柱宽（使相邻同色柱间隙=219%）
offset = 0.35 * bar_w           # 同组蓝红偏移，重叠 30% 柱宽
x_pos = np.arange(len(quarters))

ax.bar(x_pos - offset, sales, width=bar_w, color=color_sales,
       edgecolor='none', zorder=3)
ax.bar(x_pos + offset, profit, width=bar_w, color=color_profit,
       edgecolor='none', zorder=4)

# 柱顶数值标签
for x, s, p in zip(x_pos, sales, profit):
    ax.text(x - offset, s + 80, f'{s}', ha='center', va='bottom',
            fontsize=8, color=text_color, zorder=8)
    ax.text(x + offset, p + 80, f'{p}', ha='center', va='bottom',
            fontsize=8, color=text_color, zorder=8)

# 横轴标签
ax.set_xticks(x_pos)
ax.set_xticklabels(quarters, fontproperties=f_xlabel, color=text_color)

# 纵轴设置
ax.set_ylim(0, 6000)
ax.set_yticks([])
ax.tick_params(axis='y', length=0, pad=6, labelleft=False)
ax.set_xlim(-0.5, len(quarters) - 0.5)

# y=0 实线横线
fig.lines.append(Line2D([0.13, 0.97], [0.18, 0.18],
                        transform=fig.transFigure, linestyle='-',
                        linewidth=0.8, color=grid_color, alpha=0.9, zorder=6))

# 轴线隐藏
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_visible(False)
ax.spines['bottom'].set_visible(False)
ax.tick_params(axis='x', length=0, pad=8)

# 图例标注框：蓝框标注销售额（上），红框标注利润额（下）
# 位置在 Q2 柱子上方，框左端与 Q2 蓝柱左端对齐
label_color = '#C8CDD8'
f_box = FontProperties(family='Microsoft YaHei', size=8)
q2_idx = 5
box_x_left = q2_idx - offset - bar_w / 2 - 0.049
box_width = 0.70
box_height = 450
red_box_y = 2262
blue_box_y = 2962
ax.add_patch(Rectangle((box_x_left, blue_box_y), box_width, box_height,
                       facecolor=bg_color, edgecolor=color_sales,
                       linewidth=1.5, zorder=10))
ax.text(box_x_left + box_width / 2, blue_box_y + box_height / 2, '销售额',
        ha='center', va='center', fontproperties=f_box,
        color=label_color, zorder=11)
ax.add_patch(Rectangle((box_x_left, red_box_y), box_width, box_height,
                       facecolor=bg_color, edgecolor=color_profit,
                       linewidth=1.5, zorder=10))
ax.text(box_x_left + box_width / 2, red_box_y + box_height / 2, '利润额',
        ha='center', va='center', fontproperties=f_box,
        color=label_color, zorder=11)

# 主标题
fig.text(0.05, 0.94, '2021年至今季度销售额(万)和利润额(万)',
         ha='left', va='top', fontproperties=f_title, color=text_color)
# 副标题
fig.text(0.05, 0.86, '2022年第二季度销售额首次出现下降，降幅达到15%',
         ha='left', va='top', fontproperties=f_sub, color=text_color)

# 底部脚注
fig.text(0.05, 0.035, '*注：数据来源于公司销售系统，统计日期截至2022.06.30',
         ha='left', va='bottom', fontproperties=f_note, color=text_color)

plt.subplots_adjust(left=0.13, right=0.97, top=0.74, bottom=0.18)
plt.savefig('层叠.png', facecolor=bg_color, dpi=150)
print('saved 层叠.png')
