import jieba
import jieba.posseg as pseg
from collections import Counter
from textblob import TextBlob
import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

#读电影评论文件，分词
def read_file_and_segment(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        text=file.read()
        segments=jieba.cut(text)
        return list(segments)

#词性标注
def word_tag(text):
    words=pseg.cut(text)
    return [(word.word, word.flag) for word in words]

#字频统计
def word_frequency(words):
    word_counts=Counter(words)
    return word_counts

#命名实体识别
def entity_recognize(text):
    words=pseg.cut(text)
    named_entities=[]
    for word, flag in words:
        if flag.startswith('nr'):
            named_entities.append(word)
    return named_entities

#情感分析
def setiment_analyze(text):
    custom_categories={
        "开心":['喜欢', '有意思', '惊喜', '开心'],
        "生气":['失望', '不喜欢', '难看', '评分虚高','虚假'],
        "平和":['一般', '随便','可看可不看','无所谓'],
        "惊讶":['出乎意料', '意外','惊讶'],
        "疑惑":['困惑', '迷惑','不解']
    }
    blob=TextBlob(text)
    category_counts={catogory:sum(text.count(word) for word in words) for catogory, words in custom_categories.items()}
    total_words=len(blob.words)
    category_percentages={category:(count/total_words)*100 for category, count in category_counts.items()}
    total_percentage=sum(category_percentages.values())
    normalized_percentages={category:(percentage/total_percentage)*100 for category, percentage in category_percentages.items()}
    return normalized_percentages

#情感分析结果写入单独文件
def write_setiment_result(category_percentages, file_path):
    with open (file_path, "w", encoding="utf-8") as result_file:
        for category, percentage in category_percentages.items():
            result_file.write(f"{category}{percentage:.2f}%\n")

#情感分析结果可视化
def graph_setiment(category_percentages, file_path):
    categories = list(category_percentages.keys())
    percentages = list(category_percentages.values())
    plt.figure(figsize=(8, 6))
    plt.pie(percentages, labels=categories, autopct='%1.1f%%')
    plt.title('情感分析结果')
    plt.savefig(file_path)
    plt.show()
    plt.close()


# if __name__=="__main__":
#     file_paths=["阿甘正传.txt", "霸王别姬.txt", "楚门的世界.txt", "盗梦空间.txt", "美丽人生.txt", "千与千寻.txt", "泰坦尼克号.txt", "肖申克的救赎.txt", "星际穿越.txt", "这个杀手不太冷.txt"]
#     with open("电影评论分析结果.txt", "w", encoding="utf-8") as result_file:
#        for file_path in file_paths:
#            result_file.write(f"分析文件:{file_path}\n")
#            words=read_file_and_segment(file_path)
#            tagged_words=word_tag(''.join(words))
#            word_counts=word_frequency(words)
#            named_entities=entity_recognize(''.join(words))
#            category_percentages=setiment_analyze(''.join(words))
#            result_file.write(f"词性标注：{tagged_words}\n")
#            result_file.write(f"字频统计：{word_counts}\n")
#            result_file.write(f"命名实体：{named_entities}\n")
#            for category, percentage in category_percentages.items():
#                result_file.write(f"{category} {percentage:.2f}%\n")
#            result_file.write("\n")
#     print("写入完成！")

def analyze_files(file_path, result_file_path):
    with open('output/sentiment_analysis/'+result_file_path, "w", encoding="utf-8") as result_file:
        result_file.write(f"分析文件:{file_path}\n")
        words=read_file_and_segment('movie_reviews/txt/' + file_path)
        tagged_words=word_tag(''.join(words))
        word_counts=word_frequency(words)
        named_entities=entity_recognize(''.join(words))
        category_percentages=setiment_analyze(''.join(words))
        result_file.write(f"词性标注：{tagged_words}\n")
        result_file.write(f"字频统计：{word_counts}\n")
        result_file.write(f"命名实体：{named_entities}\n")
        for category, percentage in category_percentages.items():
            result_file.write(f"{category} {percentage:.2f}%\n")
        result_file.write("\n")
        sentiment_result_file = f"output/sentiment_analysis/{file_path.split('.')[0]}_情感分析.txt"
        write_setiment_result(category_percentages, sentiment_result_file)

        sentiment_plot_file = f"output/sentiment_analysis/{file_path.split('.')[0]}_情感分析可视化.png"
        graph_setiment(category_percentages, sentiment_plot_file)

if __name__ == "__main__":
    file_paths = input("请输入文件名，使用逗号分隔：").split(',')
    result_file_path = input("请输入结果文件名：")
    for file_path in file_paths:
        analyze_files(file_path, result_file_path)
    print("写入完成！")
