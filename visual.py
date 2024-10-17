import os
import sys
import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter
from matplotlib.font_manager import FontProperties  # 导入 FontProperties

# 从命令行参数获取文件路径
if len(sys.argv) < 2:
    print("请提供文件路径作为参数.")
    sys.exit(1)

input_file_path = sys.argv[1]  # 获取命令行参数
sum_dir = '/home/hadoop/big-data/fenci/sum'
num_dir = '/home/hadoop/big-data/fenci/num'

# 确保输出目录存在
os.makedirs(sum_dir, exist_ok=True)
os.makedirs(num_dir, exist_ok=True)

# 检查输入文件是否存在
if not os.path.exists(input_file_path):
    print(f"文件 {input_file_path} 不存在！")
    sys.exit(1)

# 获取输入文件的前缀名
file_name_prefix = os.path.splitext(os.path.basename(input_file_path))[0]

# 读取文件
with open(input_file_path, 'r', encoding='utf-8') as file:
    text = file.read()

# 分词（假设按空格分词，若需要使用中文分词，可使用jieba等库）
words = text.split()  # 这里可以替换为更合适的中文分词方法

# 统计词频
word_counts = Counter(words)

# 将结果转换为DataFrame
df = pd.DataFrame(word_counts.items(), columns=['Word', 'Frequency'])

# 按频率排序
df_sorted = df.sort_values(by='Frequency', ascending=False)

# 保存统计结果到num文件，包含词和频率
num_file_path = os.path.join(num_dir, f'{file_name_prefix}.csv')
df_sorted.to_csv(num_file_path, index=False)

# 获取前5个词及其频率
top_5 = df_sorted.head(5)

# 设置中文字体，确保支持中文字符的字体可用
font_path = 'SimHei.ttf'  
font_prop = FontProperties(fname=font_path)

plt.rcParams['font.family'] = font_prop.get_name()
plt.rcParams['axes.unicode_minus'] = False

import matplotlib.pyplot as plt

# 创建一个圆环图
import matplotlib.pyplot as plt
plt.figure(figsize=(8, 8))
plt.pie(top_5['Frequency'], radius=0.7, labels=top_5['Word'], startangle=90, counterclock=False, 
        autopct='%1.1f%%', wedgeprops=dict(edgecolor='w'))
plt.pie(top_5['Frequency'], radius=1, startangle=90, counterclock=False, 
        wedgeprops=dict(edgecolor='w', linewidth=2))
plt.title(f'Top 5 Words in Circular Diagram ({file_name_prefix})', fontproperties=font_prop)
plt.axis('equal')
plt.savefig(os.path.join(sum_dir, f'{file_name_prefix}_circular_diagram.png'))
plt.show()
plt.close()

# 绘制并显示柱状图
plt.figure(figsize=(10, 6))
plt.bar(top_5['Word'], top_5['Frequency'], color='skyblue')
plt.title(f'Top 5 Words - Bar Chart ({file_name_prefix})', fontproperties=font_prop)  # 使用 fontproperties
plt.xlabel('Words', fontproperties=font_prop)
plt.ylabel('Frequency', fontproperties=font_prop)
plt.xticks(rotation=45)  # 使x轴的标签倾斜，避免重叠
plt.savefig(os.path.join(sum_dir, f'{file_name_prefix}_bar_chart.png'))
plt.show()  # 显示图像
plt.close()  # 关闭当前图像，以释放内存

# 绘制并显示折线图
plt.figure(figsize=(10, 6))
plt.plot(top_5['Word'], top_5['Frequency'], marker='o')
plt.title(f'Top 5 Words - Line Chart ({file_name_prefix})', fontproperties=font_prop)  # 使用 fontproperties
plt.xlabel('Words', fontproperties=font_prop)
plt.ylabel('Frequency', fontproperties=font_prop)
plt.grid()
plt.xticks(rotation=45)  # 使x轴的标签倾斜，避免重叠
plt.savefig(os.path.join(sum_dir, f'{file_name_prefix}_line_chart.png'))
plt.show()  # 显示图像
plt.close()  # 关闭当前图像，以释放内存

# 绘制并显示饼图
plt.figure(figsize=(8, 8))
plt.pie(top_5['Frequency'], labels=top_5['Word'], startangle=90, counterclock=False, autopct='%1.1f%%', wedgeprops=dict(edgecolor='w'))
plt.title(f'Top 5 Words - Pie Chart ({file_name_prefix})', fontproperties=font_prop)  # 使用 fontproperties
plt.axis('equal')
plt.savefig(os.path.join(sum_dir, f'{file_name_prefix}_pie_chart.png'))
plt.show()  # 显示图像
plt.close()  # 关闭当前图像，以释放内存

# 绘制并显示南丁格尔图
plt.figure(figsize=(8, 8))
radii = top_5['Frequency']
theta = [i * (360 / len(top_5)) for i in range(len(top_5))]
plt.subplot(projection='polar')
plt.bar(theta, radii, width=0.3, bottom=0.0, color='skyblue')
plt.title(f'Top 5 Words - Nightingale Rose Chart ({file_name_prefix})', fontproperties=font_prop)  # 使用 fontproperties
plt.savefig(os.path.join(sum_dir, f'{file_name_prefix}_nightingale_chart.png'))
plt.show()  # 显示图像
plt.close()  # 关闭当前图像，以释放内存

