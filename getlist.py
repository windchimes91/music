import pytube
from tkinter import *
from pytube import YouTube
from moviepy.editor import VideoFileClip
from tkinter import filedialog
import eyed3

fail = []

def loadVideo():
    vlinks = links.get()
    yt = pytube.Playlist(vlinks)
    count = yt.length
    for video in yt:
        yt = YouTube(video)
        vname = yt.title
        print("影片標題：",vname)
        count -= 1
        print("影片剩餘數量：",count)
        try:
            yt.streams.filter(subtype="mp4").first().download(output_path=path,filename=vname + '.mp4')
            au = yt.author
            input_file = vname + '.mp4'
            output_file = vname + '.mp3'

            convert_video_to_audio(input_file, output_file,au)
        except:
            print('下載失敗')
            fail.append(vname)
        
    x.set("影音檔按下在完成( •̀ ω •́ )✧")
    print('下載失敗歌曲：')
    for i in range(len(fail)):
        print(fail[i])

def convert_video_to_audio(input_file, output_file,au):
    input_file = path +'/'+ input_file
    output_file = path + '/' + output_file
    # 加載影片
    video_clip = VideoFileClip(input_file)
    
    # 提取音訊部分
    audio_clip = video_clip.audio
    
    # 儲存音訊檔
    audio_clip.write_audiofile(output_file, codec='mp3')
    
    # 釋放資源
    audio_clip.close()

    editauthor(output_file,au)

def reset():
    links.set("")
    x.set("請輸入網址ヾ(•ω•`)o")

def filepathset():
    global path
    pathset = filedialog.askdirectory()
    file_path.set(pathset)
    path = pathset

def editauthor(output_file,au):
    audio_file = eyed3.load(output_file)
    audio_file.tag.artist = au
    audio_file.tag.save()


window = Tk()
window.title("抓歌（清單）")

x = StringVar()
links = StringVar()
file_path = StringVar()
x.set("請輸入網址(╯▽╰ )")
file_path.set(".\\download")

label1 = Label(window,text="請輸入網址：").grid(row=0)
label2 = Label(window,text="請輸入儲存的資料夾：").grid(row=2)
label3 = Label(window,textvariable=x,height=3).grid(row=3,column=0,columnspan=2)

e1 = Entry(window,textvariable=links)
e3 = Entry(window,textvariable=file_path)
e1.grid(row=0,column=1)
e3.grid(row=2,column=1)

btn1 = Button(window,text="下載",command=loadVideo)
btn1.grid(row=4,column=0)
btn2 = Button(window,text="Reset",command=reset)
btn2.grid(row=4,column=1)
btn3 = Button(window,text="結束",command=window.destroy)
btn3.grid(row=4,column=2)

filepathbutton = Button(window, text = "更改下載目錄", width = 15, command = filepathset)
filepathbutton.grid(row=2,column=2)


window.mainloop()

