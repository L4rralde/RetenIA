#!/usr/bin/python3
import rospy
import cv2
from sensor_msgs.msg import Image
import numpy as np
from roboflow import Roboflow

class Inference:
	def __init__(self,case):
		rf = Roboflow(api_key="muXhbHA23Vd2tWj6txCK")
		project = rf.workspace().project(case)
		self.model = project.version(3).model
	def predict(self,frame):
		M = np.ones(frame.shape, dtype="uint8") * 50
		img = cv2.add(frame, M)
		print(self.model.predict(frame, confidence=40, overlap=20).json())

class VisionNode:
	def __init__(self, model, rate):
		self.inference = Inference(model)
		self.subs = rospy.Subscriber('/cam1/camera/image_raw',Image,self.onImage,queue_size=1)
		self.rate = rate
		self.last_time = rospy.Time.now()
	def bridge(self,imgMsg):
		dt = (imgMsg.header.stamp - self.last_time).to_sec()
		print(1/dt)
		if 1/dt > self.rate:
			return
		self.last_time = imgMsg.header.stamp
		try:
			frame = np.frombuffer(imgMsg.data, dtype=np.uint8).reshape(imgMsg.height, imgMsg.width, -1)
		except:
			rospy.logwarn("Unable to bridge Image msg")
			return
		frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
		h,w,ch = frame.shape
		ratio = h/float(w)
		frame = cv2.resize(frame,(640,int(640*ratio)))
		return frame
	def onImage(self,imgMsg):
		frame = self.bridge(imgMsg)
		if frame is None:
			return
		self.inference.predict(frame)
		cv2.imshow("img",frame)
		cv2.waitKey(1)

def main():
	rospy.init_node("accidentNet")
	node = VisionNode("crash-car-detection",1)
	try:
		rospy.spin()
	except ROSInterruptException:
		pass

if __name__=='__main__':
	main()
