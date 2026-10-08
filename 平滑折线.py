# -*- coding: utf-8 -*-
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
from matplotlib.patches import FancyBboxPatch

f_title  = FontProperties(family='Microsoft YaHei', size=20, weight='bold')
f_sub    = FontProperties(family='Microsoft YaHei', size=14, weight='normal')
f_dlabel = FontProperties(family='Calibri', size=10)
f_xlabel = FontProperties(family='Microsoft YaHei', size=9)
f_ylabel = FontProperties(family='Calibri', size=10)
f_note   = FontProperties(family='Microsoft YaHei', size=9)

months = ['5月', '6月', '7月', '8月', '9月', '10月', '11月', '12月', '1月', '2月', '3月']
sales = [146, 198, 296, 412, 506, 615, 789, 1021, 3782, 3215, 2936]

x = list(range(len(months)))
y = sales

bg_color   = '#1A1F3A'
text_color = '#FFFFFF'
line_color = '#e87a5d'


def catmull_rom(points, seg=40):
    pts = [points[0]] + points + [points[-1]]
    result = []
    for i in range(len(points) - 1):
        p0, p1, p2, p3 = pts[i], pts[i + 1], pts[i + 2], pts[i + 3]
        for j in range(seg):
            t = j / seg
            t2, t3 = t * t, t * t * t
            sx = 0.5 * ((2 * p1[0]) + (-p0[0] + p2[0]) * t +
                        (2 * p0[0] - 5 * p1[0] + 4 * p2[0] - p3[0]) * t2 +
                        (-p0[0] + 3 * p1[0] - 3 * p2[0] + p3[0]) * t3)
            sy = 0.5 * ((2 * p1[1]) + (-p0[1] + p2[1]) * t +
                        (2 * p0[1] - 5 * p1[1] + 4 * p2[1] - p3[1]) * t2 +
                        (-p0[1] + 3 * p1[1] - 3 * p2[1] + p3[1]) * t3)
            result.append((sx, sy))
    result.append(points[-1])
    return result


points = list(zip(x, y))
smooth = catmull_rom(points)
sx = [p[0] for p in smooth]
sy = [p[1] for p in smooth]

fig_w = 14.68 / 2.54
fig_h = 10.47 / 2.54
fig, ax = plt.subplots(figsize=(fig_w, fig_h), dpi=150)
fig.patch.set_facecolor(bg_color)
ax.set_facecolor(bg_color)

ax.plot(sx, sy, color=line_color, linewidth=1.0, zorder=3)


peak_idx = y.index(max(y))
peak_y = y[peak_idx]
sp_idx = sy.index(max(sy))
sp_x, sp_y = sx[sp_idx], sy[sp_idx]
ax.plot([sp_x, sp_x], [0, sp_y], color=line_color, linestyle='--', linewidth=1.0, alpha=0.8, zorder=2)
ax.text(sp_x, sp_y + 150, str(peak_y), ha='center', va='bottom',
        fontproperties=f_dlabel, color=text_color, fontsize=11)

ax.set_xticks([i - 0.5 for i in range(len(months) + 1)])
ax.set_xticklabels([])
for xi, m in zip(x, months):
    ax.text(xi, -0.05, m, transform=ax.get_xaxis_transform(),
            ha='center', va='top', fontproperties=f_xlabel, color=text_color)
ax.set_yticks([0, 1000, 2000, 3000, 4000])
ax.set_yticklabels(['0', '1,000', '2,000', '3,000', '4,000'], fontproperties=f_ylabel, color=line_color)
ax.set_ylim(0, 4500)
ax.set_xlim(-0.5, len(months) - 0.5)

ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_visible(False)
ax.spines['bottom'].set_position('zero')
ax.spines['bottom'].set_color(text_color)
ax.spines['bottom'].set_linewidth(0.8)
ax.tick_params(axis='x', direction='out', length=4, color=text_color, pad=6)
ax.tick_params(axis='y', length=0, pad=6)

fig.text(0.05, 0.94, '化妆品品类月度销量走势', ha='left', va='top',
         fontproperties=f_title, color=text_color)
fig.text(0.05, 0.86, '2022年销量迅速增加，1月最高，销量达到3782', ha='left', va='top',
         fontproperties=f_sub, color=text_color)

unit = 0.84 / 11
y_box = 0.12
h_box = 0.034
half_gap = 0.0068

w1 = 8 * unit
cx1 = 0.13 + 4 * unit - half_gap
fig.patches.append(FancyBboxPatch((cx1 - w1 / 2, y_box - h_box / 2), w1, h_box,
                                  boxstyle='round,pad=0.002,rounding_size=0.008',
                                  facecolor='#5ec8d6', edgecolor='none',
                                  transform=fig.transFigure, zorder=5))
fig.text(cx1, y_box, '2021', ha='center', va='center', fontproperties=f_xlabel,
         color=text_color, fontsize=9, zorder=6)

w2 = 3 * unit
cx2 = 0.13 + 9.5 * unit + half_gap
fig.patches.append(FancyBboxPatch((cx2 - w2 / 2, y_box - h_box / 2), w2, h_box,
                                  boxstyle='round,pad=0.002,rounding_size=0.008',
                                  facecolor='#f5c842', edgecolor='none',
                                  transform=fig.transFigure, zorder=5))
fig.text(cx2, y_box, '2022', ha='center', va='center', fontproperties=f_xlabel,
         color=text_color, fontsize=9, zorder=6)

fig.text(0.05, 0.04, '*注：数据来源于公司销售系统，统计日期截至2022.03.31',
         ha='left', va='bottom', fontproperties=f_note, fontsize=8, color=text_color)

plt.subplots_adjust(left=0.13, right=0.97, top=0.78, bottom=0.22)
plt.savefig('化妆品销量走势.png', facecolor=bg_color, dpi=150)
print('saved 化妆品销量走势.png')
