import cv2
from apriltag import apriltag


class TagSensor():
	def __init__(self, device=0, tagfamilly="tag36h11"):
		self.tagFamily = tagfamilly
		self.detectedTags = []
		self.cap = cv2.VideoCapture(device)  # 0, -1, /dev/video0 ...


	def Read(self):
		cap = self.cap
		if cap.isOpened():
			ret, img = cap.read()
			img = cv2.rotate(img, cv2.ROTATE_180)
			if ret:
				image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
				detector = apriltag(self.tagFamily)
				self.detectedTags = detector.detect(image)

				return [len(self.detectedTags), self.detectedTags]

			else:
				return -1
		else:
			return -1
