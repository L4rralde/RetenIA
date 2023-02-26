#!/usr/bin/python3
import rospy
from sensor_msgs.msg import Image
import vision_utils as vu
import cv2
import datetime

AI = vu.MultiInference([('crash-car-detection',3),('fire-ronz9',1)])

def getTopicsByType(msg_type):
	topics = rospy.get_published_topics()
	wanted_topics = []
	for topic in topics:
		t_name, t_type = topic
		if not t_type==msg_type:
			continue
		wanted_topics.append(topic)
	return wanted_topics

class DisplayNode:
	def __init__(self,topic,period):
		#id = id+1
		self.rate = 1/period
		self.topic = topic
		self.subs = rospy.Subscriber(topic, Image, self.onImg, queue_size=1)
		self.last_time = rospy.Time.now()
	def onImg(self,img_msg):
		now = rospy.Time.now()
		dt = (now-self.last_time).to_sec()
		if 1/dt > self.rate:
			return
		self.last_time = now
		img_name = self.topic.split('/')[1]
		frame = vu.bridgeImgMsg(img_msg)
		if frame is None:
			return
		frame = vu.scaleImg(frame)
		bbxs = AI.inference(frame)
		for bbx in bbxs:
			for prediction in bbx:
				print("Se detecto '{}' en {} @ {}".format(prediction['class'],img_name,datetime.datetime.now()))
			frame = vu.drawBB(frame,bbx)
		cv2.imwrite(img_name+'.jpg',frame)
		print('Saving {}.jpg'.format(img_name))
		
class C5Node:
	def __init__(self,rate):
		img_topics = getTopicsByType('sensor_msgs/Image')
		displays = [DisplayNode(topic[0],rate) for topic in img_topics]



def main():
	rospy.init_node("c5_node", anonymous=True)
	C5Node(10)
	try:
		rospy.spin()
	except ROSInterruptException:
		rospy.loginfo("image_capture node terminated.")

if __name__=='__main__':
	main()