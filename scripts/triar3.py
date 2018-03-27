#!/usr/bin/env python

import sys
import random
from math import cos, sin, atan, pow
import numpy as np
PI = 3.14159265359


class triar3:

    def __init__(self):

        self.vel = 0
        self.ang = 0

        self.laserReading = []
        self.noOfsamples = 50

        self.epsilon = 0.01
        self.discount = 0.3
        self.actions = []
        self.states = []
        self.Q = {}

        self.time = 0

        self.angVals = np.arange(-0.2, 0.25, 0.05)
        self.velIncVals = np.arange(-4, 5, 2)
        self.velocities = np.arange(0, 20, 2)
        self.laserVals = np.arange(5, 35, 10)
        self.laserPosCombs = []

        for velocityInc in self.velIncVals:
            for angle in self.angVals:
                self.actions.append((velocityInc, angle))

        for i1 in self.laserVals:
            for i2 in self.laserVals:
                for i3 in self.laserVals:
                    for i4 in self.laserVals:
                        for i5 in self.laserVals:
                            self.laserPosCombs.append((i1, i2, i3, i4, i5))

        for velocity in self.velocities:
            for laserComb in self.laserPosCombs:
                self.states.append((velocity, laserComb))
                temp_dic = {}
                for a in self.actions:
                    temp_dic[a] = 0.0
                self.Q[(velocity, laserComb)] = temp_dic

def main(argv):
    node = triar3()
    print node.states
if __name__ == '__main__':
    main(sys.argv[1:])

