from __future__ import print_function
import json
import requests
import cv2
import schedule
import time


def send_image():
	addr = 'http://localhost:5000'
	test_url = addr + '/image/test'

	# prepare headers for http request
	content_type = 'image/jpeg'
	headers = {'content-type': content_type}

	capture = cv2.VideoCapture(0)

	ret = None
	image = None
	print("Warming up camera")
	for x in range(5):
		ret, image = capture.read()

	if not ret:
		print("Unable to take picture...exiting.")
		exit()

	# encode the image as a jpeg
	_, encoded_image = cv2.imencode('.jpg', image)

	print("Sending image")
	# send image using http and get response
	response = requests.post(test_url, data=encoded_image.tobytes(), headers=headers)

	# decode response
	if response.text is not None:
		print(json.loads(response.text))
	else:
		print("Response was empty.")

	capture.release()


if __name__ == "__main__":
	schedule.every(30).seconds.do(send_image)

	while True:
		schedule.run_pending()
		time.sleep(1)
