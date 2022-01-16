#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
import cv2
from src import forward_energy, seam_carving
import skvideo
import skvideo.io
from functools import partial
import threading
import imageio
from PIL import Image, ImageTk


# In[2]:


# yi po shi
cut = []
input_file = ""
fps = 0
cap = 0
frame_count = 0
vid_out = skvideo.io.FFmpegWriter("none.mp4")


# In[3]:


import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog
import tkinter.ttk as ttk
# from tkinter.ttk import *
from tkinter.ttk import Progressbar
import os


# In[4]:


window = tk.Tk()
window.title("VideoSeamCarving")
#style = Style()
#style.theme_use('default')
#style.configure("black.Horizontal.TProgressbar", background='black')


# In[5]:


# set up frame
frame = tk.Frame(window, width=800, height=800, bg='lightblue', colormap="new")
frame.grid(row=0, column=0, sticky="NW")
frame.grid_propagate(0)
frame.update()


# In[6]:


# add title
lbl_title = tk.Label(frame, text="Video Seam Carving",
                  font=("微软雅黑", 25))
lbl_title.place(x=400, y=25, anchor="center")  # set position
lbl_title.config(bg='lightblue')


# In[7]:


# cut type selection
# label
lbl_cut = tk.Label(frame, text="Select Cut Type", font=("微软雅黑", 12))
lbl_cut.place(x=200, y=100, anchor="center")
lbl_cut.config(bg='lightblue')
# combo box
cut_type = ttk.Combobox(frame)
cut_type['values'] = ("horizontal", "vertical")
cut_type.current(0)  # set the selected item
cut_type.place(x=200, y=125, anchor="center")


# In[8]:


# cut number selection
# label
lbl_cut2 = tk.Label(frame, text="Input Seam Number", font=("微软雅黑", 12))
lbl_cut2.place(x=400, y=100, anchor="center")
lbl_cut2.config(bg='lightblue')
# entry
cut_number = tk.Entry(frame, width=10)
cut_number.place(x=400, y=125, anchor="center")

# handle set_cut event
def set_cut(cut):
    cut.append(cut_type.get())
    cut.append(int(cut_number.get()))
    # message box
    messagebox.showinfo('cut parameter', f'Cut is set to {cut}!')
    
set_cut_with_arg = partial(set_cut, cut)

# add button
btn_set = tk.Button(frame, text="Cut set", command=set_cut_with_arg)
btn_set.place(x=600, y=125, anchor="center")  # button position
btn_set.config(height=3, width=10)


# In[9]:


# input section
# label
lbl_input = tk.Label(frame, text="Select File", font=("微软雅黑", 12))
lbl_input.place(x=200, y=200, anchor="center")
lbl_input.config(bg='lightblue')
# handle input_file event


def select_file():
    # file = filedialog.askopenfilename(filetypes=(("MOV Files", "*.mov"),("MP4 Files", "*.mp4"),("AVI Files","*.avi"))) # after choosing, file will hold the path
    # after choosing, file will hold the path
    global input_file
    file = filedialog.askopenfilename(filetypes=(
        ("MP4 Files", "*.mp4"), ("MOV Files", "*.mov"), ("M4V Files", "*.m4v")))
    # input_file.append(file)
    input_file = file
    


# select_file_with_arg = partial(select_file, input_file)


def test():
    global cap, fps, frame_count
    cap = cv2.VideoCapture(input_file)
    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    duration = frame_count / fps


    minutes = int(duration / 60)
    seconds = duration % 60
    
    messagebox.showinfo('input information',
                        f'fps = {fps}\n number of frames = {frame_count} \n duration (S) = {duration} \n duration (M:S) = {minutes} : {seconds}')


# test_with_arg = partial(test, cap, fps, frame_count)

# add button
btn_input = tk.Button(frame, text="Select File", command=select_file)
btn_input.place(x=200, y=250, anchor="center")
btn_input.config(height=3, width=10)

# for test only
btn_test = tk.Button(frame, text="Input Set", command=test)
btn_test.place(x=600, y=250, anchor="center")
btn_test.config(height=3, width=10)


# In[10]:


# output section
# label
lbl_out = tk.Label(frame, text="Output File Name", font=("微软雅黑", 12))
lbl_out.place(x=200, y=350, anchor="center")
lbl_out.config(bg='lightblue')
# entry
output_name = tk.Entry(frame, width=10)
output_name.place(x=200, y=375, anchor="center")

# handle output event


def output():
    global fps, vid_out
    vid_out = skvideo.io.FFmpegWriter(output_name.get(),
                                      outputdict={'-vcodec': 'libx264',
                                                  '-pix_fmt': 'yuv420p',
                                                  '-r': str(fps)})
    # message box
    messagebox.showinfo(
        'Output information', f'Output file is set to {output_name.get()}!\n check fps = {str(fps)}')


# output_with_arg = partial(output, fps, vid_out)
# add button
btn_out = tk.Button(frame, text="Output set", command=output)
btn_out.place(x=600, y=375, anchor="center")  # button position
btn_out.config(height=3, width=10)


# In[11]:


# run section (not finished)

# handle run event


def run():
    global cut, cap, fps, frame_count, vid_out
    
    bar = Progressbar(frame, length=200)
    bar.place(x=300, y=450)
    bar['value'] = 0  # placeholder
    i = 1

    while cap.isOpened():
        ret, frames = cap.read()
        if ret:
            #print("Carve frame: " + str(i) + "/" + str(frame_count))
            bar['value'] = i/frame_count*100
            window.update_idletasks()
            img, eimg = seam_carving(frames, forward_energy, cut[1], cut[0])
            img = (img*255).astype(np.uint8)
            img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
            vid_out.writeFrame(img)
            cv2.imshow('frame', cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
            cv2.waitKey(int(fps))
        else:
            break
        i += 1
    
    cap.release()
    vid_out.close()
    cv2.destroyAllWindows()


# run_with_arg = partial(run, cut, cap, fps, frame_count, vid_out)

# add button
btn_run = tk.Button(window, text="Run", command=run)
btn_run.place(x=200, y=750, anchor="center")
btn_run.config(height=3, width=10)


# In[12]:


# play section
# handle play event
def play():
    global input_file, fps, output_name

    video_original = input_file #This is your video file path
    video_cut = output_name.get()
    video1 = imageio.get_reader(video_original)
    video2 = imageio.get_reader(video_cut)

    def stream2(label):
        
        for image in video2.iter_data():
            frame_image = ImageTk.PhotoImage(Image.fromarray(image))
            label.config(image=frame_image)
            label.image = frame_image
            cv2.waitKey(int(fps))
    
    def stream(label):

        for image in video1.iter_data():
            frame_image = ImageTk.PhotoImage(Image.fromarray(image))
            label.config(image=frame_image)
            label.image = frame_image
            cv2.waitKey(int(fps))
    
    

    my_label = tk.Label(frame)
    my_label.pack()
    my_label.place(x=200, y=600, anchor="center")
    thread = threading.Thread(target=stream, args=(my_label,))
    thread.daemon = 1
    
    
    my_label2 = tk.Label(frame)
    my_label2.pack()
    my_label2.place(x=550, y=600, anchor="center")
    thread2 = threading.Thread(target=stream2, args=(my_label2,))
    thread2.daemon = 1
    
    thread2.start()
    thread.start()
   

# add button
btn_play = tk.Button(window, text="Play", command=play)
btn_play.place(x=600, y=750, anchor="center")
btn_play.config(height=3, width=10)


# In[ ]:


# run
window.mainloop()


# In[ ]:




