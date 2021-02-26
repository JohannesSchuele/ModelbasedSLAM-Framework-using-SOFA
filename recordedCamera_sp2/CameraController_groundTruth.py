import Sofa
import math
from pynput.keyboard import Key, Controller
#import matlab.engine
import time
import glob
import os
import re
from PIL import Image




class controller(Sofa.PythonScriptController):

    def initGraph(self, node):
        self.node = node
        self.object = self.node.getChild('ellipsoid')
#        self.object.createObject('BoxROI', name='boxROI', box='-0.1 0.3 3.5 1.0 1.5 4.5', drawBoxes=True)
#        print(len(self.forces.value))
        self.totalTime = 0.0
        
    def onEndAnimationStep(self, dt):
        self.totalTime += dt
        startForce = 0
        endForce = 25
        startTime = 10
        endTime = 50
        if self.totalTime >= startTime and self.totalTime <= endTime:
            forces = ""
            for i in range(1,29):
                xForce = startForce + (endForce-startForce) * (self.totalTime-startTime)/(endTime-startTime)
                yForce = startForce + (endForce-startForce) * (self.totalTime-startTime)/(endTime-startTime)
                zForce = startForce + (endForce-startForce) * (self.totalTime-startTime)/(endTime-startTime)
                forces = forces + str(xForce) + " " + str(yForce) + " " + str(zForce) + " "
            self.object.getObject('CFF').findData('forces').value = forces
    
    

    def onKeyPressed(self, c):
        # 'a' key
        if ord(c) == 65:
            forces = ""
            for i in range(1,29):
                forces = forces + "0 0 10 "
            self.object.getObject('CFF').findData('forces').value = forces
       
