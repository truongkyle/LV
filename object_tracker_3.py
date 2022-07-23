import os
import json
import numpy as np
from unittest import result
# comment out below line to enable tensorflow logging outputs
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
import time
import tensorflow as tf
physical_devices = tf.config.experimental.list_physical_devices('GPU')
if len(physical_devices) > 0:
    tf.config.experimental.set_memory_growth(physical_devices[0], True)
from absl import app, flags, logging
from absl.flags import FLAGS
import core.utils as utils
from core.yolov4 import filter_boxes
from tensorflow.python.saved_model import tag_constants
from core.config import cfg
from PIL import Image

import cv2
import numpy as np
import matplotlib.pyplot as plt
from tensorflow.compat.v1 import ConfigProto
from tensorflow.compat.v1 import InteractiveSession
# deep sort imports
from deep_sort import preprocessing, nn_matching
from deep_sort.detection import Detection
from deep_sort.tracker import Tracker
from tools import generate_detections as gdet
flags.DEFINE_string('framework', 'tf', '(tf, tflite, trt')
flags.DEFINE_string('weights', './checkpoints/yolov4-416',
                    'path to weights file')
flags.DEFINE_integer('size', 416, 'resize images to')
flags.DEFINE_boolean('tiny', False, 'yolo or yolo-tiny')
flags.DEFINE_string('model', 'yolov4', 'yolov3 or yolov4')
flags.DEFINE_string('video', './data/video/test.mp4', 'path to input video or set to 0 for webcam')
flags.DEFINE_string('output', None, 'path to output video')
flags.DEFINE_string('output_format', 'XVID', 'codec used in VideoWriter when saving video to file')
flags.DEFINE_float('iou', 0.45, 'iou threshold')
flags.DEFINE_float('score', 0.50, 'score threshold')
flags.DEFINE_boolean('dont_show', False, 'dont show video output')
flags.DEFINE_boolean('info', False, 'show detailed info of tracked objects')
flags.DEFINE_boolean('count', False, 'count objects being tracked on screen')
flags.DEFINE_string('list_data', None, 'path of list_detection data')

class ObjectTracker:
    def __init__(self, video_path, json_path, frame_num, output):
        self.total_count = 0
        self.video_path = video_path
        self.frame_num = frame_num
        self.list_track = []
        self.output = output
        self.get_info_video()
        self.load_list_detection(json_path)

    def get_info_video(self):
        try:
            vid = cv2.VideoCapture(int(self.video_path))
        except:
            vid = cv2.VideoCapture(self.video_path)

        self.out = None
        self.width = int(vid.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.height = int(vid.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.fps = int(vid.get(cv2.CAP_PROP_FPS))
        # self.codec = cv2.VideoWriter_fourcc('XVID')
        # self.out = cv2.VideoWriter(self.output, self.codec, self.fps, (self.width, self.height))

    def load_list_detection(self, json_path):
        print(json_path)
        with open(json_path,'r') as openfile:
            json_object = json.load(openfile)
        print(type(json_object))
        result = json_object['list_detections']
        print(result)
        self.list_detections = result
        return result

    def speed_estimate(self, list_track, track):
        pass

    def tracking(self, frame):
        tracks = self.list_detections[self.frame_num]
        self.frame_num +=1
        start_time = time.time()

        count = len(tracks)
        # if FLAGS.count:
        #     cv2.putText(frame, "Objects being tracked: {}".format(count), (5, 35), cv2.FONT_HERSHEY_COMPLEX_SMALL, 2, (0, 255, 0), 2)
        #     print("Objects being tracked: {}".format(count))
        #initialize color map
        cmap = plt.get_cmap('tab20b')
        colors = [cmap(i)[:3] for i in np.linspace(0, 1, 20)]
        average_speed = 0
        # update tracks
        for track in tracks:
            bbox = np.array(track['bbox'])
            class_name = track['class_name']
            track_id = track['track_id']
            center_point = [bbox[0] + (bbox[2] - bbox[0])/2, bbox[1]+(bbox[3] - bbox[1])/2]
            track_item = {
                'flat' : False,
                'track_id': track_id,
                'class_name':class_name,
                'bbox' : bbox,
                'frame' : frame,
                'center_point': center_point
            }

            if track_id > len(self.list_track):
                for i in range(track_id - len(self.list_track)):
                    self.list_track.append([])    
            self.list_track[track_id - 1].append(track_item) 
            print('len: {}, id: {}'.format(len(self.list_track), track_id -1))
            center_point_list = [i['center_point'] for i in self.list_track[track_id-1]]
        # draw bbox on screen
            color = colors[int(track_id) % len(colors)]
            color = [i * 255 for i in color]
            cv2.rectangle(frame, (int(bbox[0]), int(bbox[1])), (int(bbox[2]), int(bbox[3])), color, 2)
            cv2.rectangle(frame, (int(bbox[0]), int(bbox[1]-30)), (int(bbox[0])+(len(class_name)+len(str(track_id)))*17, int(bbox[1])), color, -1)
            cv2.putText(frame, class_name + "-" + str(track_id),(int(bbox[0]), int(bbox[1]-10)),0, 0.75, (255,255,255),2)
            center_point_list = center_point_list if len(center_point_list) < 100 else center_point_list[-100:]
            for index in range(0, len(center_point_list)-1):
                cv2.line(frame,(int(center_point_list[index][0]),int(center_point_list[index][1])),(int(center_point_list[index + 1][0]), int(center_point_list[index+1][1])),color,2)
            # cv2.polylines(frame,[center_point_list],True,color)

        # if enable info flag then print details about each track
            # if FLAGS.info:
            #     print("Tracker ID: {}, Class: {},  BBox Coords (xmin, ymin, xmax, ymax): {}, center point: {}".format(str(track_id), class_name, (int(bbox[0]), int(bbox[1]), int(bbox[2]), int(bbox[3])), (center_point[0], center_point[1])))

        # calculate frames per second of running detections
        fps = 1.0 / (time.time() - start_time)
        print("FPS: %.2f" % fps)
        result = np.asarray(frame)
        result = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        # self.out.write(result)
        self.total_count = len(self.list_track)
        return result, fps, count, average_speed, frame

def main(_argv):
    video_path = FLAGS.video

    # begin video capture
    try:
        vid = cv2.VideoCapture(int(video_path))
    except:
        vid = cv2.VideoCapture(video_path)
    path_file_list_detection = './cars.json'
    # while video is running
    tracker = ObjectTracker(video_path = video_path, json_path = path_file_list_detection, frame_num = 0, output = FLAGS.output)

    while True:
        return_value, frame = vid.read()
        if return_value:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        else:
            print('Video has ended or failed, try a different video format!')
            break
        result1, fps, count, average_speed, frame = tracker.tracking(frame)
        result = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        
        if not FLAGS.dont_show:
            cv2.imshow("Output Video", result)
        
        if cv2.waitKey(1) & 0xFF == ord('q'): break
    cv2.destroyAllWindows()

if __name__ == '__main__':
    try:
        app.run(main)
    except SystemExit:
        pass
