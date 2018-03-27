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

class informedaction:

    def __init__(self):

        self.ns = rospy.get_param("~namespace","/catvehicle")
        rospy.init_node('Qlearner', anonymous=True)

        rospy.Subscriber('{0}/front_laser_points'.format(self.ns), LaserScan, self.callback)
        self.pub_cmdvel = rospy.Publisher('{0}/cmd_vel'.format(self.ns), Twist, queue_size=50)

        self.vel = 0
        self.ang = 0
        self.laserMsg = LaserScan()
        self.xyz = [[] for i in range(3)]

    def callback(self,data):
        #self.laserMsg =
        #self.xyz = [[] for i in range(3)]
        sumx = 0
        sumy = 0
        for i in range(len(data.ranges)):
            ang = (PI/2)+data.angle_min+i*data.angle_increment
            sumx += data.ranges[i] * cos(ang)
            sumy += data.ranges[i] * sin(ang)
            #self.xyz[0].append(data.ranges[i]*cos(ang))
            #self.xyz[1].append(data.ranges[i]*sin(ang))
            #self.xyz[2].append(0)
        #sumx = sum(self.xyz[0])
        #sumy = sum(self.xyz[1])

        self.vel = 7
        self.ang = -1*atan(sumx/sumy)

    def publish(self):
        msgTwist = Twist()
        msgTwist.linear.x = self.vel
        msgTwist.angular.z=  self.ang
        self.pub_cmdvel.publish(msgTwist)
        rospy.loginfo(self.ang)

def main(argv):
    node = informedaction()
    rate = rospy.Rate(10)
    while not rospy.is_shutdown():
        node.publish()
        rate.sleep()


if __name__ == '__main__':
    try:
        main(sys.argv[1:])
    except rospy.ROSInterruptException:
        pass