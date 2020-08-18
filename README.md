# Transport-Live-Video-to-Web

In the local area, there is a IP Camera and we aim to live broadcast on our web page. For this purpose we need to transport these frames coming from IP Camera to web server on some way. And we have a two different solution to solve this problem:
#### 1. Using FTP 
The first one is transport a frame that coming from IP Camera to our web server on FTP directly . This way is cheaper to transport. So, when you do not need to store frames on your local, then you can use this way. 

**We use common library as below:**
- **cv2**: to capture frame from IP Camera and convert it to .jpg image
- **ftplib**: to use FTP protocol

#### 2. Using MongoDB
Second way is store a frame that coming from IP Camera to MongoDB database which is located on server.

**We use common library as below:**
- **cv2**: to capture frame from IP Camera and convert it to .jpg image
- **pymongo**: to get MongoDB connection
- **pyodbc**: to get MsSQL connection
- **base64**: to get base64 code of frame
