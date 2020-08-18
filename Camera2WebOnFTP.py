"""
Access IP Camera in Python OpenCV
contact: zekeriyyademirci61@gmail.com

"""

import cv2
import time
from datetime import datetime
from ftplib import FTP
from io import BytesIO

# Use the next line if your camera has a username and password
# stream = cv2.VideoCapture('protocol://username:password@IP:port/1')
streamCam1 = cv2.VideoCapture("rtsp://username:passwd@192.168.10.118:554/cam/realmonitor?channel=1&subtype=0")

fpsLimit = 0.5 # set time limit

startTime = time.time()

while True:
    # start reading frame
    rCam1, frameCam1 = streamCam1.read()

    nowTime = time.time()
    if (int(nowTime - startTime)) >= fpsLimit:
        print("current time: "+str(nowTime))
        # for see the frame coming from IP Camera, can use imshow()
        #cv2.imshow('IP Camera stream', frame)
        # for the store frame w,th .jps ext on your local
        #cv2.imwrite('C:/Users/zekeriyya/Desktop/NodeVideo/test/cam' + timeStr + '.jpg', frame)

        ## write frames data to FTP server
        ftp = FTP('DOMAIN-NAME', 'USERNAME', 'PASSWD')

        # store Cam1 frame on memory not local
        retval, buffer = cv2.imencode('.jpg', frameCam1)
        file = BytesIO(buffer)
        ftp.storbinary('STOR /httpdocs/cam1/camera1.jpg', file)  # send the file
        file.close()  # close file and FTP

        ftp.quit()

        startTime = time.time() # reset time

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

stream.release()
cv2.destroyAllWindows()

