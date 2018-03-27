import rospy
from std_msgs.msg import Bool
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan

import time

import sys
import random
from math import cos, sin, atan, pow
import numpy as np
import csv
import pickle
resetter = 0

vel = 0
ang = 0

realVelX = 100

laserMsg = LaserScan()
laserReading = []
noOfsamples = 50

msgTwist = Twist()

epsilon = 0.1
discount = 0.9
alpha = 1

actions = []
states = []
Q = {}

timer = 0

angVals = np.around(np.arange(-0.3, 0.35, 0.1), decimals=2)
# velIncVals = np.arange(-1, 4, 1)  # (-4,5,2)
# velocities = np.arange(0, 7, 2)   #(0,20,2)
laserVals = np.arange(5, 35, 10)
laserPosCombs = []

count = 0

# for velocityInc in velIncVals:
for angle in angVals:
    # actions.append((velocityInc, angle))
    actions.append(angle)

for i1 in laserVals:
    for i2 in laserVals:
        for i3 in laserVals:
            for i4 in laserVals:
                for i5 in laserVals:
                    laserPosCombs.append((i1 ,i2 ,i3 ,i4 ,i5))

# for velocity in velocities:
for laserComb in laserPosCombs:
    states.append(laserComb)
    temp_dic = {}
    for a in actions:
        temp_dic[a] = random.randint(0,10)
    Q[laserComb] = temp_dic


def save_obj(obj, name):
    with open('obj/' + name + '.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)

def load_obj(name):
    with open('obj/' + name + '.pkl', 'rb') as f:
        return pickle.load(f)

def main(argv):
    save_obj(Q, 'Qtabletry')
    Qafterload = load_obj('Qtabletry')
    for keyar1 in Q.iterkeys():
        for keyar2 in Q[keyar1].iterkeys():
            if Q[keyar1][keyar2] != Qafterload[keyar1][keyar2]:
                print('ERROR ' + str(keyar1) + '' +str(keyar2))
    #print(Q[laserPosCombs[1]][actions[1]])
    #print(Qafterload[laserPosCombs[1]][actions[1]])
if __name__ == '__main__':
    try:
        main(sys.argv[1:])
    except rospy.ROSInterruptException:
        pass
