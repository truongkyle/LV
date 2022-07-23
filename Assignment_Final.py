from decimal import DefaultContext
from tkinter import Tk, Text, TOP, BOTH, X, N, LEFT, RIGHT, BOTTOM, Canvas, NW
from tkinter.ttk import Frame, Label, Entry, Button, Combobox
import tkinter as tk
from tkinter.messagebox import showinfo
from tkvideo import tkvideo
from tkVideoPlayer import TkinterVideo
from tkinter.filedialog import askopenfile, asksaveasfile, askopenfilename, askdirectory
import xlsxwriter
import time
import datetime
from object_tracker_4 import ObjectTracker
import csv
from PIL import Image, ImageTk
import cv2


class main_window(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.parent = parent
        self.filename_1 = ''
        self.pause_1 = True
        self.f = True
        self.initUI()
        self.list_data_excel = [['Time', 'Total Vehicle', ' Current Vehicle', 'Average Speed', 'FPS', 'Total Car', 'Total Truck']]
        self.data_excel = []
        self.last_time = datetime.datetime.now()
        self.duration_time = 3
        # self.setParammeter(7.5, 7, 6.5)
        
        ### For Demo #####
        # self.clock()
    def get_size_screen(self):
        
        width = self.parent.winfo_width()
        height = self.parent.winfo_height()
        print('screeennnnn {} {}'.format(width, height))
        # self.parent.after(10, self.get_size_screen)

    def initUI(self):
        self.parent.title("Assignment_Group1")
        self.pack(fill=BOTH, expand=0)
        
        #frame1
        frame1 = Frame(self)
        frame1.pack(fill=X)
        
        # self.get_size_screen()
        #frame2
        frame2 = Frame(self)
        frame2.pack(fill=X)
        
        #frame3
        frame3 = Frame(self)
        frame3.pack(fill=X)
        
        #frame4
        frame4 = Frame(self)
        frame4.pack(fill=X)
        
        #frame5
        frame5 = Frame(self)
        frame5.pack(fill=X)

        #frame6
        frame6 = Frame(self)
        frame6.pack(fill=X)

        #frame7
        frame7 = Frame(self)
        frame7.pack(fill=X)     
        
            # Average Speed
        self.lbl1 = Label(frame1, text="Average Speed (km/h)", width=20)
        self.lbl1.pack(side=LEFT, padx=5, pady=5)
                    #Vehicle counting
        self.lbl2 = Label(frame1, text="Current Vehicle Number", width=22)
        self.lbl2.pack(side=LEFT, padx=5, pady=5)

            # App title
        self.lbl7 = Label(frame1, text="VEHICLE COUNTING AND SPEED ESTIMATING SYSTEM", font='serif 30')
        self.lbl7.pack()
    
        self.entry1 = Entry(frame2,  width=20)
        self.entry1['state'] = 'readonly'
        self.entry1.pack(side=LEFT, anchor=N, padx=5, pady=5)

        self.entry2 = Entry(frame2,  width=20)
        self.entry2['state'] = 'readonly'
        self.entry2.pack(side=LEFT, anchor=N, padx=5, pady=5)  
        
            #Label Source + Mode 1
        self.lbl8 = Label(frame2, text="Source", width=10)
        self.lbl8.pack(side=LEFT, anchor=N, padx=15, pady=5)
        
        self.entry_src = Entry(frame2,  width=43)
        self.entry_src['state'] = 'readonly'
        self.entry_src.pack(side=LEFT, anchor=N, padx=5, pady=5) 


            #Hyper Parameter 2
        self.lbl4 = Label(frame2, text="A-B (m): ", width=7)
        self.lbl4.pack(side=LEFT, anchor=N, padx=15, pady=5)
  
        self.entry4 = Entry(frame2,  width=10)
        self.entry4.insert(10, "7.5")
        self.entry4.pack(side=LEFT, anchor=N, padx=0, pady=5)

            #Hyper Parameter 3
        self.lbl5 = Label(frame2, text="B-C (m): ", width=7)
        self.lbl5.pack(side=LEFT, anchor=N, padx=5, pady=5)
  
        self.entry5 = Entry(frame2,  width=10)
        self.entry5.insert(10, "7")
        self.entry5.pack(side=LEFT, anchor=N, padx=5, pady=5)

            #Hyper Parameter 3
        self.lbl6 = Label(frame2, text="C-D (m):", width=7)
        self.lbl6.pack(side=LEFT, anchor=N, padx=5, pady=5)
  
        self.entry6 = Entry(frame2,  width=10)
        self.entry6.insert(10, "6.5")
        self.entry6.pack(side=LEFT, anchor=N, padx=5, pady=5)
        # self.lbl9 = Label(frame2, text="Mode", width=30)
        # self.lbl9.pack(side=LEFT, anchor=N, padx=50, pady=5)

        #Total Count
        self.lbl3 = Label(frame3, text="Total Vehicle Number", width=20)
        self.lbl3.pack(side=LEFT, anchor=N, padx=5, pady=5)

        self.lbl3 = Label(frame3, text="FPS", width=20)
        self.lbl3.pack(side=LEFT, anchor=N, padx=5, pady=5)

            #Select video
        self.button_browser1 = Button(frame3, text="Select video", width=12, command=self.open_file)
        self.button_browser1.pack(side=LEFT, anchor=N, padx=5, pady=5)
        
            #Play video
        self.play = Button(frame3, text="Play", width=10, command=self.play_button)
        self.play.pack(side=LEFT, anchor=N, padx=15, pady=5)

            #Pause video
        self.pause = Button(frame3, text="Pause", width=10, command=self.pause_video_1)
        self.pause.pack(side=LEFT, anchor=N, padx=5, pady=5) 
            #Export to excel
        self.button_export = Button(frame3, text="Export to CSV", command=self.save)
        self.button_export.pack(side=LEFT, padx=5, pady=5)
            # Set parameter
        self.resume = Button(frame3, text="Set parameters", width=15, command=self.set_parameter)
        self.resume.pack(side=LEFT, anchor=N, padx=150, pady=5)  
        # Total count
        self.entry3 = Entry(frame4,  width=20)
        self.entry3['state'] = 'readonly'
        self.entry3.pack(side=LEFT, anchor=N, padx=5, pady=5)
        # FPS
        self.entry3_2 = Entry(frame4,  width=20)
        self.entry3_2['state'] = 'readonly'
        self.entry3_2.pack(side=LEFT, anchor=N, padx=5, pady=5)

        #Total Count
        self.lbl3 = Label(frame5, text="Total Car", width=20)
        self.lbl3.pack(side=LEFT, anchor=N, padx=5, pady=5)

        self.lbl3 = Label(frame5, text="Total Truck", width=20)
        self.lbl3.pack(side=LEFT, anchor=N, padx=5, pady=5)

        # Total Car
        self.entry6_2 = Entry(frame6,  width=20)
        self.entry6_2['state'] = 'readonly'
        self.entry6_2.pack(side=LEFT, anchor=N, padx=5, pady=5)
        # Trucks
        self.entry6_3 = Entry(frame6,  width=20)
        self.entry6_3['state'] = 'readonly'
        self.entry6_3.pack(side=LEFT, anchor=N, padx=5, pady=5)


            #Label MONITOR
        self.lbl12 = Label(frame4, text="MONITOR", font='serif 20')
        self.lbl12.pack(anchor=N, padx=210, pady=5)

        
            # video display Area
        self.canvas_1 = Canvas(frame6)
        self.canvas_1.pack(padx=10, pady= 10)
        self.height_canvas = 300
        self.width_canvas = 400
        self.canvas_1.config(width=self.width_canvas, height=self.height_canvas)
        self.canvas_1.bind('<Control-1>', self.get_x_and_y)
        


    def setParammeter(self, ab, bc, cd):
        
        self.entry4['state'] = 'readwrite'
        self.entry4.delete(0, "end")
        self.entry4.insert(0, ab)
        self.entry4['state'] = 'readonly'

        self.entry5['state'] = 'readwrite'
        self.entry5.delete(0, "end")
        self.entry5.insert(0, bc)
        self.entry5['state'] = 'readonly'

        self.entry6['state'] = 'readwrite'
        self.entry6.delete(0, "end")
        self.entry6.insert(0, cd)
        self.entry6['state'] = 'readonly'

    def get_x_and_y(self, event):
        global lasx, lasy
        lasx, lasy = event.x, event.y
        print(lasx, lasy)

    def open_file(self):
        # self.pause_1 = False
        self.filename_1 = askopenfilename(title="Select Video", filetypes=(("MP4 files", "*.mp4"),("WMV files", "*.wmv"),("AVI files", "*.avi")))
        print(self.filename_1)
        self.entry_src['state'] = 'readwrite'
        self.entry_src.delete(0, "end")
        self.entry_src.insert(0, self.filename_1)
        self.entry_src['state'] = 'readonly'
        # print(self.filename_1)
        self.path_file_list_detection ='./' + self.filename_1.split('/')[-1].replace('mp4','json')
        print(self.path_file_list_detection)

        self.list_data_excel = [['Time', 'Total Vehicle', ' Current Vehicle', 'Average Speed', 'FPS', 'Total Car', 'Total Truck']]

        if self.f:
            self.f = False
            # self.path_file_list_detection = './cars.json'
            self.tracker = ObjectTracker(video_path = self.filename_1, json_path = self.path_file_list_detection, frame_num = 0, output = '')
            # Open the video file
            self.cap_1 = cv2.VideoCapture(self.filename_1)
            self.width = self.cap_1.get(cv2.CAP_PROP_FRAME_WIDTH)
            self.height = self.cap_1.get(cv2.CAP_PROP_FRAME_HEIGHT)
            self.canvas_1.config(width=self.width, height=self.height)
            self.fistly_play_video_1()
        else:
            self.entry_src.insert(0, self.filename_1)
            self.re_play_video()
            self.pause_1 = True
            self.fistly_play_video_1(f = False)
    def re_play_video(self):
        self.cap_1.set(cv2.CAP_PROP_POS_FRAMES, 0)
        self.tracker = ObjectTracker(video_path = self.filename_1, json_path = self.path_file_list_detection, frame_num = 0, output = '')
        # self.cap_1.release()
        self.cap_1 = cv2.VideoCapture(self.filename_1)
        print('========'*10)
    def get_frame_1(self):  # get only one frame
        try:
            if self.cap_1.isOpened():
                ret, frame = self.cap_1.read()             
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                result1, total_count , count, average_speed, frame, fps, car_num, truck_num = self.tracker.tracking(frame)
                # print(frame)
                average_speed = round(average_speed, 2)
                current_time = datetime.datetime.now()
                if (current_time - self.last_time).seconds >= self.duration_time and not self.pause_1:
                    now = datetime.datetime.now()
                    current_day = now.strftime("%H:%M:%S")
                    data_excel = [current_day, total_count, count, average_speed, fps, car_num, truck_num]
                    self.list_data_excel.append(data_excel)
                    self.last_time = current_time
                self.entry1['state'] = 'readwrite'
                self.entry1.delete(0, "end")
                self.entry1.insert(0, average_speed)
                self.entry1['state'] = 'readonly'

                self.entry2['state'] = 'readwrite'
                self.entry2.delete(0, "end")
                self.entry2.insert(0, count)
                self.entry2['state'] = 'readonly'

                self.entry3['state'] = 'readwrite'
                self.entry3.delete(0, "end")
                self.entry3.insert(0, total_count)
                self.entry3['state'] = 'readonly'
                
                self.entry3_2['state'] = 'readwrite'
                self.entry3_2.delete(0, "end")
                self.entry3_2.insert(0, fps)
                self.entry3_2['state'] = 'readonly'

                self.entry6_2['state'] = 'readwrite'
                self.entry6_2.delete(0, "end")
                self.entry6_2.insert(0, car_num)
                self.entry6_2['state'] = 'readonly'

                self.entry6_3['state'] = 'readwrite'
                self.entry6_3.delete(0, "end")
                self.entry6_3.insert(0, truck_num)
                self.entry6_3['state'] = 'readonly'
                return ret, frame
        except:
            self.pause_1 = True
            self.re_play_video()
            return self.ret, self.frame
            
    
    def fistly_play_video_1(self, f = True):
        # Get a frame from the video source, and go to the next frame automatically
        ret, frame = self.get_frame_1()
        self.pause_1 = True
        if ret:
            self.photo_1 = ImageTk.PhotoImage(image=Image.fromarray(frame))
            self.canvas_1.create_image(0, 0, image=self.photo_1, anchor=NW)
        if f:   
            self.play_video_1() 
    def play_button(self):
        if self.filename_1 != '':
            self.last_time = datetime.datetime.now()
            self.pause_1 = False

    def play_video_1(self):
        # Get a frame from the video source, and go to the next frame automatically
        if self.filename_1 != '' and not self.pause_1:
            ret, frame = self.get_frame_1()
            self.ret = ret
            self.frame = frame
            if ret:
                self.photo_1 = ImageTk.PhotoImage(image=Image.fromarray(frame))
                self.canvas_1.create_image(0, 0, image=self.photo_1, anchor=NW)
        # print('9'*30)
        self.parent.after(2, self.play_video_1)
        # if not self.pause_1:
            

    def pause_video_1(self):
        self.pause_1 = True

    # Addition
    def set_parameter(self):
        meter_distance = [float(self.entry4.get()), float(self.entry5.get()), float(self.entry6.get())]
        print(meter_distance)
        self.pause_1 = True
        self.tracker.real_distance_list = meter_distance
        
        
    def save(self):
        files = [('csv', '*.csv*')]
        file = asksaveasfile(filetypes = files, defaultextension = '.csv')
        print (file.name)
        with open(file.name, 'w', newline='') as data_file:
            writer = csv.writer(data_file)
            writer.writerows(self.list_data_excel)


    
##################################################

root = Tk()
root.geometry("1000x600+0+0")
app = main_window(root)
root.mainloop()
