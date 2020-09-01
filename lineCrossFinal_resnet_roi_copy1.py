# -*- coding: utf-8 -*-
"""
Created on Fri Jul 26 12:19:17 2019

@author: Asus
"""
import cv2
import numpy as np
import time
import threading
from datetime import datetime
import queue
from datetime import date
import os
#from mobilenet_ssd_python import main_ssd
import pandas as pd
from playsound import playsound
import sys
#from notifications_final import *
from notify_lineCross import *
import math
from firebaseconfig import db, storage
gi.require_version('Notify', '0.7')
from gi.repository import Notify
from PIL import Image

global totalCount, totalAttempts
totalCount = 0
totalAttempts = 10
totalStreams = 0


##threading sub class##

class LineCrossing(threading.Thread):
    def __init__(self, name, rtsp, line1, line2, region, case, slope):

        threading.Thread.__init__(self)
        self.NAME = name
        self.RTSP = rtsp
        self.LINE1 = line1
        self.LINE2 = line2
        self.REGION = region
        self.CASE = case
        self.SLOPE = slope
        # self.LIVESTREAM = livestream
        # self.THRESHOLD = threshold
        # self.LOCATION = location     # to store position of livestream windows on screen
        
    def run(self):
        global totalCount,totalAttempts
        #main_ssd(self.RTSP)
        detectPeople(self.NAME, self.RTSP, self.LINE1, self.LINE2, self.REGION, self.CASE, self.SLOPE)
        # self.LIVESTREAM,
        #              self.THRESHOLD,self.LOCATION)
        
        #restart process if feedloss occurs
        t = time.localtime()
        currentTime = time.strftime("%H:%M:%S", t)
        count = 0   #variable to track no of attempts for restarting a thread
        while count < totalAttempts:
            
            if feedFlag == 1:

                count+=1
                totalCount+=1
                #main_ssd(self.RTSP)
                print("restarting %s "%self.NAME)
                detectPeople(self.NAME, self.RTSP, self.LINE1, self.LINE2, self.REGION, self.CASE, self.SLOPE)
                            #  self.LIVESTREAM, self.THRESHOLD, self.LOCATION)
        if count == 10:
            #check_location(os.path.join(os.getcwd(),"LineCrossing",str(datetime.now()).split(' ')[0]))
            print("camera %s not working"%self.NAME)
            fileName = "./LineCrossing/"+str(date.today())+"/NotWorking.txt"
            with open (fileName,'a') as infile:
                infile.write("Camera %s not working at %s\n"%(self.NAME,str(currentTime)))   
        cv2.destroyAllWindows()

    def get_id(self):
        if hasattr(self, '_thread_id'):
            return self._thread_id
        for id, thread in threading._active.items():
            if thread is self:
                return id

## Function to create the date wise and camera name folders ##
def check_location(location):
    if not os.path.exists(location):
        try:
            os.makedirs(location)
        except:
            print('Unable to create directory')


## to check if event occurred or not##
def checkCase(d1, d2, case):
    if case == 1 or case == 3:
        if d1 < 0 and d2 > 0:
            tFlag = 1
        elif d1 < 0 and d2 < 0:
            tFlag = 2
        else:
            tFlag = 0

    if case == 2 or case == 4:
        if d1 > 0 and d2 < 0:
            tFlag = 1
        elif d1 > 0 and d2 > 0:
            tFlag = 2
        else:
            tFlag = 0

    return tFlag


