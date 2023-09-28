# -*- coding: utf-8 -*-
"""
Created on Sat Mar 27 12:51:32 2021

@author: DELL
"""

from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from pytube import YouTube  # pip install pytube3
from tkinter import messagebox
from googleapiclient.discovery import build

Folder_Name = ""


# file location
def openLocation():
    global Folder_Name
    Folder_Name = filedialog.askdirectory()
    if len(Folder_Name) > 1:
        locationError.config(text=Folder_Name, fg="green")
    else:
        locationError.config(text="Please Choose Folder!!", fg="red")


# donwload video
def DownloadVideo():
    choice = ytdchoices.get()
    url = ytdEntry.get()
    try:
        if len(url) > 1:
            ytdError.config(text="")
            yt = YouTube(url)

            if choice == choices[0]:
                select = yt.streams.get_highest_resolution()

            elif choice == choices[1]:
                select = yt.streams.filter(progressive=True, file_extension='mp4').last()

            elif choice == choices[2]:
                select = yt.streams.filter(only_audio=True).first()
            else:
                ytdError.config(text="Paste Link again!!", fg='white', bg='#262626')
    except:
        print("Something went wrong")

    ok = messagebox.askquestion("Dailog Box", "Do You want to Download the Video?")
    if ok == "yes":
        # download function
        select.download(Folder_Name)

        ytdError.config(text="Download Completed!!")


# detail of video and channel

def video_details():
    video_id = ytdEntry.get()[len("https://www.youtube.com/watch?v="):]
    youtube = build('youtube', 'v3', developerKey='AIzaSyDHACxLdXroyhQj7T0NewzYbwa15Y-PNf8')

    data_video = youtube.videos().list(part='snippet,statistics', id=video_id).execute()
    # print(data_video)

    channelID = data_video['items'][0]['snippet']['channelId']
    title = data_video['items'][0]['snippet']['title']
    likes = data_video['items'][0]['statistics']['likeCount']
    views = data_video['items'][0]['statistics']['viewCount']
    channelTitle = data_video['items'][0]['snippet']['channelTitle']

    data_channel = youtube.channels().list(part='statistics', id=channelID).execute()

    t_video = data_channel['items'][0]['statistics']['videoCount']
    t_sub = data_channel['items'][0]['statistics']['subscriberCount']
    t_watch = data_channel['items'][0]['statistics']['viewCount']

    details.config(width=75, bg="#2b2e4a", fg="white",
                   text=f"Channel Title :- {channelTitle}\nTotal video on channel :- {t_video}\nTotal Subs :-{t_sub}\nTotal Watch time :-{t_watch}\n\nVideo title:- {title}\nLikes:- {likes}\nViews:- {views}")


root = Tk()
# Youtbe Icon in dialogn box
winicon = PhotoImage(file='Youtube-icon.png')
root.iconphoto(False, winicon)

# Background Color
# 2F2F2F Light black
# 010B13 Dark Black
root.configure(bg='#ead3cb')

# Dialoag Title
root.title("YTD Downloader")
root.geometry("450x600")  # set window

# Maximize or Minimize off
# root.resizable(width=0,height=0)

root.columnconfigure(0, weight=1)  # set all content in center.

# developer Label
developerlabel = Label(root, text="YOUTUBE VIDEO DOWNLOADER", bg='#d44000', fg='white', font=("jost", 20), width="30",
                       borderwidth=10, padx=10, pady=10)
developerlabel.grid(padx=10, pady=10)

# Ytd Link Label
ytdLabel = Label(root, bg='#262626', fg='white', text="Enter the URL of the Video", font=("jost", 15))
ytdLabel.grid(padx=10, pady=10)

# Entry Box
ytdEntryVar = StringVar()
ytdEntry = Entry(root, width=50, bd=2, font=14, bg="#ddd", borderwidth=0, textvariable=ytdEntryVar)
ytdEntry.grid(padx=10, pady=10)

# Error Msg
ytdError = Label(root, bg='#262626', text="url box is empty", fg='white', font=("jost", 15))
ytdError.grid(padx=10, pady=10)

# Asking save file label
# saveLabel = Label(root,text="Save the Video File",font=("jost",15,"bold"))
# saveLabel.grid(padx=10,pady=10)

# btn of save file
saveEntry = Button(root, width=10, bg="red", fg="white", padx=5, pady=5, border="0", text="Choose Path",
                   command=openLocation)
saveEntry.grid(padx=10, pady=10)

# Error Msg location
locationError = Label(root, text="Path is not selected", padx=10, pady=10, fg="red", font=("jost", 12))
locationError.grid(padx=10, pady=10)

# Download Quality
ytdQuality = Label(root, bg='#262626', padx=5, pady=5, fg='white', text="Select Quality", font=("jost", 15))
ytdQuality.grid(padx=10, pady=10)

# combobox
choices = ["720p", "144p", "Only Audio"]
ytdchoices = ttk.Combobox(root, values=choices)
ytdchoices.grid(padx=10, pady=10, )

# donwload btn
downloadbtn = Button(root, text="Donwload", border="0", padx=5, pady=5, width=10, bg="red", fg="white",
                     command=DownloadVideo)
downloadbtn.grid(padx=10, pady=10)

# get video detail using API

# videodetail = Label(root,bg='gray',text="",fg='black',font=("jost",15),width="30",borderwidth=10,padx=10,pady=10)
# videodetail.grid(padx=10,pady=10)

Button(root, text="Video Details", width=15, font=("jost", 15), bg="orange", border="0", fg="black",
       command=video_details, padx=10, pady=10).grid()

details = Label(root)
details.grid(padx=5, pady=5)

root.mainloop()