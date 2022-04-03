from __future__ import print_function
import json
import requests
import cv2
import schedule
import time


def send_image(cam):
	addr = 'http://localhost:5000'
	url = addr + '/image/add'

	# prepare headers for http request
	content_type = 'image/jpeg'
	headers = {'content-type': content_type}

	ret = None
	image = None
	ret, image = cam.read()

	if not ret:
		print("Unable to take picture...exiting.")
		exit()

	# encode the image as a jpeg
	_, encoded_image = cv2.imencode('.jpg', image)

	print("Sending image")
	# send image using http and get response
	response = requests.post(url, data=encoded_image.tobytes(), headers=headers)

	# decode response
	if response.text is not None:
		print(json.loads(response.text))
	else:
		print("Response was empty.")


def start_camera():
	cap = cv2.VideoCapture(0)
	cap.set(cv2.CAP_PROP_AUTOFOCUS, 0)
	cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
	cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
	return cap


if __name__ == "__main__":
	print("Starting time lapse.")
	camera = start_camera()
	send_image(camera)
	schedule.every(30).seconds.do(send_image, cam=camera)
	print("Time lapse started.")

try:
	while True:
		schedule.run_pending()
		time.sleep(1)
except KeyboardInterrupt:
	print("Releasing camera")
	camera.release()
