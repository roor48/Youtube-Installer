from yt_dlp import YoutubeDL
from cli_to_api import cli_to_api
from tkinter import Tk, Label, Entry, Button, OptionMenu, StringVar, filedialog
from threading import Thread

def download_video(video_url: str):
    video_url = video_url.strip()
    ydl_opts = cli_to_api([
        f'-f bestvideo[height<={quality.get()[:-1]}][ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
        '-o %(title)s.%(ext)s',
        f'-P {location}'
    ])

    with YoutubeDL(ydl_opts) as ydl:
        Thread(target=ydl.download, args=([video_url])).start()


root = Tk()
root.title("YouTube Downloader")
root.geometry("400x200")

# 유튜브 주소 입력
label = Label(root, text="Enter YouTube Video URL")
label.pack()

text_entry = Entry(root, width=50)
text_entry.pack()


# 설치 경로 선택
def set_location():
    global location
    select = filedialog.askdirectory(title="설치 경로 선택", initialdir=location)
    if select:
        location = select
        location_label.config(text=location)
location = "./downloads"  # Default download location

location_label = Label(root, text=f"{location}")
location_label.pack()

location_btn = Button(root, text="설치 경로 선택", command=set_location)
location_btn.pack()


# 화질 선택
OPTIONS = [
"2160p",
"1440p",
"1080p",
"720p",
"480p",
"360p",
"240p",
"144p"
]
quality = StringVar(root)
quality.set(OPTIONS[0])  # default value

qualityMenu = OptionMenu(root, quality, *OPTIONS)
qualityMenu.pack(pady=10)


# 다운로드 버튼
url_button = Button(root, text="Download Video", command=lambda: download_video(text_entry.get()))
url_button.pack()

root.mainloop()
