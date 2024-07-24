#!/usr/bin/env python3
# approach 2: class
import rospy
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan

class Week2bot:
    def __init__(self):
        rospy.init_node('week2bot_2')
        self.cmd_vel_pub = rospy.Publisher('cmd_vel', Twist, queue_size=1)
        self.scan_sub = rospy.Subscriber('scan', LaserScan, self.scan_cb)
        self.obstacle_detected = False
        self.rate = rospy.Rate(10)
        self.twist = Twist()
        
    def scan_cb(self, msg):
        range_ahead = msg.ranges[len(msg.ranges)//2]
        rospy.loginfo('Range ahead: %0.2f' % range_ahead)
        if range_ahead < 0.5:
            rospy.loginfo('Obstacle detected!')
            self.obstacle_detected = True
        else:
            self.obstacle_detected = False
            
    def move_forward(self):
        self.twist.linear.x = -0.2
        self.twist.angular.z = 0.0
        self.cmd_vel_pub.publish(self.twist)
    
    def stop(self):
        self.twist.linear.x = 0.0
        self.twist.angular.z = 0.0
        self.cmd_vel_pub.publish(self.twist)
        
    def turn(self):
        self.twist.angular.z = 0.5
        self.cmd_vel_pub.publish(self.twist)
        rospy.sleep(3.14)
        self.stop()
    
    def run(self):
        while not rospy.is_shutdown():
            if self.obstacle_detected:
                self.stop()
                rospy.sleep(1)
                self.turn()
            else:
                self.move_forward()
            self.rate.sleep()
            
if __name__ == '__main__':
    try:
        week2bot = Week2bot()
        week2bot.run()
    except rospy.ROSInterruptException:
        pass