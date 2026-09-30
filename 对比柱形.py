# -*- coding: utf-8 -*-
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
import matplotlib.patches as mpatches

# 字体定义
f_title  = FontProperties(family='Microsoft YaHei', size=18, weight='bold')
f_sub    = FontProperties(family='Microsoft YaHei', size=11, weight='normal')
f_legend = FontProperties(family='Microsoft YaHei', size=9, weight='normal')
f_value  = FontProperties(family='Microsoft YaHei', size=6.3, weight='bold')
f_diff   = FontProperties(family='Microsoft YaHei', size=6.3, weight='bold')
f_axis   = FontProperties(family='Microsoft YaHei', size=10, weight='normal')
f_note   = FontProperties(family='Microsoft YaHei', size=8)

# 数据
products = ['口红', '面膜', '隔离', '防晒', '精华']
sales_2021 = [3568, 4135, 4436, 4106, 4936]
sales_2022 = [2569, 3241, 2965, 3209, 3541]
diff       = [999, 894, 1471, 897, 1395]

# 颜色
bg_color    = '#1A1F3A'
color_2021  = '#0070C0'   # 2021 标准蓝
color_2022  = '#88A8C8'   # 2022 浅蓝
text_color  = '#FFFFFF'
sub_color   = '#FFFFFF'

# 画布
fig_w = 14.68 / 2.54
fig_h = 10.47 / 2.54
fig, ax = plt.subplots(figsize=(fig_w, fig_h), dpi=150)
fig.patch.set_facecolor(bg_color)
ax.set_facecolor(bg_color)

n = len(products)
x = list(range(n))
bar_w = 0.22          # 柱宽
intra = 0.298         # 组内两柱中心间距 → 同色柱间隙 = 2.19 × bar_w
a = intra / 2

# 柱状图
bars1 = ax.bar([i - a for i in x], sales_2021, width=bar_w,
               color=color_2021, edgecolor='none', zorder=3)
bars2 = ax.bar([i + a for i in x], sales_2022, width=bar_w,
               color=color_2022, edgecolor='none', zorder=3)

# 柱顶数值标签
for i in x:
    ax.text(i - a, sales_2021[i] + 80, f'{sales_2021[i]}',
            ha='center', va='bottom', fontproperties=f_value, color='#DCE4F0', zorder=8)
    ax.text(i + a, sales_2022[i] - 80, f'{sales_2022[i]}',
            ha='center', va='top', fontproperties=f_value, color='#DCE4F0', zorder=8)

# 2021柱右边到2022柱中心的横线（柱顶高度，与2021同色）
for i in x:
    x_left = i - a + bar_w / 2
    x_right = i + a
    ax.plot([x_left, x_right], [sales_2021[i], sales_2021[i]],
            color=color_2021, linewidth=1.0, zorder=6)

# 两柱中间差值标注：箭头从2022柱中心顶部指向直线(2021柱顶)，误差值在箭头右边
for i in x:
    ax.annotate('', xy=(i + a, sales_2021[i]), xytext=(i + a, sales_2022[i]),
                arrowprops=dict(arrowstyle='->', color=text_color, lw=1.0), zorder=7)
    ax.text(i + a + 0.025, (sales_2021[i] + sales_2022[i]) / 2, f'{diff[i]}',
            ha='left', va='center', fontproperties=f_diff, color=text_color, zorder=8)

# X 轴标签（手动绘制，避免被 axis('off') 隐藏）
label_y = -max(sales_2021) * 0.04
for i, p in zip(x, products):
    ax.text(i, label_y, p, ha='center', va='top',
            fontproperties=f_axis, color=text_color)

# 坐标范围与去轴线
ax.set_xlim(-0.6, n - 0.4)
ax.set_ylim(label_y * 2.2, max(sales_2021) * 1.22)
ax.axis('off')

# 底部基线横线
ax.axhline(y=0, xmin=0, xmax=1, color='#8A92B8', linewidth=0.8, zorder=5)

# 主标题 / 副标题（左上）
fig.text(0.05, 0.94, '2022年商品对比去年销售情况',
         ha='left', va='top', fontproperties=f_title, color=text_color)
fig.text(0.05, 0.86, '商品整体比去年销量有所下降，其中隔离下降最多，下降33%',
         ha='left', va='top', fontproperties=f_sub, color=sub_color)

# 图例（标题下方偏左）
legend_y = 0.78
fig.text(0.05, legend_y, '■', ha='left', va='center',
         fontproperties=f_legend, color=color_2021, fontsize=14)
fig.text(0.075, legend_y, '2021销量', ha='left', va='center',
         fontproperties=f_legend, color=text_color)
fig.text(0.18, legend_y, '■', ha='left', va='center',
         fontproperties=f_legend, color=color_2022, fontsize=14)
fig.text(0.205, legend_y, '2022销量', ha='left', va='center',
         fontproperties=f_legend, color=text_color)

# 底部脚注
fig.text(0.05, 0.04, '*注：数据来源于公司销售系统，统计日期截至2022.01.01',
         ha='left', va='bottom', fontproperties=f_note, color=sub_color)

plt.subplots_adjust(left=0.08, right=0.97, top=0.72, bottom=0.12)
plt.savefig('对比柱形.png', facecolor=bg_color, dpi=150)
print('saved 对比柱形.png')