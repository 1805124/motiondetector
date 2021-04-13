# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


import cv2, pandas


#first farme variable initialized 
first_frame=None
status_list=[None,None]
times=[]
df=pandas.DataFrame(columns=["start","End"])

#capturing video will start 
video_capture = cv2.VideoCapture(0)
#while loop start to capture the image continiously
while True:
    check,frame=video_capture.read()
    status=0
    gray=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)#BGR to grayscale change due to light problem 
    gray=cv2.GaussianBlur(gray,(21,21),0)#Gaussian blurr image conversion so that we can detect the part of motion

#for the 1st time the initial image is taken 
    if first_frame is None:
        first_frame=gray
        continue
 #getting the difference between the first image frame and recent image frame  
    delta_frame=cv2.absdiff(first_frame,gray)
    #checking the Threshold crossed or not 
    thresh_delta=cv2.threshold(delta_frame,30,255,cv2.THRESH_BINARY)[1]
    thresh_delta=cv2.dilate(thresh_delta,None,iterations=0)#overriding the threshold function 
    (cnts,_) = cv2.findContours( thresh_delta.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)

    for contour in cnts:
        if cv2.contourArea(contour)<1000:#check if the change value is less than the threshold or not if less then continue
            continue
        else:
            #here the motion is detected 
            status=1
            (x,y,w,h)=cv2.boundingRect(contour)
            #rectange is used to get the part which part is not similer with the first frame
            cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),3)
            cv2.imshow('frame', frame)
            cv2.imshow('capturing', gray)
            cv2.imshow('delta', delta_frame)
            cv2.imshow('thresh', thresh_delta)
            key=cv2.waitKey(1)
            #to stop the detection window we have to press the q so that we can exit from the loop
            if key==ord('q'):
                exit()
#atlast al the opened window is closed and captring video is stopped 
video_capture.release()
cv2.destroyAllWindows()
#This is just a small model which will be integrate with other part also 
