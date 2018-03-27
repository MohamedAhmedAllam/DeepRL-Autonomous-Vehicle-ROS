
import rospy
# from std_msgs.msg import Float64, String
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan

import sys
import random
from math import cos, sin, atan, pow
import numpy as np

import pickle
import csv
import xlsxwriter


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
        actions.append((velocityInc, np.around(angle, decimals=2)))

for i1 in laserVals:
    for i2 in laserVals:
            laserPosCombs.append((i1, i2))

for velocity in velocities:
    for laserComb in laserPosCombs:
        states.append((velocity, laserComb))
        temp_dic = {}
        for a in actions:
            temp_dic[a] = random.randint(0, 10)
        Q[(velocity, laserComb)] = temp_dic

#def save_obj(obj, name ):
    #with open('obj/'+ name + '.pkl', 'wb') as f:
     #   pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)


def main(argv):
    #save_obj(Q,'Q')

     with open('mycsvfile.csv', 'wb') as f:  # Just use 'w' mode in 3.x
         w = csv.DictWriter(f, Q.keys())
         w.writeheader()
         w.writerow(Q)
     print actions[1]

    # workbook = xlsxwriter.Workbook('data.xlsx')
    # worksheet = workbook.add_worksheet()
    # row = 0
    # col = 0
    # for key in Q[(velocities[1], laserPosCombs[1])].keys():
    #     print Q[(velocities[1], laserPosCombs[1])][key]
    #     row += 1
    #     worksheet.write(row, col, key)
    #     #for item in Q[(velocities[1], laserPosCombs[1])][key]:
    #     #    worksheet.write(row, col + 1, item)
    #     #    row += 1
    #
    # workbook.close()

if __name__ == '__main__':
    try:
        main(sys.argv[1:])
    except rospy.ROSInterruptException:
        pass
