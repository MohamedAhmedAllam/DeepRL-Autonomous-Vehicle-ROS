#!/usr/bin/env python


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

PI = 3.14159265359


class Qlearner:

    def __init__(self):
        self.ns = rospy.get_param("~namespace", "/catvehicle")
        rospy.init_node('Qlearner', anonymous=True)

        rospy.Subscriber('{0}/front_laser_points'.format(self.ns), LaserScan, self.laserCallback)
        rospy.Subscriber('{0}/cmd_vel'.format(self.ns), Twist, self.velCallback)
        rospy.Subscriber('/reset_alert', Bool, self.resetCallback)

        self.pub_cmdvel = rospy.Publisher('{0}/cmd_vel'.format(self.ns), Twist, queue_size=50)

        self.resetter = 0

        self.vel = 0
        self.ang = 0

        self.laserMsg = LaserScan()
        self.laserReading = []
        self.noOfsamples = 50

        self.msgTwist = Twist()

        self.epsilon = 0.1
        self.discount = 0.9
        self.actions = []
        self.states = []
        self.Q = {}

        self.time = 0

        self.angVals = np.around(np.arange(-0.2, 0.25, 0.1), decimals=2)
        self.velIncVals = np.arange(-1, 4, 1)  # (-4,5,2)
        self.velocities = np.arange(0, 7, 2)   #(0,20,2)
        self.laserVals = np.arange(5, 35, 10)
        self.laserPosCombs = []

        self.alpha = 1
        self.count = 0

        for velocityInc in self.velIncVals:
            for angle in self.angVals:
                self.actions.append((velocityInc, angle))

        for i1 in self.laserVals:
            for i2 in self.laserVals:
                for i3 in self.laserVals:
                    self.laserPosCombs.append((i1,i2,i3))

        for velocity in self.velocities:
            for laserComb in self.laserPosCombs:
                self.states.append((velocity, laserComb))
                temp_dic = {}
                for a in self.actions:
                    temp_dic[a] = 0.0
                self.Q[(velocity, laserComb)] = temp_dic


    def laserCallback(self, lasermsg):
        self.laserMsg = lasermsg
        self.noOfsamples = len(self.laserMsg.ranges)
        self.laserReading = []
        for r in range(3):
            self.laserReading.append(sum(self.laserMsg.ranges[r*(self.noOfsamples/3):(r+1)*(self.noOfsamples/3)])/(self.noOfsamples/3))

        self.learnQ()


    def velCallback(self, twistmsg):
        self.vel = twistmsg.linear.x
        self.ang = twistmsg.angular.z


    def resetCallback(self, resetbool):
        if resetbool == True:
            self.resetter = 1

    # Calculate the reward
    def calcReward(self):
        c1 = 0.2
        c2 = 0.5
        c3 = -0.5
        c4 = 50
        return (c1*self.vel + c2*(self.laserReading[1]-20) + c3*abs(self.laserReading[0]-self.laserReading[2]) + c4*self.resetter)

    # Increment the Q value of a specific state-action pair
    def incQ(self, s, a, alpha, incVal):
        self.Q[s][a] = (1 - alpha) * self.Q[s][a] + alpha * incVal

    # Find the action with highest Q value for a specific state
    def maxQ(self, s):
        maxqval = None
        max_act = None
        for a, q in self.Q[s].items():
            if max_act is None or (q > maxqval):
                max_act = a
                maxqval = q
        return max_act, maxqval

    # choose the action to be taken depending on your policy (epsilon greedy till now)
    def policy(self, max_act):
        if random.random() > self.epsilon:
            return max_act
        else:
            ind = random.randint(0, len(self.actions) - 1)
            return self.actions[ind]

    # Publish to cmd_vel topic
    def publish(self, action, state):
        self.msgTwist.linear.x = max(state[0] + action[0], 0)
        self.msgTwist.angular.z = action[1]
        self.pub_cmdvel.publish(self.msgTwist)

    def currentState(self):
        apState = []
        for a in range(1,len(self.velocities)):
            if self.vel < (self.velocities[a]):
                apState.append(self.velocities[a-1])
                break
        if len(apState) < 1:
            apState.append(self.velocities[len(self.velocities)-1])

        RR = []
        if len(self.laserReading) == 3:
            for d in range(len(self.laserReading)):
                if self.laserReading[d] <= 10:
                    RR.append(self.laserVals[0])
                elif self.laserReading[d] <= 20:
                    RR.append(self.laserVals[1])
                elif self.laserReading[d] <= 30:
                    RR.append(self.laserVals[2])
                else: RR.append(self.laserVals[2])
        else:
            RR = [5,5,5]
        apState.append(tuple(RR))
        return tuple(apState)

    def resetStuff(self):
            self.msgTwist.linear.x = 0
            self.msgTwist.angular.z = 0
            self.pub_cmdvel.publish(self.msgTwist)
            self.resetter = 0
            time.sleep(2)

    def learnQ(self):

         # get current state
        firstState = self.currentState()
        rospy.loginfo(self.laserReading)
        rospy.loginfo(firstState)
        #rospy.loginfo(self.Q[firstState])
        # choose an action based on learning policy(epsilon greedy)
        maxAct, maxQval = self.maxQ(firstState)
        actualAct = self.policy(maxAct)

        rospy.loginfo(self.Q[firstState][actualAct])

    # run the simulation
        self.publish(actualAct, firstState)
        self.time += 1
        # get the reward & the current state
        secondState = self.currentState()
        reward = self.calcReward()

        # choose an action based on actual policy (greedy)
        maxAct2, maxQval2 = self.maxQ(secondState)

        # update Q table for the previous state
        increment = reward + self.discount * maxQval2
        self.incQ(firstState, actualAct, self.alpha, increment)
        rospy.loginfo(increment)
        rospy.loginfo(self.Q[firstState][actualAct])

        if self.resetter == 1:
            self.resetStuff()

        self.alpha = pow(self.time, -0.05)
        # node.epsilon -= 0.0000001

        # Save Q Table to csv file
        if self.count % 100 == 0:
            # node.saveQtable()
            with open('Qtable.csv', 'wb') as csv_file:
                writer = csv.writer(csv_file, delimiter='\t')
                writer.writerow(['ID'] + [keyr for keyr in self.Q.iterkeys()])
                for key in self.Q[(self.velocities[1], self.laserPosCombs[1])].iterkeys():
                    ZM = '(' + str(key[0]) + ", %.2f" % key[1] + ')'
                    writer.writerow([ZM] + [self.Q[maskey][key] for maskey in self.Q.iterkeys()])
            self.count = 0

        self.count += 1

def main(argv):
    node = Qlearner()
    rospy.spin()


if __name__ == '__main__':
    try:
        main(sys.argv[1:])
    except rospy.ROSInterruptException:
        pass
