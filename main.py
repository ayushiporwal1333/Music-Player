import os
from tkinter import *
from tkinter import filedialog
from tkinter import ttk
from ttkthemes import themed_tk as tk
import tkinter.messagebox
from mutagen.mp3 import MP3
from pygame import mixer
import time
import threading

root = tk.ThemedTk()
root.get_themes()
root.set_theme("radiance")

menubar = Menu(root)
root.config(menu=menubar)

statusbar = ttk.Label(root, text="Welcome to Sa Re Ga Ma", relief=SUNKEN, anchor=W, font='Verdana 10 italic')
statusbar.pack(side=BOTTOM, fill=X)

def browse_files():
    global filename_path
    filename_path = filedialog.askopenfilename()
    add_to_playlist(filename_path)

playlist = []

def add_to_playlist(filename):
    filename= os.path.basename(filename)
    index = 0
    playlistbox.insert(index,filename)
    playlist.insert(index,filename_path)
    index += 1

subMenu = Menu(menubar, tearoff=0)
menubar.add_cascade(label="File", menu=subMenu)
subMenu.add_command(label="Open", command=browse_files)
subMenu.add_command(label="Exit", command=root.destroy)

def about():
    tkinter.messagebox.showinfo('About Sa Re Ga Ma', 'This music player is built using Tkinter')

subMenu = Menu(menubar, tearoff=0)
menubar.add_cascade(label="Help", menu=subMenu)
subMenu.add_command(label="About", command=about)

mixer.init()


root.title("Sa Re Ga Ma")
root.iconbitmap(r'images/icon.ico')

leftframe = Frame(root)
leftframe.pack(side=LEFT,padx=30,pady=30)

playlistbox = Listbox(leftframe)
playlistbox.pack()

addBtn = ttk.Button(leftframe,text="Add",command=browse_files)
addBtn.pack(side=LEFT)

def del_song():
    selected_song = playlistbox.curselection()
    selected_song = int(selected_song[0])
    playlistbox.delete(selected_song)
    playlist.pop(selected_song)

delBtn = ttk.Button(leftframe,text="Remove",command=del_song)
delBtn.pack(side=LEFT)

rightframe = Frame(root)
rightframe.pack(pady=30)

topframe = Frame(rightframe)
topframe.pack()

lengthlabel = ttk.Label(topframe,text="Total Length  :  -- : --")
lengthlabel.pack(pady=5)

currentTimelabel = ttk.Label(topframe,text="Current Time  :  -- : --",relief=GROOVE)
currentTimelabel.pack()

def show_details(play_song):
    filedata = os.path.splitext(play_song)
    
    if filedata[1] == '.mp3':
        audio = MP3(play_song)
        total_length = audio.info.length
    else:
        a = mixer.Sound(play_song)
        total_length = a.get_length()

    mins,secs = divmod(total_length,60)
    mins = round(mins)
    secs = round(secs)
    timeformat = '{:02d}:{:02d}'.format(mins,secs)
    lengthlabel['text'] = "Total Length" + "  :  " + timeformat

    t1 = threading.Thread(target=start_count,args=(total_length,))
    t1.start()

def start_count(t):
    global paused
    current_time = 0
    while current_time<=t and mixer.music.get_busy():
        if paused:
            continue
        else:
            mins,secs = divmod(current_time,60)
            mins = round(mins)
            secs = round(secs)
            timeformat = '{:02d}:{:02d}'.format(mins,secs)
            currentTimelabel['text'] = "Current Time" + "  :  " + timeformat
            time.sleep(1)
            current_time += 1

def play_music():
    global paused

    if paused:
        mixer.music.unpause()
        statusbar['text'] = "Music Resumed"
        paused = FALSE
    else:
        try:
            stop_music()
            time.sleep(1)
            selected_song = playlistbox.curselection()
            selected_song = int(selected_song[0])
            play_it = playlist[selected_song]
            mixer.music.load(play_it)
            mixer.music.play()
            statusbar['text'] = "Playing Music" + " - " + os.path.basename(play_it)
            show_details(play_it)
        except:
            tkinter.messagebox.showerror('File Not Found', 'Sa Re Ga Ma could not find the file. Please Check Again') 


def stop_music():
    mixer.music.stop()
    statusbar['text'] = "Music Stopped"
    
    
paused = FALSE

def pause_music():
    global paused
    paused = TRUE
    mixer.music.pause()
    statusbar['text'] = "Music Paused"

def rewind_music():
    play_music()
    statusbar['text'] = "Music Rewinded"

def set_vol(val):
    volume = float(val)/100
    mixer.music.set_volume(volume)
    
muted = FALSE
    
def mute_music():
    global muted
    
    if muted:
        mixer.music.set_volume(0.4)
        volumeBtn.configure(image=volumePhoto)
        scale.set(40)
        muted = FALSE
    else:
        mixer.music.set_volume(0)
        volumeBtn.configure(image=mutePhoto)
        scale.set(0)
        muted = TRUE


middleframe = Frame(rightframe)
middleframe.pack(padx=30, pady=30)

playPhoto = PhotoImage(file='images/play.png')
playBtn = ttk.Button(middleframe, image=playPhoto, command=play_music)
playBtn.grid(row=0, column=0, padx=10)

stopPhoto = PhotoImage(file='images/stop.png')
stopBtn = ttk.Button(middleframe, image=stopPhoto, command=stop_music)
stopBtn.grid(row=0, column=1, padx=10)

pausePhoto = PhotoImage(file='images/pause.png')
pauseBtn = ttk.Button(middleframe, image=pausePhoto, command=pause_music)
pauseBtn.grid(row=0, column=2, padx=10)

bottomframe = Frame(rightframe)
bottomframe.pack()

rewindPhoto = PhotoImage(file='images/rewind.png')
rewindBtn = ttk.Button(bottomframe, image=rewindPhoto, command=rewind_music)
rewindBtn.grid(row=0, column=0)

mutePhoto = PhotoImage(file='images/mute.png')
volumePhoto = PhotoImage(file='images/volume.png')
volumeBtn = ttk.Button(bottomframe, image=volumePhoto, command=mute_music)
volumeBtn.grid(row=0, column=1)

scale = ttk.Scale(bottomframe, from_=0, to_=100, orient=HORIZONTAL, command=set_vol)
scale.set(40)
mixer.music.set_volume(0.4)
scale.grid(row=0, column=2, padx=30, pady=15)

def on_closing():
    stop_music()
    root.destroy()

root.protocol("WM_DELETE_WINDOW",on_closing)

root.mainloop()
