# -*- coding: utf-8 -*-
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.font_manager import FontProperties

# 字体定义（参考 数值.py）
f_title  = FontProperties(family='Microsoft YaHei', size=18, weight='bold')
f_sub    = FontProperties(family='Microsoft YaHei', size=11, weight='normal')
f_label  = FontProperties(family='Microsoft YaHei', size=10, weight='bold')
f_value  = FontProperties(family='Microsoft YaHei', size=9, weight='normal')
f_note   = FontProperties(family='Microsoft YaHei', size=9)

# 数据
departments = ['销售部', '采购部', '工程部', '财务部', '行政部', '人力部']
values = [29.20, 22.70, 17.50, 13.60, 10.30, 5.00]
total = 1664
people = [int(round(total * v / 100)) for v in values]

# 颜色（参考图高饱和对比色块）
bg_color   = '#1A1F3C'
text_color = '#FFFFFF'
sub_color  = '#A0A8C0'
colors = ['#E94E77', '#F5C518', '#3FB8AF', '#5DADE2', '#2E5C9E', '#9B59B6']

N = len(departments)
# 角度按人数占比分配，半径=数值（南丁格尔玫瑰图变体）
widths = [2 * np.pi * v / 100 for v in values]
theta = np.zeros(N)
cum = 0.0
for i in range(N):
    theta[i] = cum + widths[i] / 2
    cum += widths[i]

# 画布
fig_w = 14.68 / 2.54
fig_h = 10.47 / 2.54
fig = plt.figure(figsize=(fig_w, fig_h), dpi=150)
fig.patch.set_facecolor(bg_color)
ax = fig.add_subplot(111, projection='polar', facecolor=bg_color)

# 南丁格尔玫瑰图：角度按占比，半径=数值（放大扇形占比）
k = 3.3
values_scaled = [v * k for v in values]
ax.bar(theta, values_scaled, width=widths, bottom=0.0,
       color=colors, edgecolor='none', zorder=3)

ax.set_theta_zero_location('N')
ax.set_theta_direction(-1)
ax.set_xticks([])
ax.set_ylim(0, max(values_scaled) + 25)
ax.set_yticks([])
ax.grid(False)
ax.spines['polar'].set_visible(False)

# 笛卡尔叠加轴，用于绘制折线牵引线
rmax = max(values_scaled) + 25
ax2 = fig.add_axes(ax.get_position(), frameon=False)
ax2.set_xlim(-rmax, rmax)
ax2.set_ylim(-rmax, rmax)
ax2.set_aspect('equal')
ax2.axis('off')

# 各扇形牵引线与扇形的间隔（蓝色减小，绿色黄色增大）
gaps = [12, 16, 16, 8, 8, 12]
# 折线牵引线 + 首端小圆点（长度不变，无文字）
for i, ang in enumerate(theta):
    r0 = values_scaled[i]
    r_dot = r0 + gaps[i]   # 首端小圆点（与扇形间隔）
    r_mid = r_dot + 14     # 径向延伸终点（径向长度不变）
    x0 = r_dot * np.sin(ang); y0 = r_dot * np.cos(ang)
    x1 = r_mid * np.sin(ang); y1 = r_mid * np.cos(ang)
    side = 1 if x1 >= 0 else -1
    x2 = x1 + side * 13
    y2 = y1
    ax2.scatter([x0], [y0], s=20, color=colors[i], zorder=5)
    ax2.plot([x0, x1, x2], [y0, y1, y2], color=colors[i], linewidth=0.8, zorder=4)

# 主标题 / 副标题（左上）
fig.text(0.05, 0.94, '2021年各部门人数分布',
         ha='left', va='top', fontproperties=f_title, color=text_color)
fig.text(0.05, 0.85, f'公司总人数{total}，销售部人数最多{people[0]}，占比{values[0]:.1f}%',
         ha='left', va='top', fontproperties=f_sub, color=text_color)

# 底部脚注
fig.text(0.05, 0.06, '*注：数据来源于公司人力资源系统，统计日期截至2022.01.01',
         ha='left', va='bottom', fontproperties=f_note, color=text_color)

plt.subplots_adjust(left=0.01, right=0.99, top=0.80, bottom=0.02)
plt.savefig('南丁格尔玫瑰图.png', facecolor=bg_color, dpi=150)
print('saved 南丁格尔玫瑰图.png')
