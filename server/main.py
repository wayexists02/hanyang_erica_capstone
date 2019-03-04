
import sys
import numpy as np
import cv2
import threading as th
from Server import Server

host = "192.168.137.1"
port = 13333
num_step = 8
num_classes = 4
image_width = 128
image_height = 128
image_channel = 3

sys.path.append("../")

from ai.AI import AI

image = None
ok = True

def image_show():
	global image
	global ok

	while ok:
		if image is not None:
			cv2.imshow("test", cv2.resize(image, dsize=(240, 240)))
			cv2.waitKey(1000 // 60)

def main(args):
	global image
	global ok

	print("Start server!")
	server = Server()
	server.open(host, port)

	ai = AI()
	ai.setup(num_step, num_classes)

	# debug
	t = th.Thread(target=image_show)
	t.start()

	try:
		while True:
			image_arr = np.zeros((1, num_step, image_height, image_width, image_channel))
			cnt = 0
			index = 0
			
			while cnt < num_step:

				image = server.wait_for_image()
				if image is None:
					continue

				cv2.imwrite(f"./test/{index}.jpg", image)
				index += 1

				image_arr[0, cnt] = image
				cnt += 1

				image = None

			result = ""

			if ai.detect_trash(image_arr[0]) is False:
				result += str(0)
			else:
				prediction = ai.classify(image_arr)
				result += str(int(prediction[0, 0]))
				print(prediction)

			server.send_result(prediction)

	except:
		print("Exception occurs. Server shutdown.")

	ok = False
	t.join()


if __name__ == "__main__":
	main(sys.argv)