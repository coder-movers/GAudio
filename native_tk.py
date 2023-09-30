import tkinter as tk
from tkinter import filedialog
from tkinter import ttk

from dotenv import load_dotenv
import json
import os

from service.SAMIService import SAMIService

root = tk.Tk()
root.title("HS_Audio")
root.geometry("550x450+630+300")

_ = load_dotenv()

audio_input_folder_path = ''

audio_input_folder_text = tk.StringVar()
audio_input_folder_text.set("请选择音频文件夹...")


def select_audio_input_folder():
    global audio_input_folder_path
    folder_path = filedialog.askdirectory()

    if folder_path:
        audio_input_folder_path = folder_path
        audio_input_folder_text.set(folder_path)


audio_input_folder_label = tk.Label(root, textvariable=audio_input_folder_text)
audio_input_folder_label.pack(pady=20)

audio_input_folder_btn = tk.Button(root, text="选择音频文件夹", command=select_audio_input_folder)
audio_input_folder_btn.pack(pady=20)

# 配置参数


# 注意事项
tree = ttk.Treeview(root, show="headings", height=6)
style = ttk.Style()
style.configure('Treeview', rowheight=40)
tree.pack()

tree["columns"] = ("one", "two", "three")

# 设置列属性
tree.column("one", width=50, anchor="w")
tree.column("two", width=80, anchor="w")
tree.column("three", width=320, anchor="w")

# 设置表头
tree.heading("one", text="注意项")
tree.heading("two", text="")
tree.heading("three", text="说明")

# 添加数据
tree.insert("", 0, values=(
    "功能", "限制说明", "不支持非音乐类音频;避免直接拼接json文本,\n尽量使用转换库,避免造成转义符等导致json格式错误"))
tree.insert("", 1, values=("", "音频格式支持", "wav、pcm、mp3、aac等常见格式"))
tree.insert("", 2, values=(
    "输入", "音频编码建议", "采样率大于等于44.1kHz、双声道,\n否则将进行自动转码,可能带来效果损失和更多耗时处理",))
tree.insert("", 3, values=("", "音频时长限制", "小于等于10分钟;建议大于5s,否则会影响算法效果",))
tree.insert("", 4, values=("", "音频大小限制", "小于等于100MB",))
tree.insert("", 5, iid="row5",
            values=("输出", "结果格式", "默认返回44.1kHz、单通道wav格式音频。\n支持用户配置指定输出音频编码格式。"))


def check_token_empty(file, key):
    if not os.path.isfile(file):
        return False

    with open(file, 'r', encoding='utf-8') as f:
        data = json.load(f)
        return key in data


def get_token():
    sami_service = SAMIService()
    sami_service.set_ak(os.getenv('ACCESS_KEY'))
    sami_service.set_sk(os.getenv('SECRET_KEY'))

    req = {"appkey": os.getenv('APPKEY'), "token_version": os.getenv('AUTH_VERSION'), "expiration": 3600}
    resp = sami_service.common_json_handler("GetToken", req)
    with open('token.txt', 'w', encoding='utf-8') as f:
        f.write(resp)


root.mainloop()
