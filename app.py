from tkinter import *
from tkinter import messagebox
from tkinter import filedialog
from tkinter.filedialog import asksaveasfile
import PIL.Image, PIL.ImageTk
from object_tracker_4 import ObjectTracker
import cv2

BG_COLOR = 'white'

class videoGUI:

    def __init__(self, window, window_title):

        self.param_1 = 0
        self.param_2 = 0
        self.param_3 = 0
        self.count = 0
        self.speed = 0
        self.total_count = 0

        self.window = window
        self.window.title(window_title)

        self.window.rowconfigure(0, minsize=300, weight=1)
        self.window.columnconfigure(1, minsize=600, weight=1)

        top_frame_0 = Frame(self.window, bd=1)
        top_frame_0.grid(row=0, column=0)

        top_frame_1 = Frame(self.window, bd=1)
        top_frame_1.grid(row=0, column=1, padx=5, pady=5)

        bottom_frame_0 = Frame(self.window)
        bottom_frame_0.grid(row=1, column=0)

        bottom_frame_1 = Frame(self.window)
        bottom_frame_1.grid(row=1, column=1, ipadx=5)

        self.pause_1 = False  # Parameter that controls pause button
        self.pause_2 = False  # Parameter that controls pause button

        self.canvas_1 = Canvas(top_frame_1)
        self.canvas_1.pack()
        self.canvas_1.config(width=400, height=300)

        # Select Button
        self.btn_select_1 = Button(bottom_frame_1, text="Select video", width=15, command=self.open_file_1)
        self.btn_select_1.grid(row=0, column=0)

        # Play Button
        self.btn_play_1 = Button(bottom_frame_1, text="Play", width=15, command=self.play_video_1)
        self.btn_play_1.grid(row=0, column=1)

        # Pause Button
        self.btn_pause_1 = Button(bottom_frame_1, text="Pause", width=15, command=self.pause_video_1)
        self.btn_pause_1.grid(row=0, column=2)

        # Resume Button
        self.btn_resume_1 = Button(bottom_frame_1, text="Resume", width=15, command=self.resume_video_1)
        self.btn_resume_1.grid(row=0, column=3)

        # Dropdown Mode
        options = ["Counting Vehicle", "Measuring"]
        self.clicked_1 = StringVar()
        self.clicked_1.set("Select Mode")

        dropdown_1 = OptionMenu(bottom_frame_1, self.clicked_1, *options,
                                command=self.callback_dropdown)
        dropdown_1.configure(widt=20)
        dropdown_1.grid(row=0, column=4)

        self.text_speed_avg_1 = StringVar()
        self.text_car_count_1 = StringVar()
        self.text_hp_para_1_1 = StringVar()
        self.text_hp_para_2_1 = StringVar()
        self.text_hp_para_3_1 = StringVar()

        label_speed_avg_1 = Label(top_frame_0, text='Tốc độ trung bình:')
        label_car_count_1 = Label(top_frame_0, text='Số lượng xe:')
        label_hp_para_1_1 = Label(top_frame_0, text='Hyper Parameter 01:')
        label_hp_para_2_1 = Label(top_frame_0, text='Hyper Parameter 02:')
        label_hp_para_3_1 = Label(top_frame_0, text='Hyper Parameter 03:')

        vcmd = (window.register(self.callback))

        self.entry_speed_avg_1 = Entry(top_frame_0, textvariable=self.text_speed_avg_1,
                                background=BG_COLOR, borderwidth=0, highlightthickness=0)
        self.entry_car_count_1 = Entry(top_frame_0, textvariable=self.text_car_count_1,
                                background=BG_COLOR, borderwidth=0, highlightthickness=0)
        self.entry_hp_para_1_1 = Entry(top_frame_0, validate='all', validatecommand=(vcmd, '%P'),
                                       textvariable=self.text_hp_para_1_1)
        self.entry_hp_para_2_1 = Entry(top_frame_0, validate='all', validatecommand=(vcmd, '%P'),
                                       textvariable=self.text_hp_para_2_1)
        self.entry_hp_para_3_1 = Entry(top_frame_0, validate='all', validatecommand=(vcmd, '%P'),
                                       textvariable=self.text_hp_para_3_1)

        button_export_1 = Button(bottom_frame_0, text="Export", command=self.export_file)

        label_speed_avg_1.grid(row=0, column=0, sticky="n", padx=5, pady=5)
        label_car_count_1.grid(row=1, column=0, sticky="s", padx=5, pady=5)
        label_hp_para_1_1.grid(row=2, column=0, sticky="e", padx=5, pady=5)
        label_hp_para_2_1.grid(row=3, column=0, sticky="w", padx=5, pady=5)
        label_hp_para_3_1.grid(row=4, column=0, sticky="ew", padx=5, pady=5)
        button_export_1.grid(row=5, column=0, sticky="nsew", padx=5, pady=5)

        self.entry_speed_avg_1.grid(row=0, column=1, sticky="n", padx=0, pady=7)
        self.entry_car_count_1.grid(row=1, column=1, sticky="n", padx=0, pady=7)
        self.entry_hp_para_1_1.grid(row=2, column=1, sticky="n", padx=0, pady=7)
        self.entry_hp_para_2_1.grid(row=3, column=1, sticky="n", padx=0, pady=7)
        self.entry_hp_para_3_1.grid(row=4, column=1, sticky="n", padx=0, pady=7)

        self.delay = 10  # ms

        self.window.mainloop()

    def open_file_1(self):
        self.pause_1 = False
        self.filename_1 = filedialog.askopenfilename(title="Select Video",
                                                     filetypes=(
                                                         ("MP4 files", "*.mp4"),
                                                         ("WMV files", "*.wmv"),
                                                         ("AVI files", "*.avi")))
        path_file_list_detection = './cars.json'
        self.tracker = ObjectTracker(video_path = self.filename_1, json_path = path_file_list_detection, frame_num = 0, output = '')

        # Open the video file
        self.cap_1 = cv2.VideoCapture(self.filename_1)
        self.width = self.cap_1.get(cv2.CAP_PROP_FRAME_WIDTH)
        self.height = self.cap_1.get(cv2.CAP_PROP_FRAME_HEIGHT)

        self.canvas_1.config(width=self.width, height=self.height)

    def get_frame_1(self):  # get only one frame
        self.speed += 0.1
        try:
            if self.cap_1.isOpened ():
                ret, frame = self.cap_1.read()
                ret, frame = ret, cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                result1, fps, count, average_speed, frame = self.tracker.tracking(frame)
                self.count = count
                self.total_count = self.tracker.total_count
                self.speed = self.total_count
                return ret, frame
        except:
            # messagebox.showerror(title='Video_1 file not found', message='Please select a video file.')
            print("End of video_1")


    def play_video_1(self):
        try:
            self.param_1 = int(self.entry_hp_para_1_1.get())
            self.param_2 = int(self.entry_hp_para_2_1.get())
            self.param_3 = int(self.entry_hp_para_3_1.get())
        except:
            pass
        print("Read parameter", self.param_1, self.param_2, self.param_3)
        print("Choose:", self.clicked_1)
        self.update_text()
        # Get a frame from the video source, and go to the next frame automatically
        ret, frame = self.get_frame_1()
        if ret:
            self.photo_1 = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(frame))
            self.canvas_1.create_image(0, 0, image=self.photo_1, anchor=NW)

        if not self.pause_1:
            self.window.after(self.delay, self.play_video_1)

    def pause_video_1(self):
        self.pause_1 = True

    # Addition
    def resume_video_1(self):
        self.pause_1 = False
        self.play_video_1()

    # Release the video source when the object is destroyed
    def __del__(self):
        if self.cap_1.isOpened():
            self.cap_1.release()

    def callback(self, P):
        if str.isdigit(P) or P == "":
            return True
        else:
            return False

    def callback_dropdown(self, selection):
        print(self.clicked_1.get())

    def export_file(self):
        try:
            Files = [('Text Document', '*.txt'),
                     ('Excel', '*.xls')]
            file_path = asksaveasfile(filetypes=Files, defaultextension=Files)
            try:
                with open(file_path.name, 'w') as f:
                    f.write("Mode: " + self.clicked_1.get() + "\n")
                    f.write("Speed: " + str(round(self.speed, 2)) + "\n")
                    f.write("Count: " + str(self.count) + "\n")
                    f.write("Param 01: " + str(self.param_1) + "\n")
                    f.write("Param 02: " + str(self.param_2) + "\n")
                    f.write("Param 03: " + str(self.param_3) + "\n")
            except:
                pass
            print(file_path.name)
        except:
            pass

    def update_text(self):
        self.text_speed_avg_1.set(round(self.speed,2))
        self.text_car_count_1.set(self.count)

##### End Class #####


# Create a window and pass it to videoGUI Class
videoGUI(Tk(), "VEHICLE COUNTING AND SPEED ESTIMATING SYSTEM")