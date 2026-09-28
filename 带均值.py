# -*- coding: utf-8 -*-
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties

# 字体定义
f_title  = FontProperties(family='Microsoft YaHei', size=20, weight='bold')
f_sub    = FontProperties(family='Microsoft YaHei', size=14, weight='normal')
f_dlabel = FontProperties(family='Calibri', size=10)             # 数据标签(数字)
f_xlabel = FontProperties(family='Microsoft YaHei', size=9)      # 横轴(中文)
f_avg    = FontProperties(family='Microsoft YaHei', size=8)      # 平均值
f_note   = FontProperties(family='Microsoft YaHei', size=9)      # 脚注

# 数据
regions = ['华北', '华南', '东北', '西北', '西南', '华东']
values  = [2354, 1902, 3524, 2698, 2896, 2563]
avg_val = 2656

# 尺寸 14.68cm x 10.47cm
fig_w = 14.68 / 2.54
fig_h = 10.47 / 2.54
fig, ax = plt.subplots(figsize=(fig_w, fig_h), dpi=150)

# 颜色
bg_color   = '#1A1F3A'   # 深蓝背景
bar_color  = '#0070C0'   # 标准蓝
text_color = '#FFFFFF'   # 白色
avg_color  = '#F5A623'   # 偏橙
fig.patch.set_facecolor(bg_color)
ax.set_facecolor(bg_color)

# 间隙宽度219% => 柱宽 = 1/(1+2.19)
bar_w = 1 / (1 + 2.19)

# 柱状图
x_pos = list(range(len(regions)))
ax.bar(x_pos, values, width=bar_w, color=bar_color, zorder=3)

# 数据标签（柱顶，白色）
for x, v in zip(x_pos, values):
    ax.text(x, v + 70, f'{v}', ha='center', va='bottom',
            fontproperties=f_dlabel, color=text_color, zorder=5)

# 平均值线（从第一柱中心到末柱中心）
ax.plot([0, len(regions) - 1], [avg_val, avg_val],
        color=avg_color, linewidth=1.4, zorder=4)
ax.text(4.0, 2780, '平均值：2656', ha='left', va='bottom',
        fontproperties=f_avg, color=avg_color, zorder=6)

# 横轴区域名称（微软雅黑，白色）
ax.set_xticks(x_pos)
ax.set_xticklabels(regions, fontproperties=f_xlabel, color=text_color)

# 纵轴数值不显示
ax.set_ylim(0, 4000)
ax.set_yticks([])
ax.set_xlim(-0.5, len(regions) - 0.5)

# 轴线：仅保留底部横轴线（浅灰蓝）
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_visible(False)
ax.spines['bottom'].set_visible(True)
ax.spines['bottom'].set_color('#8896AA')
ax.spines['bottom'].set_linewidth(0.8)
ax.tick_params(axis='both', length=0, pad=6)

# 主标题（左对齐，加粗，白色）
ax.set_title('3 月各区域销量分布', loc='left', pad=22,
             fontproperties=f_title, color=text_color)
# 副标题（不加粗，白色，与标题间距增大）
fig.text(0.062, 0.825, '东北销量最多占总销量的 22%，华南销量最低',
         ha='left', va='top', fontproperties=f_sub, color=text_color)

# 底部脚注（白色）
fig.text(0.062, 0.035, '注：数据来源于公司销售系统，统计日期截至 2022.03.31',
         ha='left', va='bottom', fontproperties=f_note, color=text_color)

plt.subplots_adjust(left=0.06, right=0.97, top=0.78, bottom=0.18)
plt.savefig('带均值.png', facecolor=bg_color, dpi=150)
print('saved 带均值.png')
