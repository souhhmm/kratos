#!/usr/bin/env python3

import rospy
import actionlib
from geometry_msgs.msg import Twist
from week3_package.msg import ObstacleHandlingAction, ObstacleHandlingFeedback, ObstacleHandlingResult

class ObstacleHandlingActionServer:
    def __init__(self):
        self.server = actionlib.SimpleActionServer('obstacle_handling', ObstacleHandlingAction, self.execute, False)
        self.feedback = ObstacleHandlingFeedback()
        self.result = ObstacleHandlingResult()
        self.cmd_pub = rospy.Publisher('/cmd_vel', Twist, queue_size=1)
        self.server.start()

    def execute(self, goal):
        self.navigate_around_obstacle()
        self.result.handled = True
        self.server.set_succeeded(self.result)

    def navigate_around_obstacle(self):
        # turn 90 degrees
        twist = Twist()
        twist.angular.z = 0.5
        for _ in range(36):
            self.cmd_pub.publish(twist)
            rospy.sleep(0.1)

        # move forward
        twist.angular.z = 0.0
        twist.linear.x = 0.2
        for _ in range(30):
            self.cmd_pub.publish(twist)
            rospy.sleep(0.1)

        # turn back to original direction
        # twist.angular.z = -0.5
        # for _ in range(36):
        #     self.cmd_pub.publish(twist)
        #     rospy.sleep(0.1)

        # move forward
        # twist.angular.z = 0.0
        # twist.linear.x = 0.2
        # for _ in range(1):
        #     self.cmd_pub.publish(twist)
        #     rospy.sleep(0.1)

        twist.linear.x = 0.0
        self.cmd_pub.publish(twist)

if __name__ == '__main__':
    rospy.init_node('obstacle_handling_server')
    server = ObstacleHandlingActionServer()
    rospy.spin()