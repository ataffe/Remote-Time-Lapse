import cv2
import numpy as np


def print_mean():
	camera = cv2.VideoCapture(0)
	if not camera.isOpened():
		print("Unable to start video.")
		exit()

	while camera.isOpened():
		ret, image = camera.read()
		if not ret:
			print("Unable to take picture, exiting.")
			camera.release()
			exit()

		print("Mean value is {}".format(np.mean(image)))
		cv2.imshow('Image', image)

		if cv2.waitKey(25) & 0xFF == ord('q'):
			break

	cv2.destroyAllWindows()
	camera.release()


if __name__ == "__main__":
	print_mean()
