#!/usr/bin/env python3

import rospy
from gazebo_msgs.srv import SpawnModel
from geometry_msgs.msg import Pose, Point, Quaternion

def spawn_sphere():
    rospy.init_node('spawn_sphere')

    rospy.wait_for_service('/gazebo/spawn_sdf_model')
    spawn_model_prox = rospy.ServiceProxy('/gazebo/spawn_sdf_model', SpawnModel)

    model_name = 'green_sphere'
    model_xml = ''
    with open('/home/soham/catkin_ws/src/week3_package/model/green_sphere.sdf', 'r') as file:
        model_xml = file.read()

    initial_pose = Pose()
    initial_pose.position = Point(0.5, 0.5, 0)
    initial_pose.orientation = Quaternion(0, 0, 0, 0)

    try:
        spawn_model_prox(model_name, model_xml, '', initial_pose, 'world')
        rospy.loginfo("Spawned green sphere at (1, 1)")
    except rospy.ServiceException as e:
        rospy.logerr("Service call failed: {0}".format(e))

if __name__ == '__main__':
    try:
        spawn_sphere()
    except rospy.ROSInterruptException:
        pass
