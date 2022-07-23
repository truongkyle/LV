from tkinter import Tk, Text, TOP, BOTH, X, N, LEFT, RIGHT
from tkinter.ttk import Frame, Label, Entry, Button, Combobox
import tkinter as tk
from tkinter.messagebox import showinfo
from tkvideo import tkvideo
from tkVideoPlayer import TkinterVideo
from tkinter.filedialog import askopenfile

from PIL import Image, ImageTk
import cv2

class main_window(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.parent = parent
        self.initUI()
    
    def initUI(self):
        self.parent.title("Assignment_Group1")
        self.pack(fill=BOTH, expand=0)
        
        #frame1
        frame1 = Frame(self)
        frame1.pack(fill=X)
        
            # Average Speed
        lbl1 = Label(frame1, text="Average Speed", width=20)
        lbl1.pack(side=LEFT, padx=5, pady=5)
  
        entry1 = Entry(frame1,  width=10, state= "readonly")
        entry1.pack(side=LEFT, anchor=N, padx=5, pady=5)
        
            # App title
        lbl7 = Label(frame1, text="VEHICLE COUNTING AND SPEED ESTIMATING SYSTEM", font='serif 30')
        lbl7.pack()
    
        #frame2
        frame2 = Frame(self)
        frame2.pack(fill=X)
            
            #Vehicle counting
        lbl2 = Label(frame2, text="Vehicle counting", width=20)
        lbl2.pack(side=LEFT, anchor=N, padx=5, pady=5)
  
        entry2 = Entry(frame2,  width=10, state= "readonly")
        entry2.pack(side=LEFT, anchor=N, padx=5, pady=5)
        
            #Label Source + Mode 1
        lbl8 = Label(frame2, text="Source 1", width=30)
        lbl8.pack(side=LEFT, anchor=N, padx=50, pady=5)
        
        lbl9 = Label(frame2, text="Mode 1", width=30)
        lbl9.pack(side=LEFT, anchor=N, padx=50, pady=5)
        
            #Label Source + Mode 2
        lbl10 = Label(frame2, text="Source 2", width=30)
        lbl10.pack(side=LEFT, anchor=N, padx=50, pady=5)
        
        lbl11 = Label(frame2, text="Mode 2", width=30)
        lbl11.pack(side=LEFT, anchor=N, padx=50, pady=5)
  
        #frame3
        frame3 = Frame(self)
        frame3.pack(fill=X, expand=True)
  
            #Hyper Parameter 1
        lbl3 = Label(frame3, text="Hyper Parameter 01", width=20)
        lbl3.pack(side=LEFT, anchor=N, padx=5, pady=5)
  
        entry3 = Entry(frame3,  width=10)
        entry3.pack(side=LEFT, anchor=N, padx=5, pady=5)
        
        #frame4
        frame4 = Frame(self)
        frame4.pack(fill=X, expand=True)
  
            #Hyper Parameter 2
        lbl4 = Label(frame4, text="Hyper Parameter 02", width=20)
        lbl4.pack(side=LEFT, anchor=N, padx=5, pady=5)
  
        entry4 = Entry(frame4,  width=10)
        entry4.pack(side=LEFT, anchor=N, padx=5, pady=5)
        
            #Label MONITOR
        lbl12 = Label(frame4, text="MONITOR 1", font='serif 20')
        lbl12.pack(side=LEFT, anchor=N, padx=210, pady=5)
        
        lbl12 = Label(frame4, text="MONITOR 2", font='serif 20')
        lbl12.pack(side=LEFT, anchor=N, padx=210, pady=5)
        
        #frame5
        frame5 = Frame(self)
        frame5.pack(fill=X, expand=True)
  
            #Hyper Parameter 3
        lbl5 = Label(frame5, text="Hyper Parameter 03", width=20)
        lbl5.pack(side=LEFT, anchor=N, padx=5, pady=5)
  
        entry5 = Entry(frame5,  width=10)
        entry5.pack(side=LEFT, anchor=N, padx=5, pady=5)

            #Select source 1
        src1_cb = Combobox(frame3,  width=30, state= "readonly", values = ['(Select camera or video)', 'Camera 1', 'Camera 2', 'Video path'])
        src1_cb.pack(side=LEFT, anchor=N, padx=5, pady=5)
        src1_cb.current(0)
        
        def open_file(video_label):
            file = askopenfile(mode='r', filetypes=[('Video Files', ["*.mp4"])])
            if file is not None:
                global filename
                filename = file.name
                player1 = tkvideo(filename, video_label, loop = 1, size = (550, 500))
                player1.play()
                button_browser1['state'] = 'disable'
                


        cap= cv2.VideoCapture(0)
    # Define function to show frame
        def show_frames(video_label):
           # Get the latest frame and convert into Image
            cv2image= cv2.cvtColor(cap.read()[1],cv2.COLOR_BGR2RGB)
            img = Image.fromarray(cv2image)
           # Convert image to PhotoImage
            imgtk = ImageTk.PhotoImage(image = img)
            video_label.imgtk = imgtk
            video_label.configure(image=imgtk)
           # Repeat after an interval to capture continiously
            video_label.after(20, show_frames(video_label))
        global video_label1
        video_label1 = Label(frame5)
        video_label1.pack(side=LEFT, anchor=N, pady=5, padx=5)
        def source_changed1(event):
                #MONITOR 1 
            global video_label1                
            if src1_cb.current() == 3:
                button_browser1['state'] = 'anable'
                video_label1.destroy() 
                video_label1 = Label(frame5)
                video_label1.pack(side=LEFT, anchor=N, pady=5, padx=5)
            elif src1_cb.current() == 1:
                button_browser1['state'] = 'disable'
                video_label1.destroy() 
                video_label1 = Label(frame5)
                video_label1.pack(side=LEFT, anchor=N, pady=5, padx=5)
                
                show_frames(video_label1)
            elif src1_cb.current() == 2:
                button_browser1['state'] = 'disable'
                video_label1.destroy() 
                video_label1 = Label(frame5)
                video_label1.pack(side=LEFT, anchor=N, pady=5, padx=5)
                
                show_frames(video_label1)
            else:
                button_browser1['state'] = 'disable'
                video_label1.destroy()
                video_label1 = Label(frame5)
                video_label1.pack(side=LEFT, anchor=N, pady=5, padx=5)
                
           
        src1_cb.bind('<<ComboboxSelected>>', source_changed1)
        button_browser1 = Button(frame3, text="...", width=5, state="disable", command=lambda: open_file(video_label1))
        button_browser1.pack(side=LEFT, anchor=N, padx=5, pady=5)
        

        
            #Select mode 1
        mode1_cb = Combobox(frame3,  width=30, state= "readonly")
        mode1_cb.pack(side=LEFT, anchor=N, padx=50, pady=5)
        mode1_cb['values'] = ('(Select mode)', 'None', 'Speed estimating', 'Vehicle counting')
        mode1_cb.current(0)
        
            #Select source 2
        src2_cb = Combobox(frame3,  width=30, state= "readonly", values = ['(Select camera or video)', 'Camera 1', 'Camera 2', 'Video path'])
        src2_cb.pack(side=LEFT, anchor=N, padx=5, pady=5)
        src2_cb.current(0)
        
        global video_label2
        video_label2 = Label(frame5)
        video_label2.pack(side=RIGHT, anchor=N, pady=5, padx=5)        
        def source_changed2(event):
            #MONITOR 2
            global video_label2                
            if src1_cb.current() == 3:
                button_browser2['state'] = 'anable'
                video_label2.destroy() 
                video_label2 = Label(frame5)
                video_label2.pack(side=RIGHT, anchor=N, pady=5, padx=5)
            elif src1_cb.current() == 1:
                button_browser2['state'] = 'disable'
                video_label2.destroy() 
                video_label2 = Label(frame5)
                video_label2.pack(side=RIGHT, anchor=N, pady=5, padx=5)
                
                show_frames(video_label2)
            elif src1_cb.current() == 2:
                button_browser2['state'] = 'disable'
                video_label2.destroy() 
                video_label2 = Label(frame5)
                video_label2.pack(side=RIGHT, anchor=N, pady=5, padx=5)
                
                show_frames(video_label2)
            else:
                button_browser2['state'] = 'disable'
                video_label2.destroy()
                video_label2 = Label(frame5)
                video_label2.pack(side=RIGHT, anchor=N, pady=5, padx=5)
            
        src2_cb.bind('<<ComboboxSelected>>', source_changed2)       
        button_browser2 = Button(frame3, text="...", width=5, state="disable", command=lambda: open_file(video_label2))
        button_browser2.pack(side=LEFT, anchor=N, padx=5, pady=5)
        
        
           #Select mode 2
        mode2_cb = Combobox(frame3,  width=30, state= "readonly")
        mode2_cb.pack(side=LEFT, anchor=N, padx=50, pady=5)
        mode2_cb['values'] = ('(Select mode)', 'None', 'Speed estimating', 'Vehicle counting')
        mode2_cb.current(0)
        
        #frame6
        frame6 = Frame(self)
        frame6.pack(fill=X, expand=True)
        
        button_export = Button(self, text="Export to excel")
        button_export.pack(side=LEFT, padx=5, pady=5)
  
root = Tk()
root.geometry("1000x600+0+0")
app = main_window(root)
root.mainloop()
