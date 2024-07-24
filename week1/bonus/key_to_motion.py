#!/usr/bin/env python3

# code heavily borrowed from Programming Robots with ROS by Morgan Quigley, Brian Gerkey, and William D. Smart
import rospy
from std_msgs.msg import String
from geometry_msgs.msg import Twist # twist controls everything about the robot's movement

key_mapping = {'w':[0,0.1], 'a': [0.1,0], 'd': [-0.1,0], 's': [0,0], 'x': [0,-0.1]} # key: [angular, linear]


def keys_callback(message, twist_pub):
    if len(message.data) == 0 or not message.data[0] in key_mapping:
        return
    
    vels = key_mapping[message.data[0]]
    twist = Twist() # create a new Twist message
    twist.linear.x = vels[1]
    twist.angular.z = vels[0]
    twist_pub.publish(twist)
    
if __name__ == '__main__':
    rospy.init_node('key_to_motion')
    twist_pub = rospy.Publisher('cmd_vel', Twist, queue_size=1)
    rospy.Subscriber('keys', String, keys_callback, twist_pub) # subscribe to the keys made in key_publisher.py
    rospy.spin()

