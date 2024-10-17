import time
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

# 检查文件是否存在，如果不存在则创建
def ensure_file_exists(file_name):
    if not os.path.exists(file_name):
        with open(file_name, 'w', encoding='utf-8'):
            pass

def fetch_reviews_with_expand(movie_url, file_name, number):
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
                        if f"评论 {index+number}:\n{multiline_content}\n{'-' * 50}\n\n" not in existing_reviews:
                            file.write(f"评论 {index+number}:\n{multiline_content}\n{'-' * 50}\n\n")
    finally:
        driver.quit()

movie_urls = {
    "肖申克的救赎": "https://movie.douban.com/subject/1292052/reviews",
    "霸王别姬": "https://movie.douban.com/subject/1291546/reviews",
    "阿甘正传": "https://movie.douban.com/subject/1292720/reviews",
    "泰坦尼克号": "https://movie.douban.com/subject/1292722/reviews",
    "千与千寻": "https://movie.douban.com/subject/1291561/reviews",
    "这个杀手不太冷": "https://movie.douban.com/subject/1295644/reviews",
    "美丽人生": "https://movie.douban.com/subject/1292063/reviews",
    "星际穿越": "https://movie.douban.com/subject/1889243/reviews",
    "盗梦空间": "https://movie.douban.com/subject/3541415/reviews",
    "楚门的世界": "https://movie.douban.com/subject/3541415/reviews"
}

for movie, url in movie_urls.items():
    for number in range(0, 100, 20):
        fetch_reviews_with_expand(url+f"?start={number}", movie, number)

