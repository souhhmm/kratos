#!/usr/bin/env python3

# code heavily borrowed from Programming Robots with ROS by Morgan Quigley, Brian Gerkey, and William D. Smart
import rospy
import sys, select, tty, termios # tty and termios are for setting terminal attributes
from std_msgs.msg import String

if __name__ == '__main__':
    key_publisher = rospy.Publisher('keys', String, queue_size=1)
    rospy.init_node('key_publisher')
    rate = rospy.Rate(100)
    old_attr = termios.tcgetattr(sys.stdin) # store current attributes
    tty.setcbreak(sys.stdin.fileno()) # set terminal to cbreak mode (no buffering)
    
    try:
        while not rospy.is_shutdown():
            if select.select([sys.stdin], [], [], 0)[0] == [sys.stdin]:
                key = sys.stdin.read(1) # select.select(read, write, error, timeout) + additional check
                key_publisher.publish(key) # read 1 char (in our case the motion keys) from stdin
            rate.sleep()
    except rospy.ROSInterruptException: # catch the exception when the node is interrupted
        pass
    finally:
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_attr) # restore terminal settings