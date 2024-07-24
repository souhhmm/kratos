#!/usr/bin/env python3
# approach 1: functions
import rospy
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan

obstacle_detected = False

def scan_cb(msg):
    global obstacle_detected
    range_ahead = msg.ranges[len(msg.ranges) // 2]  # range directly in front
    rospy.loginfo('Range ahead: %0.2f' % range_ahead)
    if range_ahead < 0.5:
        rospy.loginfo('Obstacle detected!')
        obstacle_detected = True
    else:
        obstacle_detected = False

def stop_and_turn():
    # stop  
    twist = Twist()
    twist.linear.x = 0.0
    twist.angular.z = 0.0
    cmd_vel_pub.publish(twist)
    rospy.sleep(1)

    # turn
    twist.angular.z = 0.5   
    cmd_vel_pub.publish(twist)
    rospy.sleep(3.14) # pi

    # stop
    twist.angular.z = 0.0
    cmd_vel_pub.publish(twist)

def move_forward():
    twist = Twist()
    twist.linear.x = -0.2
    twist.angular.z = 0.0
    cmd_vel_pub.publish(twist)

if __name__ == '__main__':
    rospy.init_node('week2bot_1')
    scan_sub = rospy.Subscriber('scan', LaserScan, scan_cb)
    cmd_vel_pub = rospy.Publisher('cmd_vel', Twist, queue_size=1)
    rate = rospy.Rate(10)

    try:
        while not rospy.is_shutdown():
            if obstacle_detected:
                stop_and_turn()
            else:
                move_forward()

            rate.sleep()
    except rospy.ROSInterruptException:
        pass
        

