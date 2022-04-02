from flask import Flask, request, Response
import jsonpickle
import numpy as np
import cv2
import os

counter = 0
# Initialize the Flask application
app = Flask(__name__)

# route http posts to this method


@app.route('/image/test', methods=['POST'])
def receive_image():
	global counter
	r = request
	# Convert string of image data to unit8
	np_array = np.frombuffer(r.data, np.uint8)

	# decode image
	image = cv2.imdecode(np_array, cv2.IMREAD_COLOR)

	if not os.path.exists("images"):
		print("Making new directory.")
		os.makedirs("images")
	cv2.imwrite("images/test" + str(counter) + ".jpg", image)
	counter = counter + 1

	response = {'message': 'image received. size={}x{}'.format(image.shape[1], image.shape[0])}

	# encode response using json pickle
	response_pickled = jsonpickle.encode(response)

	return Response(response=response_pickled, status=200, mimetype='application/json')


# start flask app
app.run(host="0.0.0.0", port=5000)