## implementation of line crossing ##
def detectPeople(name, rtsplink, line1, line2, region, case, slope):
    global direc, feedFlag, liveStream_frame, liveStream_name, event_occured, eventStream_path, eventStream_frame, livestream_loc 
    frame_queue = queue.Queue(maxsize=0)
    
    # flags initialisation
    eventFlag = False                       # If event occurs
    liveStream_frame = None                 # camera frame if livestream is on
    liveStream_name = None                  # camera name if livestream is on
    event_occured = False
    feedFlag = 0                            # Flag to check feedloss
    tresFlag = 0                            # Flag to check trespassing
    countFrame = 0                          # Count to skip frames to reduce fps
    eventStream_frame = None                #event frame
    eventStream_path = None                 #event path

    check_location(os.path.join(os.getcwd(), "LineCrossing", str(datetime.now()).split(' ')[0], str(name)))

    ### RESNET FINAL PIPELINE ###
    #Input_vid = "filesrc location=1.ts ! tsdemux ! queue ! h264parse ! nvv4l2decoder ! m.sink_0 nvstreammux name=m batch-size=1 width=640 height=480 ! nvvidconv ! video/x-raw, format=RGBA ! nvvideoconvert ! nvinfer config-file-path=/opt/nvidia/deepstream/deepstream-4.0/samples/configs/deepstream-app/config_infer_primary_nano.txt ! nvvideoconvert ! nvdsosd ! nvvideoconvert ! capsfilter caps=video/x-raw,format=BGRx ! videoconvert !  appsink"
    #Input_vid = "filesrc location=RingRoad4.ts ! tsdemux ! queue ! h264parse ! nvv4l2decoder ! m.sink_0 nvstreammux name=m batch-size=1 width=640 height=480 ! nvinfer config-file-path=/home/omni/Downloads/deepstream_sdk_v4.0.1_x86_64/samples/configs/deepstream-app/config_infer_primary.txt ! nvtracker ll-config-file=tracker_config.yml ll-lib-file=/opt/nvidia/deepstream/deepstream-4.0/lib/libnvds_mot_klt.so ! nvvideoconvert ! nvdsosd ! nvvideoconvert ! capsfilter caps=video/x-raw,format=BGRx ! videoconvert ! appsink"

    Input_vid = "rtspsrc location="+ rtsplink+ " ! rtph264depay ! h264parse ! nvv4l2decoder ! m.sink_0 nvstreammux name=m batch-size=1 width=640 height=480 ! nvinfer config-file-path=/home/omni/Downloads/deepstream_sdk_v4.0_x86_64/samples/configs/deepstream-app/config_infer_primary.txt ! nvvideoconvert ! nvdsosd ! nvvideoconvert ! capsfilter caps=video/x-raw,format=BGRx ! videoconvert !  appsink"
    print(Input_vid)
    try:
        cap = cv2.VideoCapture(Input_vid)
        #cap.set(cv2.CAP_PROP_BUFFERSIZE, 3)
    except Exception as e:
        print("Exception raised",e)
        raise e

    line1 = (int(line1[0].split(',')[0]), int(line1[0].split(',')[1]), int(line1[1].split(',')[0]), int(line1[1].split(',')[1]))
    line2 = (int(line2[0].split(',')[0]), int(line2[0].split(',')[1]), int(line2[1].split(',')[0]), int(line2[1].split(',')[1]))

    if slope != 'null':
        const1 = line1[1] - slope * line1[0]  # to find eq of lines (y = mx + const)
        const2 = line2[1] - slope * line2[0]

    while True:
        ret,frame_org = cap.read()
        countFrame += 1
        check_location(os.path.join(os.getcwd(),"LineCrossing",str(datetime.now()).split(' ')[0],str(name)))
        if countFrame%1 == 0:  # to skip frames to reduce fps
            if ret == True:

                pts = np.array(region)
                
                rect = cv2.boundingRect(pts)
                x1,y1,w1,h1 = rect
                cropped = frame_org.copy()
                
                mask = np.zeros(cropped.shape[:2], np.uint8)
                cv2.drawContours(mask, [pts], -1, (255, 255, 255), -1, cv2.LINE_AA)
                
                dst = cv2.bitwise_and(cropped, cropped, mask=mask)
                
                bg = np.ones_like(cropped, np.uint8)*255
                cv2.bitwise_not(bg,bg, mask=mask)
                frame = bg+ dst
                
                # define range of blue color in HSV for identification of person class
                lower_blue = np.array([0, 0, 255])
                upper_blue = np.array([0, 0, 255])

                # Threshold the HSV image to get only blue colors
                maskb = cv2.inRange(frame_org, lower_blue, upper_blue)
                
                _,cnts,_ = cv2.findContours(maskb.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
                count = 0
                
                for c in cnts:                    
                    
                    M = cv2.moments(c)
                    if M["m00"]!=0:
                        
                        peri = cv2.arcLength(c, True)
                        approx = cv2.approxPolyDP(c, 0.03 * peri, True)
                        
                        if len(approx) == 4:
                            (x, y, w, h) = cv2.boundingRect(approx)
                            count+=1
                            lwrCtr = (int(x+w/2),y+h)   ##lower centre point for tracking line crossing
                            
                            ##### exception handling of false detections ########
                            if (name == "RingRoad19") and ((88-5,190-5) < lwrCtr < (88+5,190+5) or (222-5,138-5) < lwrCtr < (222+5, 138+5)):
                                continue
                            elif (name == "RingRoad21") and ((286-5,312-5) < lwrCtr < (286+5,312+5)) or ((160-5,148-5) < lwrCtr < (222-5,148-5)):
                                continue
                            elif (name == "RingRoad20") and ((229-5,206-5) < lwrCtr < (229+5,206+5)):
                                continue
                            elif (name == "RingRoad15") and ((49-4,142-4) < lwrCtr < (149+4,142+4)):
                                continue
                            else:
                                if x1+5 <lwrCtr[0] < x1+w1-5 and y1+5< lwrCtr[1] <y1+h1-5: 
                                    cv2.circle(frame_org,lwrCtr,2,(200,200,105),-1)       
                            
                                    if slope != 'null':
                                        dist = ((slope) * (lwrCtr[0]) - (lwrCtr[1]))                
                                        d1 = (dist + (const1))                              #distance of the object from warning line
                                        d2 = (dist + (const2))                              #distance of the object from critical line
                                    else:
                                        d1 = lwrCtr[0] - line1[0][0]
                                        d2 = lwrCtr[0] - line2[0][0]

                                    tresFlag = checkCase(d1, d2, case)
                
                ## mark ROI on the frame
                copy = frame_org.copy()
                for i in range(len(region)-1):                  
                    cv2.line(copy,(region[i][0],region[i][1]),(region[i+1][0],region[i+1][1]),(0,255,0),2)
                    cv2.line(copy,(region[len(region)-1][0],region[len(region)-1][1]),(region[0][0],region[0][1]),(0,255,0),2)
                
                cv2.line(copy, (line1[0], line1[1]), (line1[2], line1[3]), (0, 255, 255), 2)   # mark the warning line
                cv2.line(copy, (line2[0], line2[1]), (line2[2], line2[3]), (0, 0, 255), 2)     # mark the critical line
                
                frame_org = copy
                
                #### warning notification ####
                if tresFlag == 1:
                    today = str(date.today())
                    print("warning at", name)
                    frame_name = str(datetime.now().strftime("%H-%M-%S"))
                    cv2.putText(frame_org, "WARNING", (10, 25), cv2.FONT_HERSHEY_SIMPLEX, 1, (200, 0, 100), 4)
                    db.child('event').push({ "date": today, "type": "warning", "camera_name": name, "activity": "linecrossing" })
                    cv2.imwrite(os.path.join(os.getcwd(), "LineCrossing", today, name,'Warning_alert_%s.jpg' % frame_name), frame_org)
                    img = Image.fromarray(frame_org)
                    # print(type(im))
                    # imageBlob = bucket.blob('Warning_alert_%s.jpg' % frame_name)
                    # imageBlob.upload_from_filename(os.path.join(os.getcwd(), "LineCrossing", today, name))
                    img_path = "LineCrossing"+'/'+today+'/'+name+'/Warning_alert_%s.jpg' % frame_name
                    storage.child(img_path).put(os.path.join(os.getcwd(), "LineCrossing", today, name,'Warning_alert_%s.jpg' % frame_name))
                    img_url = storage.child(img_path).get_url(None)
                    db.child('event').push({ "date": today, "type": "warning", "camera_name": name, "activity": "linecrossing", "img_url": img_url })
                    os.remove(os.path.join(os.getcwd(), "LineCrossing", today, name,'Warning_alert_%s.jpg' % frame_name))
                    tresFlag = 0

                #### Critical notification ####
                elif tresFlag == 2:
                    cv2.putText(frame_org, "CRITICAL", (10, 25), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 4)
                    today = str(date.today())
                    
                    # Save frame with time for critical event
                    frame_name = str(datetime.now().strftime("%H-%M-%S"))
                    
                    dir_logs = "LineCrossing"+'/'+today+'/'+name
                    list_of_files = glob.glob(dir_logs+"//Tresspass_alert_%s_*"%name) # * means all if need specific format then *.csv
                    if len(list_of_files )!=0:
                        latest_file = max(list_of_files, key=os.path.getctime)
                        #print("name",latest_file)
                        latest_file_time = os.path.getctime(latest_file)
                        saved_time = datetime.fromtimestamp(latest_file_time)
                        currentTime = datetime.now()
                        time_diff = (currentTime - saved_time).total_seconds()
                    else:
                        time_diff = -100
                    
                    image_path = os.path.join(os.getcwd(), "LineCrossing", today, name,'Tresspass_alert_%s_%s.jpg' % (name,frame_name))
                    if not os.path.exists(image_path):
                        
                        #### display notifications at an interval of 60 sec from previous alarm #####
                        if time_diff >60 or time_diff == -100:
                            cv2.imwrite(image_path, frame_org)
                            frame_queue.put(image_path)
                                      #add image path to queue
                            # storage.child(os.path.join("LineCrossing", today, name, 'Tresspass_alert_%s_%s.jpg' % (name,frame_name))).put(frame_org)
                            img_path = os.path.join("LineCrossing", today, name, 'Tresspass_alert_%s_%s.jpg' % (name,frame_name))
                            storage.child(img_path).put(image_path)
                            img_url = storage.child(img_path).get_url(None)
                            db.child('event').push({ "date": today, "type": "critical", "camera_name": name, "activity": "linecrossing", "img_url": img_url })
                            eventFlag = True                        #raise event flag
                            tresFlag = 0                            #reset trespass flag
                            
                            #### Image pop-up ######
                            try:
                                notify_obj = ImageNotification(name)
                            except:
                                pass

                            #### Sound Alarm #####
                            try:
                                for i in range(6):
        	                        playsound('beep-02.mp3')
                            except:
                                pass

                            #### SMS alarm ######
                            try:
                                alert_message = 'WARNING TRESPASSING ACTIVITY HAS BEEN DETECTED ON CAMERA %s' % name   #text for sms
                                sendSMS(alert_message)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 
                            except:
                                pass

                            #### EMail Alarm #####
                            try:
                                email_alert(name, rtsplink, ' WARNING!! Tresspass Event ')
                            except:
                                #Notify.init("Internet Connection")
                                #notification = Notify.Notification.new("Internet might not be working") 
                                #notification.show()
                                pass

                else:
                    cv2.putText(frame_org, "OK", (10, 25), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 4)

                ##### send frame for livestreaming to main thread ######
                # if livestream.lower() == 'yes':
                liveStream_name = name          #pass camera name for livestream
                liveStream_frame = frame_org    #pass camera frame for livestream
                #     livestream_loc = location       #pass window location for livestream
            
            #### if no frame received, attempt to restart #####    
            else:
                feedFlag = 1
                cv2.destroyAllWindows()
                break

    cv2.destroyAllWindows()
    cap.release()


def lineCross():
    global feedFlag, liveStream_frame, liveStream_name, event_occured, eventStream_path, eventStream_frame, totalCount,totalAttempts, livestream_loc

    allcams = db.child('line Crossing').get()
    camdata = []
    for cam in allcams.each():
        camdata.append(cam.val())
        
    # for cam in camdata
    config_cams = []
    for i, cam in enumerate(camdata):
        if(cam.get("configuration", None) != None):
            config_cams.append(cam)
    # print(config_cams)

    # camList = []                                                # to store camera details from the database
    print(config_cams)
    threads = len(config_cams)  # Number of threads to create
    jobs = []     
    for i in range(threads):
        reg = ([])
        IP = config_cams[i]['ipaddress']
        Ch = config_cams[i]['channel']
        UI = config_cams[i]['userid']
        cam_name = config_cams[i]['camera_name']
        psd = "admin123"
        line1 = config_cams[i]['configuration']['line1']
        line2 = config_cams[i]['configuration']['line2']
        roi = config_cams[i]['configuration']['regionPts']
        case = config_cams[i]['configuration']['case']
        slope = config_cams[i]['configuration']['slope']
        roi_list = []
        for i in range(len(roi)):
            pt = []
            pt.append(int(roi[i].split(', ')[0]))
            pt.append(int(roi[i].split(', ')[1]))
            roi_list.append(pt)
            
        
        rtsplink = "rtsp://" + UI + ':' + psd + '@' + IP + "/Streaming/Channels/"+ Ch

        thread = LineCrossing(cam_name, rtsplink, line1, line2, roi_list, case, slope)
        thread.setName(cam_name)
        jobs.append(thread)


    # To start threads appended in the list 'jobs'
    for lineThread in jobs:
        lineThread.start()
        time.sleep(2)

    print('Started all Threads')
    
    ###########livestream and event pop-up section################ 
    # while True:
        
    #     try:
    #         if totalCount == threads*totalAttempts:         # if the no of restart attempts have exhusted for all threads, end program
    #             break
            
    #         #### display livestream 
    #         if liveStream_name != None and  len(liveStream_frame.shape)>0:      #check status of global variables for livestreaming
    #             try:
    #                 cv2.namedWindow('Livestream for : {}'.format(liveStream_name))
    #                 # cv2.moveWindow('Livestream for : {}'.format(liveStream_name),livestream_loc[0],livestream_loc[1])
    #                 cv2.imshow('Livestream for : {}'.format(liveStream_name), cv2.resize(liveStream_frame,(150,150)))
    #                 cv2.waitKey(1)
    
    #             except Exception as e:
    #                 print("error in livestream")
    #                 cv2.destroyAllWindows() # if error in event show window, destroy that window    
                    
    #     except KeyboardInterrupt:           # to exit script with ctrl+c command

    #         cv2.destroyAllWindows()
    #         quit()
    #         sys.exit()
    # cv2.destroyAllWindows()


# lineCross(os.getcwd()+"/LineCrossing/cam1.csv")
#lineCross(os.getcwd()+"/camera_details.csv")
