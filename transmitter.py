from __future__ import print_function
import json
import requests
import cv2
import schedule
import time
import sys
import getopt


def send_image(cam, host, port):
	if not wait_for_receiver(host, port, 30):
		print("Receiver not found after 60 seconds, exiting")
		exit()

	address = 'http://{}:{}'.format(host, port)
	url = address + '/image/add'

	# prepare headers for http request
	content_type = 'image/jpeg'
	headers = {'content-type': content_type}

	ret = None
	image = None
	# To allow the camera to do its stuff
	for x in range(50):
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


def wait_for_receiver(host, port, num_retries):
	if num_retries <= 0:
		return False

	heart_beat_url = 'http://{}:{}/image/heart_beat'.format(host, port)
	try:
		response = requests.get(heart_beat_url)
		if response.status_code != 200:
			print("No receiver found at {} waiting for receiver to start. Retries left {}".format(heart_beat_url, num_retries - 1))
			time.sleep(10)
			wait_for_receiver(host, port, num_retries - 1)
	except:
		print("No receiver found at {} waiting for receiver to start. Retries left {}".format(heart_beat_url, num_retries - 1))
		time.sleep(10)
		wait_for_receiver(host, port, num_retries - 1)

	return True


def start_camera():
	cap = cv2.VideoCapture(0)
	return cap


def print_help_message():
	print("""Usage: python transmitter.py [OPTIONS]

Takes images at a specified interval and sends them to a receiver.
	
Available options:
--host				The hostname of the receiver e.g. 11.0.0.6 (default is localhost)
--port				The port of the receiver e.g. 5000 (default is 5000)
-i, --interval		The amount of time between images in minutes. (default is 10 minutes)
-h					Displays this help menu.
""")


if __name__ == "__main__":
	receiver_host = ''
	receiver_port = ''
	interval = ''
	try:
		opts, args = getopt.getopt(sys.argv[1:], "hi:", ["host=", "port=", "interval="])
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
		elif opt in ["-i", "--interval"]:
			interval = arg

	if not receiver_host:
		print("Missing receiver host, defaulting to localhost.")
		receiver_host = "localhost"

	if not receiver_port:
		print("Missing receiver port, defaulting to 5000.")
		receiver_port = "5000"

	if not interval:
		print("Missing interval defaulting to every 10 minutes")
		interval = 10

	print("Starting time lapse transmitter with host: {}, port: {}, and interval: every {} minutes.".format(receiver_host, receiver_port, interval))
	camera = start_camera()
	send_image(camera, receiver_host, receiver_port)
	schedule.every(int(interval)).minutes.do(send_image, cam=camera, host=receiver_host, port=receiver_port)
	print("Time lapse started.")

	try:
		while True:
			schedule.run_pending()
			time.sleep(1)
	except KeyboardInterrupt:
		print("Program ended gracefully.")
		camera.release()
