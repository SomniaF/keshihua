# -*- coding: utf-8 -*-
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.font_manager import FontProperties

# 字体定义
f_title  = FontProperties(family='Microsoft YaHei', size=18, weight='bold')
f_sub    = FontProperties(family='Microsoft YaHei', size=11, weight='normal')
f_legend = FontProperties(family='Microsoft YaHei', size=9, weight='normal')
f_value  = FontProperties(family='Microsoft YaHei', size=8, weight='bold')
f_quart  = FontProperties(family='Microsoft YaHei', size=10, weight='bold')
f_axis   = FontProperties(family='Microsoft YaHei', size=10, weight='normal')
f_note   = FontProperties(family='Microsoft YaHei', size=8)

# 数据
months    = [f'{m}月' for m in range(1, 13)]
sales     = [2354, 1902, 3524, 2698, 2896, 2563, 3156, 2896, 3621, 2635, 2963, 2789]
quarters  = ['Q1', 'Q2', 'Q3', 'Q4']
q_total   = [7780, 8157, 9673, 8387]
q_color   = ['#0070C0', '#C55A11', '#BF9000', '#7030A0']   # 蓝/红褐/金黄/紫红

# 颜色
bg_color    = '#1A1F3A'
text_color  = '#FFFFFF'
sub_color   = '#FFFFFF'

# 画布
fig_w = 14.68 / 2.54
fig_h = 10.47 / 2.54
fig, ax = plt.subplots(figsize=(fig_w, fig_h), dpi=150)
fig.patch.set_facecolor(bg_color)
ax.set_facecolor(bg_color)

n = len(months)
# x 坐标：季度内月份间距1，季度间隔1.8
x = []
for i in range(n):
    qi, mi = divmod(i, 3)
    x.append(qi * 4.0 + mi)
bar_w = 0.38

# 季度背景色块（高度按季度总销量比例，与对应柱形同色半透明）
for qi in range(4):
    x_start = x[qi * 3] - 0.5
    x_end = x[qi * 3 + 2] + 0.5
    rect = mpatches.Rectangle((x_start, 0), x_end - x_start, q_total[qi],
                              facecolor=q_color[qi], alpha=0.28,
                              edgecolor='none', zorder=0)
    ax.add_patch(rect)
    # 季度总销量标注（背景块顶部中央上方）
    cx = (x_start + x_end) / 2
    ax.text(cx, q_total[qi] + 120, f'{q_total[qi]}',
            ha='center', va='bottom', fontproperties=f_quart,
            color=text_color, zorder=8)

# 柱状图（按季度着色）
bar_colors = [q_color[i // 3] for i in range(n)]
bars = ax.bar(x, sales, width=bar_w, color=bar_colors,
              edgecolor='none', zorder=3)

# 柱顶数值标签
for i in range(n):
    ax.text(x[i], sales[i] + 90, f'{sales[i]}',
            ha='center', va='bottom', fontproperties=f_value,
            color='#DCE4F0', zorder=8)


# X 轴标签（手动绘制）
label_y = -max(sales) * 0.05
for xi, m in zip(x, months):
    ax.text(xi, label_y, m, ha='center', va='top',
            fontproperties=f_axis, color=text_color)


# 坐标范围与去轴线
ax.set_xlim(x[0] - 0.6, x[-1] + 0.6)
ax.set_ylim(label_y * 2.2, max(q_total) * 1.08)
ax.axis('off')

# 底部基线横线
ax.axhline(y=0, xmin=0, xmax=1, color='#8A92B8', linewidth=0.8, zorder=5)

# 主标题 / 副标题（左上）
fig.text(0.05, 0.94, '2021年各月化妆品销量走势',
         ha='left', va='top', fontproperties=f_title, color=text_color)
fig.text(0.05, 0.86, '第三季度销量最多9673，9月单月销量最大3621',
         ha='left', va='top', fontproperties=f_sub, color=sub_color)


# 底部脚注
fig.text(0.05, 0.04, '*注：数据来源于公司销售系统，统计日期截至2021.12.31',
         ha='left', va='bottom', fontproperties=f_note, color=sub_color)

plt.subplots_adjust(left=0.08, right=0.97, top=0.72, bottom=0.12)
plt.savefig('复合柱形图.png', facecolor=bg_color, dpi=150)
print('saved 复合柱形图.png')