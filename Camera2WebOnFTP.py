"""Access IP Camera in Python OpenCV"""
"""
contact: zekeriyyademirci61@gmail.com
"""

import cv2
import time
from datetime import datetime
from ftplib import FTP
from io import BytesIO

# Use the next line if your camera has a username and password
# stream = cv2.VideoCapture('protocol://username:password@IP:port/1')
streamCam1 = cv2.VideoCapture("rtsp://admin:ifarlab1@192.168.8.118:554/cam/realmonitor?channel=1&subtype=0")
streamCam2 = cv2.VideoCapture("rtsp://admin:ifarlab1@192.168.8.119:554/cam/realmonitor?channel=1&subtype=0")
fpsLimit = 0.5 # set time limit
startTime = time.time()
while True:
    rCam1, frameCam1 = streamCam1.read()
    rCam2, frameCam2 = streamCam2.read()

    nowTime = time.time()
    if (int(nowTime - startTime)) >= fpsLimit:
        print("current time: "+str(nowTime))
        # do other cv2 stuff....
        #cv2.imshow('IP Camera stream', frame)
        #dt=datetime.now()
        #timeStr=str(dt.year)+"."+str(dt.month)+"."+str(dt.day)+"_"+str(dt.hour)+"."+str(dt.minute)+"."+str(dt.second)+"."+str(dt.microsecond)
        #cv2.imwrite('C:/Users/zekeriyya/Desktop/NodeVideo/test/cam' + timeStr + '.jpg', frame)

        ## write frames data to FTP server
        ftp = FTP('ifarlab.evobulut.com', 'Ajk323NU77h2d', '$547Xmyn')

        # store Cam1 frame on memory
        retval, buffer = cv2.imencode('.jpg', frameCam1)
        file = BytesIO(buffer)
        ftp.storbinary('STOR /httpdocs/cam1/camera1.jpg', file)  # send the file
        file.close()  # close file and FTP


        # store Cam2 frame on memory
        retval, buffer = cv2.imencode('.jpg', frameCam2)
        file = BytesIO(buffer)
        ftp.storbinary('STOR /httpdocs/cam2/camera2.jpg', file)  # send the file
        file.close()  # close file and FTP

        ftp.quit()

        startTime = time.time() # reset time

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

stream.release()
cv2.destroyAllWindows()

