import os
import jieba.analyse
import matplotlib.pyplot as plt
from wordcloud import WordCloud

# 读取影评文件
def read_reviews(file_path):
    if not os.path.isfile(file_path):
        raise FileNotFoundError(f"文件路径 '{file_path}' 不存在或不可读。")
    
    with open(file_path, 'r', encoding='utf-8') as file:
        reviews = file.read()
    
    if not reviews:
        raise ValueError("评论文件为空，请确保文件中包含有效的评论。")
    
    return reviews

# 提取角色和脉络相关的关键词和短语
def extract_keywords(reviews):
    # 使用jieba的关键词提取功能
    keywords = jieba.analyse.extract_tags(reviews, topK=100, withWeight=True, allowPOS=('nr', 'ns', 'nt', 'n', 'vn'))
    return keywords

# 生成词云图
def generate_wordcloud(keywords):
    if not keywords:
        raise ValueError("关键词列表为空，无法生成词云图。")
    
    font_path = 'SimHei.ttf'
    if not os.path.isfile(font_path):
        raise FileNotFoundError(f"字体文件 '{font_path}' 不存在。请确保它在当前目录中。")
    
    wordcloud = WordCloud(font_path=font_path,
                          background_color='white',
                          width=1000,
                          height=800,
                          max_font_size=200).generate_from_frequencies(dict(keywords))
    
    plt.figure(figsize=(12, 10))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.show()

# 分析电影评论并生成词云
def analyze_movie_reviews(file_path):
    # 读取评论
    reviews = read_reviews(file_path)
    
    # 提取角色和脉络相关的关键词和短语
    keywords = extract_keywords(reviews)
    
    # 生成词云图
    generate_wordcloud(keywords)

if __name__ == '__main__':
    file_path = input("请输入电影评论文件路径：")
    
    # 分析电影评论并生成词云
    try:
        analyze_movie_reviews('movie_reviews/txt/' + file_path)
    except Exception as e:
        print(f"错误: {e}")

