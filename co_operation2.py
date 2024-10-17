import math
import time
import os
import jieba  # 导入jieba库
import re  # 导入re模块以使用正则表达式
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import tkinter as tk
from tkinter import messagebox
import type_transfer

# 检查文件是否存在，如果不存在则创建
def ensure_file_exists(file_name):
    if not os.path.exists(file_name):
        with open(file_name, 'w', encoding='utf-8'):
            pass

def fetch_reviews_with_expand(movie_url, filename, number):
    file_name = 'movie_reviews/txt/' + filename
    driver = webdriver.Chrome()

    driver.get(movie_url)

    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "review-item"))
        )

        review_items = driver.find_elements(By.CLASS_NAME, "review-item")

        # 检查文件是否存在，如果不存在则创建
        ensure_file_exists(f"{file_name}.txt")

        with open(f"{file_name}.txt", 'r', encoding='utf-8') as file:
            existing_reviews = file.read()

        with open(f"{file_name}.txt", 'a', encoding='utf-8') as file:
            for index, review_item in enumerate(review_items, start=1):
                expand_button = review_item.find_element(By.XPATH, ".//a[@class='unfold']")
                if expand_button:
                    ActionChains(driver).move_to_element(expand_button).click().perform()
                    WebDriverWait(review_item, 10).until(
                        EC.invisibility_of_element_located((By.CLASS_NAME, "loading"))
                    )
                    time.sleep(1)
                    review_content = review_item.find_element(By.CLASS_NAME, "main-bd")
                    if review_content:
                        content_lines = review_content.text.split('\n')
                        cleaned_content = []
                        for line in content_lines:
                            if "回应" not in line and "有用" not in line and "没用" not in line and "APP" not in line and "收起" not in line:
                                cleaned_content.append(line)
                        multiline_content = '\n'.join(cleaned_content)
                        if f"评论 {index + number}:\n{multiline_content}\n{'-' * 50}\n\n" not in existing_reviews:
                            file.write(f"评论 {index + number}:\n{multiline_content}\n{'-' * 50}\n\n")

            # 进行分词处理
            tokenize_reviews(file_name)

            # 转换为JSON格式
            type_transfer.txt_to_json(f"{file_name}.txt", f"movie_reviews/json/{filename}.json")
    finally:
        driver.quit()

def tokenize_reviews(file_name):
    # 读取TXT文件
    input_file_path = f"{file_name}.txt"
    output_file_path = f"/home/hadoop/big-data/fenci/{os.path.basename(file_name)}.txt"
    
    with open(input_file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    # 使用jieba进行分词
    tokens = jieba.cut(content)

    # 过滤掉非汉字字符，只保留汉字
    filtered_tokens = [token for token in tokens if re.match(r'^[\u4e00-\u9fa5]+$', token)]

    # 将过滤后的分词结果连接成字符串
    tokenized_content = " ".join(filtered_tokens)

    # 将分词结果保存到指定目录
    ensure_file_exists(output_file_path)
    with open(output_file_path, 'w', encoding='utf-8') as file:
        file.write(tokenized_content)

movie_urls = {
    "肖申克的救赎": "https://movie.douban.com/subject/1292052/reviews",
    "霸王别姬": "https://movie.douban.com/subject/1291546/reviews",
    "阿甘正传": "https://movie.douban.com/subject/1292720/reviews",
    "泰坦尼克号": "https://movie.douban.com/subject/1292722/reviews",
    "千与千寻": "https://movie.douban.com/subject/1291561/reviews",
    "这个杀手不太冷": "https://movie.douban.com/subject/1295644/reviews",   
    "美丽人生": "https://movie.douban.com/subject/1292063/reviews",
    "星际穿越": "https://movie.douban.com/subject/1889243/reviews",
    "盗梦空间": "https://movie.douban.com/subject/3541415/reviews"
}

def fetch_reviews():
    # 获取输入框中的值
    movie_url = url_entry.get()
    file_name = name_entry.get()
    number = num_entry.get()

    # 检查输入是否为空
    if not movie_url or not file_name or not number:
        messagebox.showerror("错误", "所有的输入框都必须填写")
        return

    # 调用函数
    try:
        number = math.ceil(int(number) / 20) * 20  # 向上取整到最接近的20的整数倍
        for i in range(0, number, 20):
            fetch_reviews_with_expand(movie_url + f"?start={i}", file_name, i)
        messagebox.showinfo("成功", "成功获取评论！")
    except Exception as e:
        messagebox.showerror("错误", str(e))

# 关闭时退出进程
def on_closing():
    import os
    os._exit(0)

if __name__ == "__main__":
    # 创建一个新窗口
    root = tk.Tk()
    root.protocol("WM_DELETE_WINDOW", on_closing)  # 关闭时退出进程
    root.geometry("960x200")  # 设置窗口的大小为 960 宽 x 200 高

    # 创建标签和输入框
    url_label = tk.Label(root, text="电影网址")
    url_entry = tk.Entry(root, width=100)
    name_label = tk.Label(root, text="文件名")
    name_entry = tk.Entry(root, width=20)
    num_label = tk.Label(root, text="评论数量")
    num_entry = tk.Entry(root, width=5)

    # 创建一个按钮，点击时会调用fetch_reviews函数
    fetch_button = tk.Button(root, text="获取评论", command=fetch_reviews)

    # 将组件添加到窗口中
    url_label.pack()
    url_entry.pack()
    name_label.pack()
    name_entry.pack()
    num_label.pack()
    num_entry.pack()
    fetch_button.pack()

    # 运行窗口
    root.mainloop()

