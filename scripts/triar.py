#!/usr/bin/env python



import rospy
from std_msgs.msg import Float64, String
import sys


class triar:

    def __init__(self):
        self.ns = rospy.get_param("~namespace","catvehicle")
        rospy.init_node('triar', anonymous=True)
        self.x = 5
        self.y = 7
        self.Q = {}

        self.pub = rospy.Publisher('/pubozz'.format(self.ns), String, queue_size=1)

        for i in range(self.x):
            self.Q[i] = {}
            for j in range(self.y):
                self.Q[i][j] = i*j

    def publish(self):
        self.Q[1][1] = self.Q[1][1]+1
        msger = "%f" %self.Q[1][1]

        self.pub.publish(msger)
        rospy.loginfo(msger)
        #print(self.Q[1][1])

def main(argv):
    node = triar()
    rate = rospy.Rate(1000)
    while not rospy.is_shutdown():
        node.publish()
        rate.sleep()

if __name__ == '__main__':
    try:
        main(sys.argv[1:])
    except rospy.ROSInterruptException:
        pass