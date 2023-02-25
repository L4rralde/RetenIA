#!/usr/bin/env python2
import rospy
import rospkg
from gazebo_msgs.srv import SpawnModel
from gazebo_msgs.srv import SpawnModelRequest
import math
from geometry_msgs.msg import Pose
from geometry_msgs.msg import Quaternion
import math
import numpy
from tf.transformations import quaternion_from_euler
import random

rospack  = rospkg.RosPack()
pkg_path = rospack.get_path('simulation')
spawn_model = rospy.ServiceProxy('/gazebo/spawn_sdf_model', SpawnModel)
cameraModel = '/models/ros_camera/model.sdf'
carPoloModel = '/models/car_polo/model.sdf'
car46Model = '/models/car_046/model.sdf'
car144Model = '/models/car_144/model.sdf'
carLexusModel = '/models/car_lexus/model.sdf'
carBeetleModel = '/models/car_beetle/model.sdf'
carModels = [carPoloModel, car46Model, car144Model, carLexusModel, carBeetleModel]

def getRandCarModel():
	return carModels[random.randint(0,len(carModels)-1)]
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
def rpy2Quat(r=0,p=0,y=0):
	q = quaternion_from_euler(r,p,y)
	orientation = Quaternion()
	orientation.x = q[0]
	orientation.y = q[1]
	orientation.z = q[2]
	orientation.w = q[3]
	return orientation

def simpleSpawn(name,model,x=0,y=0,z=0,roll=0,pitch=0,yaw=0):
	modelSpawner = ModelSpawner(name,model)
	pose = Pose()
	pose.position.x = x
	pose.position.y = y
	pose.position.z = z
	pose.orientation = rpy2Quat(roll,pitch,yaw)
	modelSpawner.spawn(pose)

def main():
	rospy.init_node("c5cam_node")
	rospy.wait_for_service("/gazebo/spawn_sdf_model")
	
	simpleSpawn('cam0',cameraModel, y=35, z=35, pitch=0.9, yaw=-math.pi/2)
	simpleSpawn('cam1',cameraModel, x=100, y=-35, z=35, pitch=0.9, yaw=math.pi/2)
	conLen = 7
	for i in range(conLen):
		simpleSpawn('car'+str(2*i), carPoloModel, x=0+25*i, y=-16, yaw=-math.pi/2)
		simpleSpawn('car1'+str(2*i+1), carPoloModel, x=10+25*i, y=-6, yaw=-math.pi/2)
	#simpleSpawn('cam1',cameraModel, x=40, y=-20, z=20, pitch=0.3, yaw=-0.5)
	simpleSpawn('car'+str(2*conLen), carPoloModel, x=0+25*conLen, y=-12, yaw=-math.pi/2)
	simpleSpawn('car1'+str(2*conLen+1), carPoloModel, x=10+25*conLen, y=-10, yaw=-1.2*math.pi/2)

"""
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
"""

if __name__ == '__main__':
	main()