#!/usr/bin/env python3

# Importations

import rospy
import math
from open_manipulator_msgs.srv import SetKinematicsPose, SetJointPosition, SetJointPositionRequest
from open_manipulator_msgs.msg import KinematicsPose
from time import sleep
#from geometry_msgs.msg import Point
#from std_msgs.msg import Int32

# Variables

d1 = 77
a2 = 130
a3 = 124
a4 = 126+35
phi = math.atan2(128, 24)



########################### Type de déplacement ####################################

# Commande articulaire du robot : MGD 

def move_joints(q1, q2, q3, q4, t):
	rospy.init_node('move_robot', anonymous=True)
	rospy.wait_for_service('/goal_joint_space_path')
	try:
		set_joint_position = rospy.ServiceProxy('/goal_joint_space_path', SetJointPosition)
		req = SetJointPositionRequest()
		req.planning_group = 'arm'
		req.joint_position.joint_name = ['joint1', 'joint2', 'joint3', 'joint4']
		req.joint_position.position = [q1, q2, q3, q4]
		req.path_time = t
		response = set_joint_position(req)
		if response.is_planned:
			rospy.loginfo("Mouvement articulaire planifié avec succès")
		else:
			rospy.logwarn("Le mouvement n'a pas pu être planifié")
	except rospy.ServiceException as e:
		rospy.logerr(f"Erreur lors de l'appel au service : {e}")



# Commande relative articulaire du robot : MGD relatif

def move_joints_relative(q1, q2, q3, q4, t):
	rospy.init_node('move_robot', anonymous=True)
	rospy.wait_for_service('/goal_joint_space_path_from_present')
	try:
		set_joint_position = rospy.ServiceProxy('/goal_joint_space_path_from_present', SetJointPosition)
		req = SetJointPositionRequest()
		req.planning_group = 'arm'
		req.joint_position.joint_name = ['joint1', 'joint2', 'joint3', 'joint4']
		req.joint_position.position = [q1, q2, q3, q4]
		req.path_time = t
		response = set_joint_position(req)
		if response.is_planned:
			rospy.loginfo("Mouvement relatif planifié avec succès")
		else:
			rospy.logwarn("Le mouvement n'a pas pu être planifié")
	except rospy.ServiceException as e:
		rospy.logerr(f"Erreur lors de l'appel au service : {e}")



# Commande angulaire de l'effecteur (0.01 open, -0.01 close)

def move_effector(angle, t):
	rospy.wait_for_service('/goal_tool_control')
	try:
 		set_effector_position = rospy.ServiceProxy('/goal_tool_control', SetJointPosition)
 		req = SetJointPositionRequest()
 		req.planning_group = 'arm'
 		req.joint_position.joint_name = ['gripper']
 		req.joint_position.position = [angle]
 		req.path_time = t
 		response = set_effector_position(req)
 		#if response.is_planned:
 			#rospy.loginfo("Mouvement planifié avec succès")
 		#else:
 			#rospy.logwarn("Le mouvement n'a pas pu être planifié")
	except rospy.ServiceException as e:
 		rospy.logerr(f"Erreur lors de l'appel au service : {e}")



# Commande en position de l'effecteur dans le repère robot : MGI

def MGI(x, y, z, t):
	q1 = math.atan2(y, x)
	try:
		X1 = math.sqrt(x**2 + y**2)
		Y1 = -(z + a4 - d1)
		q3 = math.acos((Y1**2 + X1**2 - a2**2 - a3**2) / (2*a2*a3)) - phi
		k1 = a2*math.cos(phi) + a3*math.cos(q3)
		k2 = a2*math.sin(phi) - a3*math.sin(q3)
		q2 = math.atan2(k2*X1 + Y1*k1, k1*X1 - k2*Y1)
		q4 = math.pi/2 - q2 - q3
		move_joints(q1, q2, q3, q4, t)
	except rospy.ServiceException as e:
		if e == ValueError:
			rospy.logerr(f"La position est inatteignable")
		else:
			rospy.logerr(f"Erreur lors de l'appel au service : {e}")

##################### Déplacements simples ############################

def effector_open():
	move_effector(0.01, 1.0)

def effector_close():
	move_effector(-0.01, 1.0)

# Position pour prise d'images
def home_pos(t):
	move_joints(0.7, -0.2, 0.0, 1.5, t)

# Prendre verre	
def take_pos(t):
	
	move_joints_relative(0, 0.8, 0.8, -3.0, t)
	sleep(2)
	move_joints_relative(0, 0.0, 0.0, 0.1, t)
	sleep(2)
	effector_close()
	sleep(1)
	move_joints_relative(0, -0.3, 0.0, 0.0, t)

# Position et service du verre
def serv_pos(t):
	move_joints(-1.4, 0.0, -0.5, 0.5, t)
	sleep(3)
	move_joints_relative(0.0, 0.1, 0.0, 2.0, t)

def throw_pos(t):
	move_joints(-1.6, 0.0, -0.5, 0.5, t)
	effector_open()


###################### Déplacements composés ###########################

def home_to_serv():
	home_pos(2.0)
	sleep(2)
	serv_pos(2.0)

# Fonctions communication ROS

current_position = 10000

		
		
		
