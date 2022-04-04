from __future__ import print_function
import json
import requests
import cv2
import schedule
import time
import sys
import getopt


def send_image(cam, host, port):
	addr = 'http://{}:{}'.format(host, port)
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


def print_help_message():
	print("Usage: transmitter.py --host <hostname> --port <port>")


if __name__ == "__main__":
	receiver_host = ''
	receiver_port = ''
	try:
		opts, args = getopt.getopt(sys.argv[1:], "h", ["host=", "port="])
	except getopt.GetoptError:
		print_help_message()
		sys.exit(2)
	for opt, arg in opts:
		if opt == '-h':
			print_help_message()
			sys.exit()
		elif opt in "--host":
			receiver_host = arg
		elif opt in "--port":
			receiver_port = arg

	if not receiver_host:
		print("Missing receiver host.")
		print_help_message()
		sys.exit()

	if not receiver_port:
		print("Missing receiver port, defaulting to 5000.")
		receiver_port = "5000"

	print("Starting time lapse transmitter with host: {} and port: {}".format(receiver_host, receiver_port))
	camera = start_camera()
	send_image(camera, receiver_host, receiver_port)
	schedule.every(10).seconds.do(send_image, cam=camera, host=receiver_host, port=receiver_port)
	print("Time lapse started.")

	try:
		while True:
			schedule.run_pending()
			time.sleep(1)
	except KeyboardInterrupt:
		print("Program ended gracefully.")
		camera.release()
