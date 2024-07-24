#!/usr/bin/env python3
import rospy
from sensor_msgs.msg import LaserScan

def scan_cb(msg):
    range_ahead = msg.ranges[len(msg.ranges)//2] # range directly in front
    rospy.loginfo('range ahead: %0.1f' % range_ahead)
    
rospy.init_node('range_ahead')
scan_sub = rospy.Subscriber('scan', LaserScan, scan_cb)
rospy.spin()