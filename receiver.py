from flask import Flask, request, Response
import jsonpickle
import numpy as np
import cv2
import os
from datetime import datetime
import glob

# Initialize the Flask application
app = Flask(__name__)


# Heart beat for checking is server is up.
@app.route('/image/heart_beat', methods=['GET'])
def heat_beat():
	response = {"message": "ok"}
	pickled_response = jsonpickle.encode(response)
	return Response(response=pickled_response, status=200, mimetype='application/json')


# Function to create the time lapse video
@app.route('/image/create_time_lapse', methods=['POST'])
def create_time_lapse():

	images = sorted(glob.glob('images/*.jpg'))
	print("Total number of images: {}".format(len(images)))
	make_directory_if_missing("videos")
	# Calculate frame rate in frames per second
	# if len(images) < 30:
	# 	frame_rate = 2
	# else:
	# 	frame_rate = 30

	frame_rate = 30
	data = request.json
	if "frame_rate" in data.keys():
		frame_rate = data["frame_rate"]

	width, height = get_image_size(images[0])
	if "width" in data.keys():
		width = data["width"]
	if "height" in data.keys():
		height = data["height"]
	fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
	video_name = "videos/" + get_video_name("")
	if "name_suffix" in data.keys():
		video_name = "videos/" + get_video_name("_" + data["name_suffix"])
	print("Generating video name: {}, width: {}, height: {}, frame rate: {}".format(video_name, width, height, frame_rate))
	video = cv2.VideoWriter(video_name, fourcc, frame_rate, (width, height))

	for ctr in range(len(images)):
		# Load image
		image = cv2.imread(images[ctr])
		# Match the size of the image.
		image = cv2.resize(image, (width, height))
		video.write(image)

	video.release()
	print("Created time lapse.")

	response = {"message": "Created time lapse from {} images.".format(len(images))}
	pickled_response = jsonpickle.encode(response)
	return Response(response=pickled_response, status=200, mimetype='application/json')


# route http posts to this method
@app.route('/image/add', methods=['POST'])
def receive_image():
	r = request
	# Convert string of image data to unit8
	np_array = np.frombuffer(r.data, np.uint8)

	# decode image
	image = cv2.imdecode(np_array, cv2.IMREAD_COLOR)
	image_name = get_image_name()

	make_directory_if_missing("images")

	# Save the image
	print("Saving image as: {}".format("images/" + image_name))
	cv2.imwrite("images/" + image_name, image)

	# Create the response
	response = {'message': 'image {} received. size={}x{}'.format(image_name, image.shape[1], image.shape[0])}

	# encode response using json pickle
	response_pickled = jsonpickle.encode(response)

	return Response(response=response_pickled, status=200, mimetype='application/json')


def get_image_size(image_raw):
	image = cv2.imread(image_raw)
	return image.shape[1], image.shape[0]


def make_directory_if_missing(name):
	if not os.path.exists(name):
		print("Making new directory named {}".format(name))
		os.makedirs(name)


def get_image_name():
	# Image name format TL_<dd/mm/YY>+<H:M:S>
	now = datetime.now()
	date_string = now.strftime("%d-%m-%Y_%H-%M-%S")
	return "TL_" + date_string + ".jpg"


def get_video_name(suffix):
	now = datetime.now()
	date_string = now.strftime("%d-%m-%Y_%H-%M")
	return "TL_Video_" + date_string + suffix + ".mp4"


# start flask app
app.run(host="0.0.0.0", port=5000)

