#!/usr/bin/env python3
import rospy
from geometry_msgs.msg import Twist

# initialize the node
rospy.init_node('red_light_green_light')

# create a publisher for the cmd_vel topic
cmd_vel_pub = rospy.Publisher('cmd_vel', Twist, queue_size=1)

# create Twist messages for stopping and moving forward
red_light_twist = Twist()
green_light_twist = Twist()
green_light_twist.linear.x = 0.5

# initial state
driving_forward = False
light_change_time = rospy.Time.now() + rospy.Duration(3)

# set the rate at which the loop should run
rate = rospy.Rate(10)

while not rospy.is_shutdown():
    # publish the appropriate message based on the driving state
    if driving_forward:
        cmd_vel_pub.publish(green_light_twist)
    else:
        cmd_vel_pub.publish(red_light_twist)

    # check if it's time to change the light
    if rospy.Time.now() > light_change_time:
        driving_forward = not driving_forward
        light_change_time = rospy.Time.now() + rospy.Duration(3)

    # sleep to maintain the loop rate
    rate.sleep()
