# TimeLapse Helper
A python helper for creating a time lapse. This script takes pictures at configured intervals and sends them to a receiver running on another computer. 
The receiver then gives each photo a unique name and then saves the images in a folder named "images". A program like Photoshop can be used to combine the images.

The REST API is created using Flask, and images are taken using opencv.

**SendImage.py**

Uses OpenCV to take an image and then sends the image to the receiver using a REST API. The hostname and port must be passed in
as input arguments.

**ReceivedImage.py**

Receives an image via a REST endpoint decodes the image and saves it in a folder named images with a unique name.