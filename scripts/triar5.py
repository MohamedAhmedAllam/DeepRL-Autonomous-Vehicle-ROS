
#PRINTING THE Q TABLE

import rospy
# from std_msgs.msg import Float64, String
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan

import sys
import random
from math import cos, sin, atan, pow
import numpy as np

import csv
from pandas import ExcelWriter



PI = 3.14159265359

vel = 0
ang = 0

laserMsg = LaserScan()
laserReading = []
noOfsamples = 50

msgTwist = Twist()

epsilon = 0.01
discount = 0.3
actions = []
states = []
Q = {}

time = 0

angVals = np.around(np.arange(-0.2, 0.25, 0.1), decimals=2)
velIncVals = np.arange(-2, 3, 1)  # (-4,5,2)
velocities = np.arange(0, 20, 4)
laserVals = np.arange(5, 35, 10)
laserPosCombs = []

for velocityInc in velIncVals:
    for angle in angVals:
        actions.append((velocityInc, angle))


for i1 in laserVals:
    for i2 in laserVals:
        for i3 in laserVals:
            laserPosCombs.append((i1,i2,i3))

for velocity in velocities:
    for laserComb in laserPosCombs:
        states.append((velocity, laserComb))
        temp_dic = {}
        for a in actions:
            temp_dic[a] = random.randint(0, 10)
        Q[(velocity, laserComb)] = temp_dic

def save_xls(list_dfs, xls_path):
    writer = ExcelWriter(xls_path)
    for n, df in enumerate(list_dfs):
        df.to_excel(writer,'sheet%s' % n)
    writer.save()

def main(argv):
    with open('dict.csv', 'wb') as csv_file:
        writer = csv.writer(csv_file, delimiter = '\t')
        writer.writerow(['ID'] + [keyr for keyr in Q.iterkeys()])
        #for key, value in Q[(velocities[1], laserPosCombs[1])].items():
        #    writer.writerow([key, value])
        for key in Q[(velocities[1], laserPosCombs[1])].iterkeys():
            RR = '(' + str(key[0]) + ", %.2f" %key[1] + ')'
            writer.writerow([RR] + [Q[maskey][key] for maskey in Q.iterkeys()])

    print velocities[1]
    print laserPosCombs[1]
    print Q[(velocities[1], laserPosCombs[1])]

if __name__ == '__main__':
    try:
        main(sys.argv[1:])
    except rospy.ROSInterruptException:
        pass
