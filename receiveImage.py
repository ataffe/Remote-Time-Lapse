from flask import Flask, request, Response
import jsonpickle
import numpy as np
import cv2
import os
from datetime import datetime

# Initialize the Flask application
app = Flask(__name__)

# route http posts to this method


@app.route('/image/add', methods=['POST'])
def receive_image():
	r = request
	# Convert string of image data to unit8
	np_array = np.frombuffer(r.data, np.uint8)

	# decode image
	image = cv2.imdecode(np_array, cv2.IMREAD_COLOR)
	image_name = get_image_name()

	if not os.path.exists("images"):
		print("Making new directory.")
		os.makedirs("images")

	# Save the image
	print("Saving image as: {}".format("images/" + image_name))
	cv2.imwrite("images/" + image_name, image)

	# Create the response
	response = {'message': 'image {} received. size={}x{}'.format(image_name, image.shape[1], image.shape[0])}

	# encode response using json pickle
	response_pickled = jsonpickle.encode(response)

	return Response(response=response_pickled, status=200, mimetype='application/json')


def get_image_name():
	# Image name format TL_<dd/mm/YY>+<H:M:S>
	now = datetime.now()
	date_string = now.strftime("%d-%m-%Y_%H-%M-%S")
	return "TL" + "_" + date_string + ".jpg"


# start flask app
app.run(host="0.0.0.0", port=5000)

