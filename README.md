# Remote TimeLapse Creator
This time lapse creator is composed of two python scripts, a transmitter and a receiver.
 It is designed to send images, one at a time, from a transmitter running on one computer to a receiver running on another at a specified interval.
 The receiver then gives each image a unique name (format: "TL_dd-mm-YY_H-M-S"), and then save it to a folder named images. The `create_time_lapse` endpoint
 can be used to create an MP4 time lapse video. Time lapse videos are saved in the "video" folder.
 
<br>

#### How to Use
**Transmitter**   
Run the following commands in a terminal/command prompt. This assumes python and pip are installed. I have tested with Python 3
but it can be tweaked to run with Python 2.
1. `git clone https://github.com/ataffe/TimeLapseHelper.git`
2. `pip install numpy opencv-python schedule`
3. `python transmitter.py --host <host> --port <port> -i <interval in minutes>`   
Replace "host" and "port" with the ip address and port of the receiver.
To get the ip address of the receiver, on the receiver machine run `ipconfig` on Windows and
`ifconfig` on Unix to get the ip address of the machine. 
 
 **Receiver**   
 Run the following commands in a terminal/command prompt.
 1. `git clone https://github.com/ataffe/TimeLapseHelper.git`
 2. `pip install numpy opencv-python jsonpickle Flask`
 3. `python receiver.py`
 
 <br>
 
 **Creating a Time Lapse Video**
 Call `http://host:port/image/create_time_lapse` to generate a time lapse video. This will create a folder named "video"
 and add the time lapse videos to the folder. The naming format for each video is "TL_Video_mm-dd-YY_H-M.mp4"
 
#### REST API Details
**Default Host:** localhost  
**Default Port:** 5000

`POST image/create_time_lapse` - Used for creating a time lapse using the images taken by the sender.

`GET image/heart_beat` - Used for checking that the server is alive.

`POST image/add` - Used to send an image from the sender to the receiver.

The REST API is created using [Flask](https://flask.palletsprojects.com/en/2.1.x/), and images are taken using [OpenCV](https://opencv.org/).

Here is a time lapse I created using this creator:
[![IMAGE ALT TEXT HERE](https://img.youtube.com/vi/weLxdWpJDms/0.jpg)](https://www.youtube.com/watch?v=weLxdWpJDms)
