import cv2
import numpy as np
from roboflow import Roboflow
import rospy

def bridgeImgMsg(img_msg):
	try:
		frame = np.frombuffer(img_msg.data, dtype=np.uint8).reshape(img_msg.height, img_msg.width, -1)
	except:
		rospy.logwarn("Unable to bridge Image msg")
		return
	frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
	return frame

def scaleImg(frame,res=640):
	h,w,ch = frame.shape
	ratio = float(h)/w
	frame = cv2.resize(frame,(res,int(res*ratio)))
	return frame

class Inference:
	def __init__(self,params):
		project,version = params
		rf = Roboflow(api_key="muXhbHA23Vd2tWj6txCK")
		project = rf.workspace().project(project)
		self.model = project.version(version).model
	def predict(self,frame):
		M = np.ones(frame.shape, dtype="uint8") * 50
		img = cv2.add(frame, M)
		predictions = self.model.predict(img, confidence=40, overlap=20).json()["predictions"]
		return predictions

class MultiInference:
	def __init__(self,params):
		self.units = [Inference(param) for param in params]
	def inference(self,frame):
		predictions = [model.predict(frame) for model in self.units]
		return predictions

def drawBB(img,predictions):
	for prediction in predictions:
		w = prediction['width'] / 2
		h = prediction['height'] / 2
		x1 = int(prediction['x'] - w)
		x2 = int(prediction['x'] + w)
		y1 = int(prediction['y'] - h)
		y2 = int(prediction['y'] + h)
		cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
		cv2.putText(img, prediction["class"] + " " + str(int(prediction["confidence"] * 100)) + '%', (x1, y1 - 5),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
		cv2.imwrite("img.jpg",img)
		print("Image saved")
	return img