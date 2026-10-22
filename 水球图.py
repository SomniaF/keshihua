# -*- coding: utf-8 -*-
"""水球图：圆形液位填充进度指示器（平面液面）"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
from matplotlib.patches import Circle
import numpy as np

plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei']
plt.rcParams['axes.unicode_minus'] = False

f_title = FontProperties(family='Microsoft YaHei', size=18, weight='bold')
f_sub   = FontProperties(family='Microsoft YaHei', size=12, weight='normal')
f_note  = FontProperties(family='Microsoft YaHei', size=8)

BG_COLOR = '#1A1F3A'
LIQUID_COLOR = '#0070C0'
RING_COLOR = '#0070C0'

percent = 65
aux = 100

fig = plt.figure(figsize=(14.68 / 2.54, 10.88 / 2.54), facecolor=BG_COLOR)
ax = fig.add_axes([0.25, 0.12, 0.5, 0.72])
ax.set_facecolor(BG_COLOR)
ax.set_aspect('equal')
ax.axis('off')

R = 0.9
cx, cy = 0, 0
R_inner = R - 0.06

clip_patch = Circle((cx, cy), R_inner, transform=ax.transData)

water_level = cy - R_inner + 2 * R_inner * percent / 100

x = np.linspace(cx - R_inner, cx + R_inner, 500)
ax.fill_between(x, water_level, cy - R_inner - 0.1, color=LIQUID_COLOR, alpha=0.95, zorder=2)
ax.plot([cx - R_inner, cx + R_inner], [water_level, water_level], color='#FFFFFF', linewidth=0.8, alpha=0.4, zorder=3)

for artist in ax.findobj():
    artist.set_clip_path(clip_patch)

ring_outer = Circle((cx, cy), R, fill=False, edgecolor=RING_COLOR, linewidth=2, zorder=4)
ax.add_patch(ring_outer)
ring_inner = Circle((cx, cy), R - 0.06, fill=False, edgecolor=RING_COLOR, linewidth=1.2, zorder=4)
ax.add_patch(ring_inner)

ax.text(cx, cy, f'{percent}%', ha='center', va='center',
        fontsize=46, color='white', fontweight='bold', zorder=5)

fig.text(0.05, 0.94, '2022年上半年目标完成率', ha='left', va='top',
         fontproperties=f_title, color='#FFFFFF')
fig.text(0.05, 0.86, f'截至6月30日销售目标总体完成率达到{percent}%', ha='left', va='top',
         fontproperties=f_sub, color='#FFFFFF')
fig.text(0.05, 0.025, '*注：数据来源于公司销售系统', ha='left', va='bottom',
         fontproperties=f_note, color='#FFFFFF')

ax.set_xlim(-1.1, 1.1)
ax.set_ylim(-1.1, 1.1)

plt.savefig('水球图.png', dpi=200, facecolor=BG_COLOR)
print('done')
