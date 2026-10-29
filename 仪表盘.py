# -*- coding: utf-8 -*-
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
from matplotlib.patches import Wedge, Circle
import numpy as np

f_title  = FontProperties(family='Microsoft YaHei', size=20, weight='bold')
f_label  = FontProperties(family='Microsoft YaHei', size=14)
f_center = FontProperties(family='Microsoft YaHei', size=24, weight='bold')

min_val = 50
max_val = 150
pointer_val = 76

gauge_start = 225
gauge_span = 270


def val_to_angle(val):
    return gauge_start - (val - min_val) / (max_val - min_val) * gauge_span


fig_w = 14.68 / 2.54
fig_h = 10.47 / 2.54
fig, ax = plt.subplots(figsize=(fig_w, fig_h), dpi=150, subplot_kw={'aspect': 'equal'})

bg_color   = '#1A1F3A'
text_color = '#FFFFFF'
ring_color = '#1a4a8a'
green      = '#00a65a'
yellow     = '#f39c12'
red        = '#e74c3c'

fig.patch.set_facecolor(bg_color)
ax.set_facecolor(bg_color)

cx, cy = 0, 0

radius_outer = 1.0
radius_inner = 0.88
width = radius_outer - radius_inner

radial_gap = 0.03
ring_outer = radius_outer + width + radial_gap

gap = 0.5
segments = [
    (50, 80,  green),
    (80, 120, yellow),
    (120, 150, red),
]

for v_start, v_end, color in segments:
    for v in range(v_start, v_end, 10):
        a1 = val_to_angle(v + 10)
        a2 = val_to_angle(v)
        w = Wedge((cx, cy), radius_outer, a1 + gap, a2 - gap,
                  width=width, facecolor=color, edgecolor='none')
        ax.add_patch(w)
        wr = Wedge((cx, cy), ring_outer, a1 + gap, a2 - gap,
                   width=width, facecolor=ring_color, edgecolor='none', zorder=2)
        ax.add_patch(wr)

a_50  = val_to_angle(50)
a_150 = val_to_angle(150)
w_gap = Wedge((cx, cy), ring_outer, a_50, a_150,
              width=width, facecolor=ring_color, edgecolor='none', zorder=2)
ax.add_patch(w_gap)

for val in range(50, 151, 10):
    angle = val_to_angle(val)
    rad = np.radians(angle)
    x_text = cx + (radius_inner - 0.13) * np.cos(rad)
    y_text = cy + (radius_inner - 0.13) * np.sin(rad)
    ax.text(x_text, y_text, str(val), color=text_color,
            fontproperties=f_label, ha='center', va='center')

pointer_angle = val_to_angle(pointer_val)
pointer_rad = np.radians(pointer_angle)
pointer_length = 0.72
px = cx + pointer_length * np.cos(pointer_rad)
py = cy + pointer_length * np.sin(pointer_rad)
ax.plot([cx, px], [cy, py], color=text_color, linewidth=2, zorder=5)

ax.text(cx, cy - 0.5, str(pointer_val), color=text_color,
        fontproperties=f_center, ha='center', va='center', zorder=5)

ax.set_xlim(-1.4, 1.4)
ax.set_ylim(-1.4, 1.4)
ax.axis('off')

fig.text(0.5, 0.95, '2022年6月29公司整体运营指数良好',
         ha='center', va='top', fontproperties=f_title, color=text_color)

plt.subplots_adjust(left=0.02, right=0.98, top=0.88, bottom=0.02)
plt.savefig('仪表盘.png', facecolor=bg_color, dpi=150)
print('saved 仪表盘.png')
