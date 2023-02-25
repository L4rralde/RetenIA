#!/usr/bin/env python
import rospy
import rospkg
from gazebo_msgs.srv import SpawnModel
from gazebo_msgs.srv import SpawnModelRequest
import math
from geometry_msgs.msg import Pose
import math

rospack  = rospkg.RosPack()
pkg_path = rospack.get_path('simulation')
spawn_model = rospy.ServiceProxy('/gazebo/spawn_sdf_model', SpawnModel)

class ModelSpawner:
	def __init__(self,name,sdf):
		self.name = name
		self.sdf = sdf
	def spawn(self,pose):
		spawn_req = SpawnModelRequest()
		spawn_req.model_name = self.name
		spawn_req.model_xml  = open(pkg_path+self.sdf,'r').read()
		spawn_req.robot_namespace = self.name
		spawn_req.initial_pose = pose
		spawn_model(spawn_req)
#Dummy push

def main():
	rospy.init_node("c5cam_node")
	rospy.wait_for_service("/gazebo/spawn_sdf_model")

	angle = 0.5
	pose = Pose()
	pose.position.y = -15
	pose.position.z = 20
	pose.orientation.z = math.sin(angle/2)
	pose.orientation.w = math.cos(angle/2)
	cam0 = ModelSpawner('cam0','/models/ros_camera/model.sdf')
	cam0.spawn(pose)

	angle = -0.5
	pose.position.y = 15
	pose.orientation.z = math.sin(angle/2)
	pose.orientation.w = math.cos(angle/2)
	cam1 = ModelSpawner('cam1','/models/ros_camera/model.sdf')
	cam1.spawn(pose)

	angle = 0.0
	pose.position.y = 0.0
	pose.position.z = 0.0
	pose.orientation.z = math.sin(angle/2)
	pose.orientation.w = math.cos(angle/2)
	polo = ModelSpawner('car1','/models/car_polo/model.sdf')
	polo.spawn(pose)


	

if __name__ == '__main__':
	main()