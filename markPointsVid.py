
import cv2
import numpy as np
import pandas as pd
import csv
import json

mouse_pts = []
camDict = {}
camDict['camera_info'] = []

def get_mouse_points(event, x, y, flags, param):

    global mouse_pts
    
    if event == cv2.EVENT_LBUTTONDOWN:
        
        #select top view region with 4 points     
        if len(mouse_pts) < 4:
            cv2.circle(image, (x, y), 5, (0, 0, 255), 10)
            cv2.imshow(name,image)
        
        else:
            cv2.circle(image, (x, y), 5, (255, 0, 0), 10)
            cv2.imshow(name,image)    

        #select two points in horizontal direction parallel to horizontal line of the region and vertical direction parallel to vertical of the region
        if len(mouse_pts) >= 1 and len(mouse_pts) <= 3:
            cv2.line(image, (x, y), (mouse_pts[len(mouse_pts)-1][0], mouse_pts[len(mouse_pts)-1][1]), (70, 70, 70), 2)
            cv2.imshow(name,image)
            if len(mouse_pts) == 3:
                cv2.line(image, (x, y), (mouse_pts[0][0], mouse_pts[0][1]), (70, 70, 70), 2)
                cv2.imshow(name,image)
        if "mouse_pts" not in globals():
            mouse_pts = []
        mouse_pts.append((x, y))



def captureFrame(video,cam_name):
        global mouse_pts, name ,image
        
        #capture video
        cap = cv2.VideoCapture(video)
        
        #read first frame
        ret,frame = cap.read()

        #resize frame captured
        frame = cv2.resize(frame,(640,480))

        #call mouse click function till 7 points are marked
        while len(mouse_pts)<=7:
            image = frame
            cv2.namedWindow(name)
            cv2.setMouseCallback(name,get_mouse_points)    
            cv2.imshow(name,image)
            cv2.waitKey(1)
            if len(mouse_pts) == 7:
        
                cv2.destroyWindow(name)
                break
        
           
        points = mouse_pts  
        mouse_pts = []
        
        #append points marked and camera info to a dictionary
        camDict['camera_info'].append({'name': cam_name,'ip': video,'roi':points})

if __name__ == "__main__":
    video = "fm1.mp4"
    name = video.strip(".mp4")
    
    captureFrame(video,name)
    
    #dump camera info all cameras to text file using json
    with open ("cam_info.txt",'w') as infile:
        json.dump(camDict,infile)

    