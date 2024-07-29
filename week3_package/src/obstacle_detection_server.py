#!/usr/bin/env python3

import rospy
import actionlib
from sensor_msgs.msg import LaserScan
from week3_package.msg import ObstacleDetectionAction, ObstacleDetectionFeedback, ObstacleDetectionResult

class ObstacleDetectionActionServer:
    def __init__(self):
        self.server = actionlib.SimpleActionServer('obstacle_detection', ObstacleDetectionAction, self.execute, False)
        self.feedback = ObstacleDetectionFeedback()
        self.result = ObstacleDetectionResult()
        self.laser_sub = rospy.Subscriber('/scan', LaserScan, self.scan_callback)
        self.obstacle_detected = False
        self.threshold_distance = 0.4
        self.server.start()

    def scan_callback(self, data):
        front_ranges = data.ranges[:30] + data.ranges[-30:]
        if min(front_ranges) < self.threshold_distance:
            self.obstacle_detected = True
        else:
            self.obstacle_detected = False
         
    def execute(self, goal):
        rate = rospy.Rate(10)
        try:
            while not rospy.is_shutdown():
                self.feedback.obstacle_detected = self.obstacle_detected
                self.server.publish_feedback(self.feedback)
                if self.obstacle_detected:
                    self.result.obstacle_detected = True
                    self.server.set_succeeded(self.result)
                    return
                rate.sleep()
        except rospy.ROSInterruptException:
            rospy.logwarn("ROS shutdown request received. Exiting.")

if __name__ == '__main__':
    rospy.init_node('obstacle_detection_server')
    server = ObstacleDetectionActionServer()
    rospy.spin()