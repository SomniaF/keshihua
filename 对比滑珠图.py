# -*- coding: utf-8 -*-
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
import matplotlib.patches as mpatches

# 字体定义（参考滑珠.py）
f_title  = FontProperties(family='Microsoft YaHei', size=16, weight='bold')
f_sub    = FontProperties(family='Microsoft YaHei', size=9, weight='normal')
f_legend = FontProperties(family='Microsoft YaHei', size=9, weight='normal')
f_value  = FontProperties(family='Microsoft YaHei', size=9, weight='bold')
f_value2 = FontProperties(family='Microsoft YaHei', size=8, weight='normal')
f_axis   = FontProperties(family='Microsoft YaHei', size=11, weight='normal')
f_note   = FontProperties(family='Microsoft YaHei', size=8)

# 数据（按 2022 完成率降序排列：华南 > 华北 > 东北 > 西北 > 华东）
regions   = ['华南', '华北', '东北', '西北', '华东']
rate_2022 = [86, 74, 62, 51, 35]      # 2022 完成率
rate_2021 = [92, 69, 53, 39, 45]      # 2021 完成率

# 颜色
bg_color    = '#1A1F3A'
color_track = '#3A4170'   # 背景轨道 灰蓝
color_2022  = '#0070C0'   # 2022 亮蓝
color_2021  = '#8A8A9A'   # 2021 灰
color_line  = '#CFD6E6'   # 连线 浅灰
text_color  = '#FFFFFF'
sub_color   = '#B8C0D4'
note_color  = '#7A82A4'

# 画布（尺寸参考滑珠.py）
fig_w = 12.0 / 2.54
fig_h = 7.5 * 1.3 / 2.54
fig, ax = plt.subplots(figsize=(fig_w, fig_h), dpi=150)
fig.patch.set_facecolor(bg_color)
ax.set_facecolor(bg_color)

n = len(regions)
y = list(range(n))[::-1]   # 自上而下降序：第一个在最上方
bar_h = 0.26          # 柱高（=圆直径）

# 背景轨道：左侧蓝色柱(0~2022) + 右侧灰蓝柱(2022~100)，直角无半圆
ax.barh(y, rate_2022, height=bar_h, color=color_2022, edgecolor='none', zorder=3)
ax.barh(y, [100 - r for r in rate_2022], height=bar_h, left=rate_2022,
        color=color_track, edgecolor='none', zorder=3)

# 两个年份圆点之间不连线

# 2021 圆点（灰，白边，与 2022 同样大小）
ax.plot(rate_2021, y, 'o', markersize=8,
        markerfacecolor=color_2021, markeredgecolor=text_color,
        markeredgewidth=1.2, zorder=5)

# 2022 圆点（亮蓝，白边）—— 滑珠
ax.plot(rate_2022, y, 'o', markersize=8,
        markerfacecolor=color_2022, markeredgecolor=text_color,
        markeredgewidth=1.2, zorder=9)

# 数值标签：仅保留 2022 完成率，置于蓝圆正上方，字体白色
for i in range(n):
    ax.text(rate_2022[i], y[i] + 0.25, f'{rate_2022[i]}%', ha='center', va='bottom',
            fontproperties=f_value, color=text_color, zorder=8)

# Y 轴区域标签（左侧）
for i, reg in zip(range(n), regions):
    ax.text(-10, y[i], reg, ha='right', va='center',
            fontproperties=f_axis, color=text_color)

# 坐标范围与去轴线
ax.set_xlim(-22, 112)
ax.set_ylim(-0.8, n - 0.2)
ax.axis('off')

# 主标题 / 副标题（左上）
fig.text(0.05, 0.94, '2022年上半年销量目标达成率同比去年情况',
         ha='left', va='top', fontproperties=f_title, color=text_color)
fig.text(0.05, 0.82, '华南完成率最高达到86%，华东最低35%，其中华南和华东不及2021年',
         ha='left', va='top', fontproperties=f_sub, color=sub_color)

# 图例（副标题下方，2022 与 2021 左右排列，圆点带白色外圈）
ax_leg = fig.add_axes([0.08, 0.71, 0.6, 0.05], facecolor=bg_color)
ax_leg.set_xlim(0, 1)
ax_leg.set_ylim(0, 1)
ax_leg.axis('off')
ax_leg.plot(0.02, 0.5, 'o', markersize=7, markerfacecolor=color_2022,
            markeredgecolor=text_color, markeredgewidth=1.0)
ax_leg.text(0.06, 0.5, '2022完成率', ha='left', va='center',
            fontproperties=f_legend, color=text_color)
ax_leg.plot(0.40, 0.5, 'o', markersize=7, markerfacecolor=color_2021,
            markeredgecolor=text_color, markeredgewidth=1.0)
ax_leg.text(0.44, 0.5, '2021完成率', ha='left', va='center',
            fontproperties=f_legend, color=text_color)

# 底部脚注
fig.text(0.05, 0.04, '*注：数据来源于公司销售系统，统计日期截至2022.06.30',
         ha='left', va='bottom', fontproperties=f_note, color=note_color)

plt.subplots_adjust(left=0.08, right=0.97, top=0.72, bottom=0.12)
plt.savefig(r'D:\huaweixinjian\对比滑珠图.png', facecolor=bg_color, dpi=150)
print('saved 对比滑珠图.png')
