"""
## Access IP Camera in Python OpenCV

contact: zekeriyyademirci61@gmail.com

"""

import cv2
import base64
import pyodbc
import pymongo
import datetime
import threading

### MsSQL Server Connection
driver="SQL Server"
server="serverName"
db="dbname"
user="username"
password="passwd"

cam1Str = "rtsp://admin:passwd@192.168.10.118:554/cam/realmonitor?channel=1&subtype=0"

cam1Base64Str,insertStr="null","null"

def getBase64FrameFromCamera(connectionString,id):
    # Use the next line if your camera has a username and password
    # stream = cv2.VideoCapture('protocol://username:password@IP:port/1')
    streamCam = cv2.VideoCapture(connectionString)
    rCam, frameCam = streamCam.read()
    retval, image = streamCam.read()
    retval, buffer = cv2.imencode('.jpg', image)
    jpg_base64 = base64.b64encode(buffer)

    global cam1Base64Str

    cam1Base64Str=jpg_base64.decode('ascii')

    streamCam.release()


def getStatusDataFromMsSQL(cursor):
    cursor.execute('select * from Status')
    for row in cursor:
        str=row[1].replace("\\","")
        strArr=str.split(",")

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

    conn = pyodbc.connect('driver={%s};server=%s;database=%s;uid=%s;pwd=%s' % (driver, server, db, user, password))
    cursor = conn.cursor()

    ### Mongo & Cloud Connection
    cloudClient = pymongo.MongoClient("mongodb://IPADDRESS", username='USERNAME', password='PASSWORD',
                                      authSource='XXX')
    mydbCloud = cloudClient["dbName"]
    cloudStatus = mydbCloud["CollectionName"]


    while (1):
        # creating thread
        t1 = threading.Thread(target=getBase64FrameFromCamera, args=(cam1Str, 1))
        t2 = threading.Thread(target=getStatusDataFromMsSQL, args=(cursor,))

        # starting thread 1
        t1.start()
        # starting thread 2
        t2.start()

        # wait until thread 1 is completely executed
        t1.join()
        # wait until thread 2 is completely executed
        t2.join()

        insertStr["Cam1Base64Code"]=cam1Base64Str

        # all threads completely executed

        if (cloudStatus.count({"ID": "1"})):
            cloudStatus.update({"ID": "1"}, insertStr)
        else:
            cloudStatus.insert(insertStr, check_keys=False)  ## writing cloud mongo














