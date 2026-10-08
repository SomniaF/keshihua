# -*- coding: utf-8 -*-
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
from matplotlib.patches import FancyBboxPatch
from matplotlib.lines import Line2D

# 字体定义
f_title  = FontProperties(family='Microsoft YaHei', size=20, weight='bold')
f_sub    = FontProperties(family='Microsoft YaHei', size=12, weight='normal')
f_legend = FontProperties(family='Microsoft YaHei', size=9, weight='normal')
f_value  = FontProperties(family='Microsoft YaHei', size=9, weight='bold')
f_axis   = FontProperties(family='Microsoft YaHei', size=10, weight='normal')
f_note   = FontProperties(family='Microsoft YaHei', size=8)

# 数据
months    = ['1月', '2月', '3月', '4月', '5月', '6月']
sales_2021 = [1686, 1345, 1934, 1658, 1865, 1936]
sales_2022 = [1385, 1846, 1654, 1936, 2564, 2236]

# 颜色
bg_color    = '#1A1F3A'
color_2021  = '#E74C3C'   # 2021 红色
color_2022  = '#3498DB'   # 2022 蓝色
text_color  = '#FFFFFF'
sub_color   = '#FFFFFF'

# 画布
fig_w = 14.68 / 2.54
fig_h = 10.47 / 2.54
fig, ax = plt.subplots(figsize=(fig_w, fig_h), dpi=150)
fig.patch.set_facecolor(bg_color)
ax.set_facecolor(bg_color)

x = list(range(len(months)))

# 折线（线宽 1.5 磅）+ 实心小圆点标记
ax.plot(x, sales_2021, color=color_2021, linewidth=1.5, zorder=3,
        marker='o', markersize=5, markerfacecolor=color_2021,
        markeredgecolor=color_2021, markeredgewidth=1.0)
ax.plot(x, sales_2022, color=color_2022, linewidth=1.5, zorder=3,
        marker='o', markersize=5, markerfacecolor=color_2022,
        markeredgecolor=color_2022, markeredgewidth=1.0)

# 数据点数值标签（白色，上下两侧分布）
for i in x:
    if sales_2021[i] >= sales_2022[i]:
        ax.text(i, sales_2021[i] + 60, f'{sales_2021[i]}',
                ha='center', va='bottom', fontproperties=f_value, color=text_color, zorder=8)
        ax.text(i, sales_2022[i] - 60, f'{sales_2022[i]}',
                ha='center', va='top', fontproperties=f_value, color=text_color, zorder=8)
    else:
        ax.text(i, sales_2022[i] + 60, f'{sales_2022[i]}',
                ha='center', va='bottom', fontproperties=f_value, color=text_color, zorder=8)
        ax.text(i, sales_2021[i] - 60, f'{sales_2021[i]}',
                ha='center', va='top', fontproperties=f_value, color=text_color, zorder=8)

# X 轴标签
for xi, m in zip(x, months):
    ax.text(xi, -0.05, m, transform=ax.get_xaxis_transform(),
            ha='center', va='top', fontproperties=f_axis, color=text_color)

# Y 轴范围与刻度
y_max = max(max(sales_2021), max(sales_2022))
ax.set_ylim(-30, y_max * 1.18)
ax.set_xlim(-0.5, len(months) - 0.5)
ax.set_yticks([0, 500, 1000, 1500, 2000, 2500, 3000])
ax.set_yticklabels(['0', '500', '1,000', '1,500', '2,000', '2,500', '3,000'],
                   fontproperties=f_axis, color=text_color)

# 去除所有轴线，改用虚线网格
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_visible(False)
ax.spines['bottom'].set_visible(False)
ax.tick_params(axis='x', length=0, pad=6)
ax.tick_params(axis='y', length=0, pad=6)

# Y 轴每个刻度对应虚线网格
for yt in [0, 500, 1000, 1500, 2000, 2500, 3000]:
    ax.axhline(y=yt, color='#8A92B8', linewidth=0.6, linestyle='--', alpha=0.5, zorder=1)

# 主标题 / 副标题（左上）
fig.text(0.05, 0.94, '2022年上半年各月同比去年销量',
         ha='left', va='top', fontproperties=f_title, color=text_color)
fig.text(0.05, 0.86, '上半年同比去年增长明显，5月份同比增长最多，增长近40%',
         ha='left', va='top', fontproperties=f_sub, color=sub_color)

# 图例（副标题右下角，左右分布：2021年在前，2022年在后）
legend_y = 0.78
fig.lines.append(Line2D([0.76, 0.785], [legend_y, legend_y], color=color_2021,
                         linewidth=1.5, transform=fig.transFigure, figure=fig))
fig.text(0.7725, legend_y, '●', ha='center', va='center',
         fontproperties=f_legend, color=color_2021, fontsize=7)
fig.text(0.795, legend_y, '2021年', ha='left', va='center',
         fontproperties=f_legend, color=text_color)
fig.lines.append(Line2D([0.88, 0.905], [legend_y, legend_y], color=color_2022,
                         linewidth=1.5, transform=fig.transFigure, figure=fig))
fig.text(0.8925, legend_y, '●', ha='center', va='center',
         fontproperties=f_legend, color=color_2022, fontsize=7)
fig.text(0.915, legend_y, '2022年', ha='left', va='center',
         fontproperties=f_legend, color=text_color)

# 底部脚注
fig.text(0.05, 0.025, '*注：数据来源于公司销售系统，统计日期截至2022.06.30',
         ha='left', va='bottom', fontproperties=f_note, color=sub_color)

plt.subplots_adjust(left=0.10, right=0.97, top=0.72, bottom=0.14)
plt.savefig('对比折线.png', facecolor=bg_color, dpi=150)
print('saved 对比折线.png')