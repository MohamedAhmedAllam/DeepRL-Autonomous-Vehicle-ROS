#!/usr/bin/env python


import rospy
from std_msgs.msg import Float64, String
from geometry_msgs.msg import Twist
from sensor_msgs.msg import PointCloud, PointCloud2, LaserScan
from laser_geometry import laser_geometry

import sys
import random
from math import cos, sin, atan
PI = 3.14159265359

class triar2:

    def __init__(self):

        self.ns = rospy.get_param("~namespace","/catvehicle")
        rospy.init_node('Qlearner', anonymous=True)

        rospy.Subscriber('{0}/front_laser_points'.format(self.ns), LaserScan, self.callback)
        self.pub_cmdvel = rospy.Publisher('{0}/cmd_vel'.format(self.ns), Twist, queue_size=50)

        self.vel = 0
        self.ang = 0
        self.laserMsg = LaserScan()
        self.laserReading = []
        self.noOfsamples = 0
        self.xyz = [[] for i in range(3)]

    def callback(self,data):
        self.laserMsg = data
        self.noOfsamples = len(self.laserMsg.ranges)
        self.laserReading = []
        for r in range(5):
            self.laserReading.append(sum(self.laserMsg.ranges[r*(self.noOfsamples/5):(r+1)*(self.noOfsamples/5)])/(self.noOfsamples/5))

    def publish(self):
        msger = ", ".join([str(x) for x in self.laserReading] )
        #msger = "%f" %int(self.noOfsamples)
        rospy.loginfo(msger)

def main(argv):
    node = triar2()
    rate = rospy.Rate(10)
    while not rospy.is_shutdown():
        node.publish()
        rate.sleep()


if __name__ == '__main__':
    try:
        main(sys.argv[1:])
    except rospy.ROSInterruptException:
        pass