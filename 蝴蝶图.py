# -*- coding: utf-8 -*-
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
from matplotlib.lines import Line2D
import numpy as np

# 字体定义
f_title  = FontProperties(family='Microsoft YaHei', size=20, weight='bold')
f_sub    = FontProperties(family='Microsoft YaHei', size=12, weight='normal')
f_label  = FontProperties(family='Microsoft YaHei', size=11)
f_value  = FontProperties(family='Microsoft YaHei', size=9)
f_note   = FontProperties(family='Microsoft YaHei', size=9)
f_legend = FontProperties(family='Microsoft YaHei', size=10)

# 数据（按图片从上到下顺序）
regions = ['华南', '华北', '东北', '西北', '华东']
sales_2022 = [2238, 1531, 1426, 1321, 1215]
sales_2021 = [2066, 1436, 1531, 1265, 1003]

# 尺寸 14.68cm x 10.47cm
fig_w = 14.68 / 2.54
fig_h = 10.47 / 2.54
fig, ax = plt.subplots(figsize=(fig_w, fig_h), dpi=150)

# 颜色
bg_color    = '#1A1F3A'
text_color  = '#FFFFFF'
grid_color  = '#6A71A8'
color_2022  = '#0070C0'   # 2022 标准蓝
color_2021  = '#E85D75'   # 2021 红色

fig.patch.set_facecolor(bg_color)
ax.set_facecolor(bg_color)

# 蝴蝶图：左侧2022（向左延伸），右侧2021（向右延伸）
bar_h = 0.5
# 同色条形之间垂直间隙 = 150% 条高，行中心距 = bar_h * (1 + 1.5)
y_step = bar_h * 2.5
y_pos = np.arange(len(regions)) * y_step
max_val = max(max(sales_2022), max(sales_2021))

# 坐标轴设置（先定 xlim 以便换算 1cm 对应的数据单位）
ax.set_ylim(-0.9, y_pos[-1] + 0.7)
ax.set_xlim(-max_val * 1.18, max_val * 1.18)
ax.invert_yaxis()

# 计算 1cm 对应的数据单位（axes 宽度占比 = right - left）
ax_w_inch = (0.97 - 0.08) * fig_w
ax_w_cm = ax_w_inch * 2.54
data_width = max_val * 1.18 * 2
cm_in_data = data_width / ax_w_cm
# 左右条形之间的距离为 2cm（每侧留 1cm）
gap = cm_in_data * 1.0

# 左侧条形（2022）：从 -v22 到 -gap
left_widths = [v - gap for v in sales_2022]
ax.barh(y_pos, left_widths, left=[-v for v in sales_2022],
        height=bar_h, color=color_2022, edgecolor='none', zorder=3,
        align='center')
# 右侧条形（2021）：从 gap 到 v21
right_widths = [v - gap for v in sales_2021]
ax.barh(y_pos, right_widths, left=gap,
        height=bar_h, color=color_2021, edgecolor='none', zorder=3,
        align='center')

# 数值写在条形上（条形内远离中心端，白色文字）
inner_pad = max_val * 0.012
for y, v22, v21 in zip(y_pos, sales_2022, sales_2021):
    ax.text(-v22 + inner_pad, y, f'{v22}', ha='left', va='center',
            fontproperties=f_value, color=text_color, zorder=8)
    ax.text(v21 - inner_pad, y, f'{v21}', ha='right', va='center',
            fontproperties=f_value, color=text_color, zorder=8)

# 中间区域名称
for y, name in zip(y_pos, regions):
    ax.text(0, y, name, ha='center', va='center',
            fontproperties=f_label, color=text_color, zorder=9,
            bbox=dict(facecolor=bg_color, edgecolor='none', pad=3))

# 隐藏所有轴线和刻度
for spine in ax.spines.values():
    spine.set_visible(False)
ax.set_xticks([])
ax.set_yticks([])
ax.tick_params(length=0)

# 图例（往外挪、往上挪，无边框）
legend_y = -0.6
ax.text(-max_val * 0.45, legend_y, '2022', ha='center', va='center',
        fontproperties=f_legend, color=color_2022, zorder=10)
ax.text(max_val * 0.45, legend_y, '2021', ha='center', va='center',
        fontproperties=f_legend, color=color_2021, zorder=10)

# 主标题
fig.text(0.05, 0.94, '2022年上半年各区域对比去年销量',
         ha='left', va='top', fontproperties=f_title, color=text_color)
# 副标题
fig.text(0.05, 0.86, '2022年整体销量高于2021年，只有东北区域较2021有所下降',
         ha='left', va='top', fontproperties=f_sub, color=text_color)

# 底部脚注
fig.text(0.05, 0.035, '*注：数据来源于公司销售系统，统计日期截至2022.06.30',
         ha='left', va='bottom', fontproperties=f_note, color=text_color)

plt.subplots_adjust(left=0.08, right=0.97, top=0.78, bottom=0.12)
plt.savefig('蝴蝶图.png', facecolor=bg_color, dpi=150)
print('saved 蝴蝶图.png')