#!/usr/bin/env python3

import rospy
import actionlib
import math
from tf.transformations import euler_from_quaternion
from geometry_msgs.msg import Twist, Pose, Point
from nav_msgs.msg import Odometry
from week3_package.msg import ObstacleDetectionAction, ObstacleDetectionGoal, ObstacleHandlingAction, ObstacleHandlingGoal

class MainControl:
    def __init__(self):
        self.goal_x = rospy.get_param('~goal_x')
        self.goal_y = rospy.get_param('~goal_y')
        self.goal = Point(self.goal_x, self.goal_y, 0)
        self.current_pose = Pose()
        self.obstacle_count = 0
        self.max_obstacles = 5
        self.goal_tolerance = 0.1
        self.kp = 0.5
        
        self.obstacle_detection_client = actionlib.SimpleActionClient('obstacle_detection', ObstacleDetectionAction)
        self.obstacle_handling_client = actionlib.SimpleActionClient('obstacle_handling', ObstacleHandlingAction)

        rospy.loginfo("Waiting for action servers...")
        self.obstacle_detection_client.wait_for_server()
        self.obstacle_handling_client.wait_for_server()
        rospy.loginfo("Action servers started.")

        self.cmd_pub = rospy.Publisher('/cmd_vel', Twist, queue_size=1)
        self.odom_sub = rospy.Subscriber('/odom', Odometry, self.odom_callback)

        rospy.sleep(1)  # wait for the publisher to be ready
        self.turn_towards_goal()
        self.move_to_goal()

    def odom_callback(self, msg):
        self.current_pose = msg.pose.pose

    def get_yaw_from_quaternion(self, q):
        euler = euler_from_quaternion([q.x, q.y, q.z, q.w])
        return euler[2] # roll, pitch, yaw

    def normalize_angle(self, angle):
        while angle > math.pi:
            angle -= 2 * math.pi
        while angle < -math.pi:
            angle += 2 * math.pi
        return angle
    
    def turn_towards_goal(self):
        rate = rospy.Rate(10)
        twist = Twist()
        twist.linear.x = 0.0
        twist.angular.z = 0.0
        self.cmd_pub.publish(twist)

        while not rospy.is_shutdown():
            dx = self.goal.x - self.current_pose.position.x
            dy = self.goal.y - self.current_pose.position.y
            desired_yaw = math.atan2(dy, dx)
            current_yaw = self.get_yaw_from_quaternion(self.current_pose.orientation)

            yaw_error = self.normalize_angle(desired_yaw - current_yaw)

            if abs(yaw_error) > 0.01: 
                twist.angular.z = self.kp * yaw_error / abs(yaw_error)
                self.cmd_pub.publish(twist)
            else:
                twist.angular.z = 0
                self.cmd_pub.publish(twist)
                break

            rate.sleep()

    def move_to_goal(self):
        rate = rospy.Rate(10)
        twist = Twist()

        while self.obstacle_count < self.max_obstacles and not rospy.is_shutdown():
            distance = math.sqrt((self.goal.x - self.current_pose.position.x)**2 + (self.goal.y - self.current_pose.position.y)**2)
            # rospy.loginfo(f"Distance to goal: {distance}")
            if distance <= self.goal_tolerance:
                rospy.loginfo("Goal reached.")
                twist.linear.x = 0.0
                twist.angular.z = 0.0
                self.cmd_pub.publish(twist)
                break

            twist.linear.x = 0.2
            self.cmd_pub.publish(twist)

            if not self.detect_obstacles():
                continue
            
            rate.sleep()

    def detect_obstacles(self):
        obstacle_detected = False
        self.obstacle_detection_client.send_goal(ObstacleDetectionGoal())
        if self.obstacle_detection_client.wait_for_result(rospy.Duration(0.1)):
            result = self.obstacle_detection_client.get_result()
            if result.obstacle_detected:
                rospy.loginfo("Obstacle detected.")
                obstacle_detected = True
                self.handle_obstacle()

        return obstacle_detected
    
    def handle_obstacle(self):
        twist = Twist()
        twist.linear.x = 0.0
        self.cmd_pub.publish(twist)

        self.obstacle_handling_client.send_goal(ObstacleHandlingGoal())
        self.obstacle_handling_client.wait_for_result()
        result = self.obstacle_handling_client.get_result()

        if result is not None:
            if result.handled:
                self.obstacle_count += 1
                rospy.loginfo(f"Handled obstacle {self.obstacle_count}/{self.max_obstacles}.")
            else:
                rospy.logwarn("Obstacle handling interrupted by ROS shutdown.")
                
        self.turn_towards_goal()

if __name__ == '__main__':
    rospy.init_node('main_control')
    MainControl()
    rospy.spin()
