from yt_dlp import YoutubeDL
from cli_to_api import cli_to_api
from tkinter import Tk, Label, Entry, Button, OptionMenu, StringVar, filedialog, DoubleVar, ttk, messagebox
from threading import Thread

def download_video(video_url: str):
    global totalVideoCount, downloadedCount

    try:
        video_url = video_url.strip()
        ydl_opts = cli_to_api([
            '-f', f'bestvideo[height<={quality.get()[:-1]}][ext=mp4]/bestvideo[height<={quality.get()[:-1]}]+bestaudio[ext=mp4]/bestaudio[ext=m4a]/bestaudio',
            '-o', '%(title)s.%(ext)s',
            '-P', location,
            '--merge-output-format', 'mp4'
        ])
        ydl_opts['progress_hooks'] = (progress_hook,)


        with YoutubeDL({'quiet': True}) as ydl:
            info_dict = ydl.extract_info(video_url, download=False)  # 다운로드 없이 정보만 가져오기
            if 'entries' in info_dict:
                totalVideoCount = len(info_dict['entries'])  # 재생목록 영상 수
            else:
                totalVideoCount = 1  # 단일 영상인 경우
            downloadedCount = 0

        with YoutubeDL(ydl_opts) as ydl:
            ydl.download((video_url,))

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")
        videoProgress.set(0)
        totalProgress.set(0)

def progress_hook(d):
    global downloadedCount

    if d['status'] == 'downloading':
        percent = d.get('_percent', 0.0)

        if ( (videoProgress.get() >= 100) or (percent > videoProgress.get()) ):
            videoProgress.set(percent)

    elif d['status'] == 'finished':
        videoProgress.set(0)
        downloadedCount += 1

    totalProgress.set(downloadedCount / totalVideoCount * 100)
    if downloadedCount == totalVideoCount:
        videoProgress.set(100)
        totalProgress.set(100)


# GUI 설정
root = Tk()
root.title("YouTube Downloader")
root.resizable(False, False)


# 유튜브 주소 입력
label = Label(root, text="Enter YouTube Video URL")
label.pack()

text_entry = Entry(root, width=50)
text_entry.pack()


# 설치 경로 선택
def set_location():
    global location
    select = filedialog.askdirectory(title="Select Directory", initialdir=location)
    if select:
        location = select
        location_label.config(text=location)
location = "./downloads"  # Default download location

location_label = Label(root, text=f"{location}")
location_label.pack()

location_btn = Button(root, text="Select Directory", command=set_location)
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
url_button = Button(root, text="Download", command=lambda: Thread(target=download_video, args=(text_entry.get(),)).start())
url_button.pack()


# 개별 진행도 바
videoProgress = DoubleVar()
videoProgressBar = ttk.Progressbar(root, style="custom.Horizontal.TProgressbar", maximum=100, variable=videoProgress, length=400)
videoProgressBar.pack(pady=(10, 0))

# 전체 진행도 바
totalProgress = DoubleVar()
totalProgressBar = ttk.Progressbar(root, style="custom.Horizontal.TProgressbar", maximum=100, variable=totalProgress, length=400)
totalProgressBar.pack()

# 다운로드 진행도
totalVideoCount = 0
downloadedCount = 0


# 각 요소 스타일 지정
style = ttk.Style()
style.theme_use('default')
style.configure("custom.Horizontal.TProgressbar", thickness=7)  # 원하는 두께


# 모든 위젯 배치 후 화면 업데이트
root.update_idletasks()
# 최소 크기를 현재 내용물 크기에 맞춤
root.minsize(root.winfo_width(), root.winfo_height())

root.mainloop()