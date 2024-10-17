from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

def extractive_summary(text, num_sentences=3):
    sentences = text.split('。')
    sentences = [s.strip() for s in sentences if s]

    # 使用TF-IDF计算每个句子的权重
    vectorizer = TfidfVectorizer()
    X = vectorizer.fit_transform(sentences)
    scores = cosine_similarity(X).sum(axis=1)

    # 按权重排序并选取前几个句子
    ranked_sentences = [sentences[i] for i in np.argsort(scores, axis=0)[-num_sentences:]]
    
    return '。'.join(sorted(ranked_sentences, key=lambda x: sentences.index(x)))

# 将 extractive_summary 函数与 summarize_text 函数结合
def chinese_text_summarization(text, num_sentences=3):
    return extractive_summary(text, num_sentences)

# 其他部分保持不变

