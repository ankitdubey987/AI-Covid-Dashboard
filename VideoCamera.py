import cv2
from imutils.video import VideoStream
import datetime
import pickle
import time
import numpy as np

class VideoCamera(object):
    def __init__(self,ip):
        self.stream = cv2.VideoCapture(ip)
        time.sleep(3)
    
    def __del__(self):
        self.stream.release()
        cv2.destroyAllWindows()
    
    def predict(self, frame):
        pass

    def getframe(self):
        ret,image = self.stream.read()
        ret,jpeg = cv2.imencode(".jpg",image)
        data = []
        return (jpeg.tobytes())

