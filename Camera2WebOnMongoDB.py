"""
## Access IP Camera in Python OpenCV
## Getting a frame per second
## Getting info from MsSQL
## Combine all datas and write remote server mongoDB database

contact: zekeriyyademirci61@gmail.com

"""

import cv2
import base64
import pyodbc
import pymongo
import datetime
import threading

### MsSQL Server Connection info
driver="SQL Server"
server="serverName"
db="dbname"
user="username"
password="passwd"

## local IP Camera connection string
cam1Str = "rtsp://admin:passwd@192.168.10.118:554/cam/realmonitor?channel=1&subtype=0"

## a string variable that store the base64 code of a frame
cam1Base64Str="null"
## a string that store individual info getting from MsSQL database
insertStr="null"

## a function that capture a frame coming from local IP Camera and convert it to base64 code and assign it on cam1Base64Str
def getBase64FrameFromCamera(connectionString):
    # Use the next line if your camera has a username and password
    # stream = cv2.VideoCapture('protocol://username:password@IP:port/1')
    
    # capture a video
    streamCam = cv2.VideoCapture(connectionString)
    retval, image = streamCam.read()
    
    # store a frame with .jpg extension on memory not local
    retval, buffer = cv2.imencode('.jpg', image)
    # convert image to base64 code
    jpg_base64 = base64.b64encode(buffer)

    global cam1Base64Str
    
    # assigment
    cam1Base64Str=jpg_base64.decode('ascii')

    streamCam.release()

# a function that connect a MsSQL database and get information , parse them and assign it all to "insertStr"
def getStatusDataFromMsSQL(cursor):
    cursor.execute('select * from Status')
    for row in cursor:
        str=row[1].replace("\\","")
        strArr=str.split(",")

        # parsing 
        Datetime=datetime.datetime.now().strftime("%m/%d/%Y %H:%M:%S")
        Prd_DateTime_Value=(strArr[0].split('"'))[3]
        positionX=(strArr[1].split('"'))[6]
        positionY=(strArr[2].split('"'))[3]
        orientationZ = (strArr[3].split('"'))[3]
        orientationW = (strArr[4].split('"'))[3]
        lineerX= (strArr[5].split('"'))[3]
        lineerY = (strArr[6].split('"'))[3]
        angularZ = (strArr[7].split('"'))[3]
        timeStampt=(strArr[8].split('"'))[3]
        OTA_Status=(strArr[9].split('"'))[3]
        OTA_OEE = (strArr[10].split('"'))[3]
        RK_Status = (strArr[11].split('"'))[3]
        RK_Status2 = (strArr[12].split('"'))[3]
        HMI_Status = (strArr[13].split('"'))[3]
        HMI_Status2 = (strArr[14].split('"'))[3]

    global insertStr
    insertStr = {"datetime": Datetime,
                 "prd_DateTime_Value": Prd_DateTime_Value,
                 "ID": "1",
                 "positionX": positionX,
                 "positionY": positionY,
                 "orientationZ": orientationZ,
                 "orientationW": orientationW,
                 "linearX": lineerX,
                 "linearY": lineerY,
                 "angularZ": angularZ,
                 "headerStampSec": timeStampt,
                 "OTA_Status": OTA_Status,
                 "OTA_OEE": OTA_OEE,
                 "RK_Status": RK_Status,
                 "RK_Status2": RK_Status2,
                 "HMI_Status": HMI_Status,
                 "HMI_Status2": HMI_Status2
                 }

if __name__ == "__main__":

    # create a MsSQL connection with initial variable
    conn = pyodbc.connect('driver={%s};server=%s;database=%s;uid=%s;pwd=%s' % (driver, server, db, user, password))
    cursor = conn.cursor()

    ### create Mongo & Cloud Connection
    cloudClient = pymongo.MongoClient("mongodb://IPADDRESS", username='USERNAME', password='PASSWORD',
                                      authSource='XXX')
    mydbCloud = cloudClient["dbName"]
    cloudStatus = mydbCloud["CollectionName"]

    
    while (1):
        # creating thread
        t1 = threading.Thread(target=getBase64FrameFromCamera, args=(cam1Str))
        t2 = threading.Thread(target=getStatusDataFromMsSQL, args=(cursor))

        # starting thread 1
        t1.start()
        # starting thread 2
        t2.start()

        # wait until thread 1 is completely executed
        t1.join()
        # wait until thread 2 is completely executed
        t2.join()

        # add frame's base64 code to insertStr dict 
        insertStr["Cam1Base64Code"]=cam1Base64Str

        # all threads completely executed

        # check MongoDB whether has only a record. If it already has a record then update, else insert.
        if (cloudStatus.count({"ID": "1"})):
            cloudStatus.update({"ID": "1"}, insertStr)
        else:
            cloudStatus.insert(insertStr, check_keys=False)  ## writing cloud mongo














