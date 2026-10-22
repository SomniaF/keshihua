import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
from matplotlib.patches import Wedge
import numpy as np

plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei']
plt.rcParams['axes.unicode_minus'] = False

f_title = FontProperties(family='Microsoft YaHei', size=18, weight='bold')
f_sub   = FontProperties(family='Microsoft YaHei', size=12, weight='normal')
f_note  = FontProperties(family='Microsoft YaHei', size=8)

BG_COLOR = '#1A1F3A'

fig = plt.figure(figsize=(14.68 / 2.54, 10.88 / 2.54), facecolor=BG_COLOR)

ax = fig.add_axes([0.25, 0.12, 0.5, 0.72])
ax.set_facecolor(BG_COLOR)
ax.set_aspect('equal')
ax.axis('off')

percent = 85
remaining = 15

r_outer = 0.9
r_inner = 0.80

start_angle = 207
filled_span = 360 * percent / 100

n_segments = 200
purple = np.array([138, 43, 226]) / 255.0
pink = np.array([255, 105, 180]) / 255.0

for i in range(n_segments):
    t0 = start_angle + filled_span * i / n_segments
    t1 = start_angle + filled_span * (i + 1) / n_segments
    frac = i / (n_segments - 1)
    color = pink * (1 - frac) + purple * frac
    wedge = Wedge((0, 0), r_outer, t0, t1,
                  width=r_outer - r_inner, facecolor=color, edgecolor='none')
    ax.add_patch(wedge)

empty_start = start_angle + filled_span
empty_span = 360 * remaining / 100
wedge_empty = Wedge((0, 0), r_outer, empty_start, empty_start + empty_span,
                    width=r_outer - r_inner, facecolor='#2A3358', edgecolor='none')
ax.add_patch(wedge_empty)

ax.text(0, 0.12, f'{percent}%', ha='center', va='center',
        fontsize=42, color='white', fontweight='bold')
ax.text(0, -0.28, '目标完成率', ha='center', va='center',
        fontsize=11, color='#C8D0EC')

fig.text(0.05, 0.94, '2022年上半年目标完成率', ha='left', va='top',
         fontproperties=f_title, color='#FFFFFF')
fig.text(0.05, 0.86, '截至6月30日销售目标总体完成率达到85%', ha='left', va='top',
         fontproperties=f_sub, color='#FFFFFF')
fig.text(0.05, 0.025, '*注：数据来源于公司销售系统', ha='left', va='bottom',
         fontproperties=f_note, color='#FFFFFF')

ax.set_xlim(-1, 1)
ax.set_ylim(-1, 1)

plt.savefig('单值圆环.png', dpi=200, facecolor=BG_COLOR)
print('done')
