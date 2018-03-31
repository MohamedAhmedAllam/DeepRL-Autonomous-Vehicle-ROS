
#!/usr/bin/env python

import rospy
from std_msgs.msg import Bool
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan
from gazebo_msgs.msg import ContactsState

import copy
import time
import collections as col

import sys
import random
from math import cos, sin, atan, pow
import numpy as np
import csv
import pickle

PI = 3.14159265359

class ddpglearner:


    def __init__(self):
        self.ns = rospy.get_param("~namespace", "/catvehicle")
        rospy.init_node('DDPGlearner', anonymous=True)

        rospy.Subscriber('{0}/front_laser_points'.format(self.ns), LaserScan, self.laserCallback)
        rospy.Subscriber('{0}/cmd_vel'.format(self.ns), Twist, self.velCallback)
        rospy.Subscriber('/reset_alert', Bool, self.resetCallback)
        rospy.Subscriber('/front_left_wheel_link_contacts', ContactsState, self.flContactCallback)
        rospy.Subscriber('/front_right_wheel_link_contacts', ContactsState, self.frContactCallback)
        rospy.Subscriber('/back_left_wheel_link_contacts', ContactsState, self.blContactCallback)
        rospy.Subscriber('/back_right_wheel_link_contacts', ContactsState, self.brContactCallback)

        rospy.Subscriber('{0}/vel'.format(self.ns), Twist, self.realVelCallback)

        self.pub_cmdvel = rospy.Publisher('{0}/cmd_vel'.format(self.ns), Twist, queue_size=50)

        self.pub_reset = rospy.Publisher('/reset_alert',Bool,queue_size=50)

        self.resetter = 0

        self.vel = 0
        self.ang = 0

        self.realVelX = 0

        self.laserMsg = LaserScan()
        self.laserReading = [0,0,0,0,0]
        self.laserRead = np.zeros(25)

        self.noOfsamples = 50

        self.msgTwist = Twist()
        self.msgBool =Bool()
        self.resetflag=False
        #code from Torcs
        self.initial_run = True


        self.prevSpeed = 0
        self.stopcount = 0
        self.contact =[1,1,1,1]

    #subscribers callbacks

    def laserCallback(self, lasermsg):
        self.laserMsg = lasermsg
        self.noOfsamples = len(self.laserMsg.ranges)
        # print(len(lasermsg.ranges))
        lengthLas = 5
        for r in range(lengthLas):
            self.laserReading[r] = sum(self.laserMsg.ranges[r*(self.noOfsamples/lengthLas):(r+1)*(self.noOfsamples/lengthLas)])/(self.noOfsamples/lengthLas)

        length = 25
        for r in range(length):
            self.laserRead[r] = sum(
                self.laserMsg.ranges[r * (self.noOfsamples / lengthLas):(r + 1) * (self.noOfsamples / lengthLas)]) / (
                                               self.noOfsamples / lengthLas)

    def velCallback(self, twistmsg):
        self.vel = twistmsg.linear.x
        self.ang = twistmsg.angular.z

    # velocity and laser readings as state

    def realVelCallback(self, twistmsg):
        self.realVelX = twistmsg.linear.x


    def resetCallback(self, resetbool):
        if resetbool.data:
            self.resetter = 1
            self.prevSpeed = 0

    # Contact wheels as states

    def flContactCallback(self, contactmsg):
        if not contactmsg.states:
            self.contact[0] = 0
        else:
            self.contact[0] = 1

    def frContactCallback(self, contactmsg):
        if not contactmsg.states:
            self.contact[1] = 0
        else:
            self.contact[1] = 1

    def blContactCallback(self, contactmsg):
        if not contactmsg.states:
            self.contact[2] = 0
        else:
            self.contact[2] = 1

    def brContactCallback(self, contactmsg):
        if not contactmsg.states:
            self.contact[3] = 0
        else:
            self.contact[3] = 1


    def publish(self, action):
        #self.msgTwist.linear.x = max(state[0] + action[0], 0)
        self.msgTwist.linear.x = max(action[1] + self.prevSpeed,0)
        self.prevSpeed = self.msgTwist.linear.x
        self.msgTwist.angular.z = action[0]/2
        self.pub_cmdvel.publish(self.msgTwist)


    # Calculate the reward
    def calcReward(self):
        c1 = 0.1
        c2 = 0.7
        c3 = -0.5
        c4 = -15
        #return (c1*self.vel + c2*(self.laserReading[1]-20) + c3*abs(self.laserReading[0]-self.laserReading[2]) + c4*self.resetter)
        if self.realVelX < 0.5:
            slowMove = 1
        else:
            slowMove = 0
        return ((self.realVelX/8)*( c2 * (self.laserReading[2] - 15) + c3 * abs(self.laserReading[0] - self.laserReading[4]) - abs(self.ang)*5 )+ c4 * slowMove)



    def resetStuff(self):
        print("Reset")
        self.time_step = 0
        self.prevSpeed = 0
        self.msgTwist.linear.x = 0
        self.msgTwist.angular.z = 0
        self.pub_cmdvel.publish(self.msgTwist)
        self.resetter = 0
        self.prevSpeed = 0
        self.stopcount = 0
        time.sleep(2)
        return self.make_observaton()

    def make_observaton(self):

        names = ['focus',
                 'speedX', 'angle','contact'
                ]
        Observation = col.namedtuple('Observaion', names)
        return Observation(focus=np.array(self.laserRead,dtype=np.float32)/30,
                           speedX=self.realVelX/15,
                           angle=self.ang/0.5,
                           contact=self.contact)

    def step(self, u):

        # convert thisAction to the actual torcs actionstr

        #client = self.client


        # One-Step Dynamics Update #################################
        # Apply the Agent's action into torcs
        this_action = self.publish(u)

        # Get the current full-observation from torcs
        #obs =

        # Make an obsevation from a raw observation vector from TORCS
        self.observation = self.make_observaton()
        # print(self.ang,self.realVelX)
        # Reward setting Here #######################################
        reward = self.calcReward()

        if self.time_step>700:
            if self.realVelX<0.4:
                self.stopcount +=1
                if self.stopcount>300:
                    self.msgTwist.linear.x = 100
                    self.pub_cmdvel.publish(self.msgTwist)
                    time.sleep(1)
            else:
                self.stopcount=0

        for a in range(4):
            if not self.contact[a]:
                reward -=1



        if self.resetter:
            reward = -100

        self.time_step += 1



        return self.observation, reward, self.resetter, {}