# TimeLapse
A python helper for creating a time lapse.

**SendImage.py**

Uses opencv to take an image and then sends the image to the receiver using a REST API.

**ReceivedImage.py**

Receives an image via a REST endpoint decodes the image and saves it in a folder named images with a unique name.