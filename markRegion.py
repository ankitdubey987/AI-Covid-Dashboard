# -*- coding: utf-8 -*-
"""
Created on Mon Jul 29 17:28:17 2019

@author: Asus
"""
import cv2
import numpy as np
import tkinter.messagebox 

#from imutils.video import VideoStream
import math
import os
import csv

global regionFlag,regionPts
regionFlag = 0

def selectPoint (event,x,y,flags,params):
    global point_selected,point,old_point,count,pts,param,regionPts,regionFlag
    
    if event == cv2.EVENT_LBUTTONDOWN:
        if regionFlag == 0:
            point = ([x,y])
            regionPts.append(point)
            cv2.circle(param[0],(x,y),3,(255,0,0),-1)
            for i in range(len(regionPts)-1):
                cv2.line(param[0],(regionPts[i][0],regionPts[i][1]),(regionPts[i+1][0],regionPts[i+1][1]),(0,255,0),2)
            cv2.imshow("selectRegion",param[0])
            
        else:
            param[1]+=1
            #print(param[1])
            if param[1] <= 3:
                point = (x,y)
                param[2].append(point)
                if len(param[2]) == 2:
                    cv2.line(param[0],pts[0],pts[1],(0,0,255),2)  
                    cv2.imshow("MarkCriticalLine",param[0])
                if len(param[2]) == 3:
                    cv2.circle(param[0],(x,y),4,(255,0,0),-1)
                    cv2.imshow("MarkDirection",param[0])
                
def markRoi(video,cam):
    global param,pts,regionFlag,regionPts
    
    case = 0
    cap = (cv2.VideoCapture(video))
    
    try:

        ret,image = cap.read()
        
        image = cv2.resize(image,(640,480))
        gray1 = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        gray1 = cv2.GaussianBlur(gray1, (21, 21), 0)
        
        count = 0
        pts = []
        regionPts = []

        param = [image,count,pts]        
        
        cv2.namedWindow("selectRegion")
        cv2.setMouseCallback("selectRegion",selectPoint)
        cv2.imshow("selectRegion",image)
        cv2.waitKey(0) 
        cv2.destroyAllWindows()

        regionFlag = 1
        #print(regionPts)
        #cv2.line(image,(len(regionPts)-1][0],regionPts[i][1]),(regionPts[i+1][0],regionPts[i+1][1]),(0,255,0),2)
        cv2.line(image,(regionPts[len(regionPts)-1][0],regionPts[len(regionPts)-1][1]),(regionPts[0][0],regionPts[0][1]),(0,255,0),2)

        cv2.namedWindow("MarkCriticalLine")
        cv2.setMouseCallback("MarkCriticalLine",selectPoint)    
        cv2.imshow("MarkCriticalLine",image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        cv2.namedWindow("MarkDirection")
        cv2.setMouseCallback("MarkDirection",selectPoint)    
        cv2.imshow("MarkDirection",image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        regionFlag = 0
        
        try:
            x1 , x2 , x3 = pts[0][0] , pts[1][0] , pts[2][0]         #line end points wrt roi
            y1 , y2 , y3 = pts[0][1] , pts[1][1] , pts[2][1]
        
            if x1 != x2 and y1 != y2:
                slope = float(y1-y2)/float(x1-x2)
                const = y1 - slope*x1              
                distSign = (slope*x3 + const - y3) / (np.sqrt(np.square(slope)+1))
                if y2 >y1:
                    angle = 180-np.degrees(math.atan2((y2-y1),(x2-x1))) 
                else:
                    angle = -1*np.degrees(math.atan2((y2-y1),(x2-x1))) 
            elif x1 == x2 and y1!=y2:
                slope = 'null'
                angle = 90
                distSign = x3-x1
            elif y1 == y2 and x1 != x2:
                slope = 0
                angle = 0
                distSign = y1 - y3
            else:
                print("error,same point")
                #insert tkinter message"    
                
            if angle >=90 and distSign < 0:                                             # line on left side
                case = 1
                x1_warn , x2_warn = x1+30 , x2+30
                y1_warn , y2_warn = y1-30 , y2-30
                
            elif angle >=90 and distSign > 0:                                           # line on right side
                case = 2
                x1_warn , x2_warn = x1-30 , x2-30
                y1_warn , y2_warn = y1+30 , y2+30
                
            elif angle <90 and distSign < 0:                                            # line on right side
                case = 3
                x1_warn , x2_warn = x1-30 , x2-30
                y1_warn , y2_warn = y1-30 , y2-30
                 
            elif angle <90 and distSign > 0:                                            # line on left side
                case = 4
                x1_warn , x2_warn = x1+30 , x2+30
                y1_warn , y2_warn = y1+30 , y2+30
                 
            else:
                print('Error')
                #insert tkinter warning
            
            line1 = ((x1_warn,y1_warn),(x2_warn,y2_warn))   # warning line
            line2 = ((x1,y1),(x2,y2))                       # Critical line
            cv2.line(image,line1[0],line1[1],(0,255,255),2)  
            cv2.line(image,line2[0],line2[1],(0,0,255),2)  
            cv2.imshow("FinalSelection",image)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
            cv2.imwrite(cam+'.jpg',image)
            info = [line1,line2,regionPts,case,slope]
            regionPts = []
            
            '''file_path = os.path.join(os.getcwd(),"LineCrossing","camera_details_ts.csv")
            
            cam = video.split('\\')[-1]
            vid_url = video
            LS = "yes"
            th = 200
            cam_info = [cam,vid_url]+info+[LS]
            cam_info_new = cam_info+[th]

            with open(file_path, "a",newline ="") as csv_file:
                writer = csv.writer(csv_file)
                writer.writerow(cam_info_new)'''
            
        except:
            info = "null_pts"
    except:
        info = "null_rtsp"
    # print(info)
    return info
#markRoi(r"D:\FACE_DETECT_RECOG_webel\webel_data\trespassVideo\ringroad21\3.ts")