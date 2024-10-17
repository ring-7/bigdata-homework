import os
import sys
import tkinter as tk
from tkinter import messagebox
import co_operation2
import wordCloud
import threading
import subprocess

def run_co_operation2():
    python_path = sys.executable
    subprocess.run([python_path, '/home/hadoop/big-data/co_operation2.py'])

def run_co_operation2_in_thread():
    threading.Thread(target=run_co_operation2).start()

def run_analyze_movie_reviews_in_thread():
    name = selected_file.get()
    threading.Thread(target=lambda: wordCloud.analyze_movie_reviews('/home/hadoop/big-data/movie_reviews/txt/' + name)).start()

def run_visualization_in_thread():
    name = selected_file.get()
    input_file_path = f'/home/hadoop/big-data/fenci/{name}'
    threading.Thread(target=lambda: subprocess.run([sys.executable, '/home/hadoop/big-data/visual.py', input_file_path])).start()

def upload_segmentation():
    text_box.delete(1.0, tk.END)
    segmentation_file = '/home/hadoop/big-data/fenci/' + selected_file.get()
    if os.path.exists(segmentation_file):
        with open(segmentation_file, 'r', encoding='utf-8') as file:
            file_content = file.read()
            text_box.insert(tk.END, file_content)
    else:
        messagebox.showerror("错误", f"文件 {segmentation_file} 不存在！")

def refresh_files():
    path = '/home/hadoop/big-data/movie_reviews/txt/'
    files = os.listdir(path)
    menu = dropdown['menu']
    menu.delete(0, 'end')
    for file in files:
        menu.add_command(label=file, command=tk._setit(selected_file, file))

def on_option_change(*args):
    read_file()

def read_file():
    text_box.delete(1.0, tk.END)
    with open('/home/hadoop/big-data/movie_reviews/txt/' + selected_file.get(), 'r', encoding='utf-8') as file:
        file_content = file.read()
    text_box.insert(tk.END, file_content)

def show_word_frequency():
    text_box.delete(1.0, tk.END)
    # 获取选中文件的前缀
    file_prefix = selected_file.get().split('.')[0]
    frequency_file_path = f'/home/hadoop/big-data/fenci/num/{file_prefix}.csv'
    
    if os.path.exists(frequency_file_path):
        with open(frequency_file_path, 'r', encoding='utf-8') as file:
            file_content = file.read()
            text_box.insert(tk.END, file_content)
    else:
        messagebox.showerror("错误", f"文件 {frequency_file_path} 不存在！")

def on_closing():
    import os
    os._exit(0)

# 创建一个新窗口
root = tk.Tk()
root.protocol("WM_DELETE_WINDOW", on_closing)
root.geometry("1280x720")

# 创建 Frame
left_frame = tk.Frame(root, bg='white')
right_frame = tk.Frame(root, bg='grey')

# 使用 grid 几何管理器来布局框架
left_frame.grid(row=0, column=0, sticky='nsew')
right_frame.grid(row=0, column=1, sticky='nsew')

# 设置行和列的权重
root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=4)
root.grid_columnconfigure(1, weight=1)

# 在左侧框架的顶部添加下拉框
selected_file_label = tk.Label(left_frame, text="选择电影")
selected_file = tk.StringVar()
selected_file.trace('w', on_option_change)
dropdown = tk.OptionMenu(left_frame, selected_file, " ")
dropdown.config(width=20)
dropdown = tk.OptionMenu(left_frame, selected_file, " ", command=on_option_change)
selected_file_label.pack(side='top', padx=(10, 10), pady=(20, 0))
dropdown.pack(side='top', padx=(10, 10), pady=(0, 20))

# 在左侧框架添加文本框
text_box = tk.Text(left_frame)
text_box.place(relx=0.5, rely=0.3, relwidth=0.9, relheight=0.4, anchor='center')

# 添加滚动条
scrollbar = tk.Scrollbar(text_box)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

# 配置文本框和滚动条
text_box.config(yscrollcommand=scrollbar.set)
scrollbar.config(command=text_box.yview)

# 在右侧框架添加按钮
refresh_button = tk.Button(right_frame, text="刷新列表", command=refresh_files)
refresh_button.pack(side='top', padx=(10, 10), pady=(20, 0))

run_button = tk.Button(right_frame, text="爬取文件", command=run_co_operation2_in_thread)
run_button.pack(side='top', pady=(5, 0))

wordcloud_button = tk.Button(right_frame, text="生成词云", command=run_analyze_movie_reviews_in_thread)
wordcloud_button.pack(side='top', pady=(5, 0))

upload_button = tk.Button(right_frame, text="分词上传", command=upload_segmentation)
upload_button.pack(side='top', pady=(5, 0))

visualization_button = tk.Button(right_frame, text="可视化", command=run_visualization_in_thread)
visualization_button.pack(side='top', pady=(5, 0))

# 添加“词频排序”按钮
word_frequency_button = tk.Button(right_frame, text="词频排序", command=show_word_frequency)
word_frequency_button.pack(side='top', pady=(5, 0))

# 运行窗口
refresh_files()
root.mainloop()

