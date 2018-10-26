import sys
import split
import cv2
import numpy as np
from matplotlib import pyplot as plt
import math

def check_is_near_middle(circle, middle):
	return abs(int(circle[0]) - middle) <= circle[2]/2


def detect(path_to_file, strict_mode = True, debug = False):
	# Изменить ширину до 1000, все коэффиценты настроены именно так
	size = 1000
	
	img = cv2.imread(path_to_file)

	kf = size / len(img[0])
	img = cv2.resize(img, (0, 0), fx = kf, fy = kf, interpolation = cv2.INTER_LANCZOS4)
	width = len(img[0])

	min_perc = .05
	max_perc = .15

	gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	gray = cv2.GaussianBlur(gray, (15, 15), 0)
	kernel = np.ones((7, 7), np.uint8)
	gray = cv2.dilate(gray, kernel, iterations = 3)
	edged = cv2.Canny(gray, 10, 10)
	circles = cv2.HoughCircles(edged, cv2.HOUGH_GRADIENT, 1, int(2*max_perc*width), param1 = 15, param2 = 35, minRadius = int(min_perc*width), maxRadius = int(max_perc*width))
	if not circles is None:
		circles = np.uint16(np.around(circles))

	if debug:
		plt.subplot(131)
		plt.imshow(img, cmap = 'gray')
		plt.title("Original image")
	
		plt.subplot(132)
		plt.imshow(edged, cmap = 'gray')	
		plt.title("Edges")

		cimg = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)	

		if not circles is None:
			for k in range(len(circles[0,:])):
				cur_circle = circles[0,:][k]
				cv2.circle(cimg, (cur_circle[0], cur_circle[1]), cur_circle[2], (0, 255, 0), 20)
				cv2.circle(cimg, (cur_circle[0], cur_circle[1]), 2, (255, 0, 0), 40) 

		plt.subplot(133)
		plt.imshow(cimg)
		plt.title("Detected stamps")
		plt.show()

	middle = width / 2

	# Проверить что распознанные круги могут быть печатями
	correct = True
	circles_count = 0
	positions = []
	description = ""

	if not circles is None:
		circles_count = len(circles[0])
		circles = circles[0,:]
		if circles_count > 2:
			# Strict mode
			if strict_mode:
				description = "Объектов, распознанных как печати больше 2."
				correct = False
			else:
				# Получить два нижних объекта
				sorted_circles = sorted(circles, key = lambda x: x[1])
				circles = sorted_circles[-2:]
				circles_count = 2

		if circles_count == 1:
			# Одна печать
			circle = circles[0]
			# Если объект смещен от центра -- скорее всего печать
			if not check_is_near_middle(circle, middle):				
				if circle[0] > middle:
					positions.append("R")
				else:
					positions.append("L")

			else:
				description = "Объект слишком близко к центру"	
				correct = False
		elif circles_count == 2:
			# Две печати
			first = circles[0]
			second = circles[1]

			if check_is_near_middle(first, middle) or check_is_near_middle(second, middle):
				description = "Один из объектов слишком близко к центру"
				correct = False
			elif (first[0] < middle and second[0] < middle) or (first[0] > middle and second[0] > middle):
				description = "Объекты, распознанные как печати находятся на одной стороне"
				correct = False
			else:
				max_rad = max([first[2], second[2]])
				if abs(int(first[1]) - int(second[1])) > max_rad:
					description = "Объекты разнесены по вертикали"
					correct = False
				else:
					correct = True
					positions.append("R")
					positions.append("L")

	return correct, circles_count, positions, description