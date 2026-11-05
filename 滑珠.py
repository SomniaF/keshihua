# -*- coding: utf-8 -*-
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
import matplotlib.patches as mpatches

# 字体定义（参考对比柱形.py）
f_title  = FontProperties(family='Microsoft YaHei', size=18, weight='bold')
f_sub    = FontProperties(family='Microsoft YaHei', size=11, weight='normal')
f_legend = FontProperties(family='Microsoft YaHei', size=9, weight='normal')
f_value  = FontProperties(family='Microsoft YaHei', size=8, weight='normal')
f_axis   = FontProperties(family='Microsoft YaHei', size=11, weight='normal')
f_note   = FontProperties(family='Microsoft YaHei', size=8)

# 数据（按完成率降序排列：华南 > 华北 > 东北 > 西北 > 华东）
regions = ['华南', '华北', '东北', '西北', '华东']
rates   = [86, 74, 62, 51, 35]      # 完成率
rests   = [14, 26, 38, 49, 65]      # 未完成占比

# 颜色
bg_color    = '#1A1F3A'
color_done  = '#0070C0'   # 已完成 亮蓝
color_rest  = '#3A4170'   # 未完成 灰蓝
text_color  = '#FFFFFF'
sub_color   = '#FFFFFF'

# 画布（尺寸较小）
fig_w = 12.0 / 2.54
fig_h = 7.5 * 1.3 / 2.54
fig, ax = plt.subplots(figsize=(fig_w, fig_h), dpi=150)
fig.patch.set_facecolor(bg_color)
ax.set_facecolor(bg_color)

n = len(regions)
y = list(range(n))[::-1]   # 自上而下降序：第一个在最上方
bar_h = 0.52          # 柱高

# 横向堆叠柱形图：左侧完成率（亮蓝）+ 右侧未完成（灰色），总长100
ax.barh(y, rates, height=bar_h, color=color_done, edgecolor='none', zorder=3)
ax.barh(y, rests, height=bar_h, left=rates, color=color_rest, edgecolor='none', zorder=3)

# 柱形两端半圆（直径=柱高，zorder低于柱子，柱子盖住内半，露出外半圆）
ax.plot([0] * n, y, 'o', markersize=15.4,
        markerfacecolor=color_done, markeredgecolor='none', zorder=2)
ax.plot([100] * n, y, 'o', markersize=15.4,
        markerfacecolor=color_rest, markeredgecolor='none', zorder=2)

# 完成率数值（紧贴圆左侧）
for i in range(n):
    ax.text(rates[i] - 7, y[i], f'{rates[i]}%', ha='right', va='center',
            fontproperties=f_value, color=text_color, zorder=8)

# 蓝色部分最右端的圆（白边蓝填充，直径=柱高）
ax.plot(rates, y, 'o', markersize=15.4,
        markerfacecolor=color_done, markeredgecolor=text_color,
        markeredgewidth=1.5, zorder=9)

# Y 轴区域标签（手动绘制，左侧）
for i, reg in zip(range(n), regions):
    ax.text(-10, y[i], reg, ha='right', va='center',
            fontproperties=f_axis, color=text_color)

# 坐标范围与去轴线
ax.set_xlim(-22, 108)
ax.set_ylim(-0.8, n - 0.2)
ax.axis('off')

# 主标题 / 副标题（左上）
fig.text(0.05, 0.94, '2022年上半年产品销量目标达成率情况',
         ha='left', va='top', fontproperties=f_title, color=text_color)
fig.text(0.05, 0.82, '华南完成率最高达到86%，华东最低35%',
         ha='left', va='top', fontproperties=f_sub, color=sub_color)

# 底部脚注
fig.text(0.05, 0.04, '*注：数据来源于公司销售系统，统计日期截至2022.06.30',
         ha='left', va='bottom', fontproperties=f_note, color=sub_color)

plt.subplots_adjust(left=0.08, right=0.97, top=0.72, bottom=0.12)
plt.savefig('滑珠.png', facecolor=bg_color, dpi=150)
print('saved 滑珠.png')
