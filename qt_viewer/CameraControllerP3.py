import Sofa
import Sofa.Core
from pynput.keyboard import Key, Controller
from Sofa.constants import *
import math
#from pynput.keyboard import Key, Controller
from Sofa.constants import *
import time


# Go to slam directory


class controller(Sofa.Core.Controller):
    """ This is a custom controller to perform actions when events are triggered """
    def __init__(self, *args, **kwargs):
        # These are needed (and the normal way to override from a python class)
        Sofa.Core.Controller.__init__(self, *args, **kwargs)

        self.node = kwargs.get("node")
#        self.camera = self.node.camera
        self.totalTime = 0.0
        self.object = self.node.getChild('ellipsoid')
        self.forces = []
        self.printIndices = True
        self.applyForces = True

    def onAnimateEndEvent(self, event):
        self.totalTime += event['dt']
#        if self.totalTime <= 1:
#            self.node.camera.position += [0., 0.01, 0.]
#        elif self.totalTime <= 2:
#            self.node.camera.position += [0.01, 0., 0.]
#        elif self.totalTime <= 4:
#            self.node.camera.position += [0., -0.01, 0.01]
#        elif self.totalTime <= 6:
#            self.node.camera.position += [-0.01, 0., -0.01]
#        elif self.totalTime <= 7:
#            self.node.camera.position += [0., 0.01, 0.]
#        elif self.totalTime <= 8:
#            self.node.camera.position += [0.01, 0., 0.]
        
#        if self.printIndices:
#            n = len(self.object.boxROI.findData("indices").value)
#            print(n)
#            self.printIndices = False
#            for i in range(1,n+1):
#                self.forces.append([0,0,0])
#            print(len(self.forces))
#        if self.totalTime >= 2 and self.applyForces:
#            self.node.ellipsoid.addObject('ConstantForceField', name="CFF", indices="@boxROI.indices", forces=self.forces, showArrowSize="0.01")
#            self.applyForces = False
            
        startForce = 0
        endForce = 25
        startTime = 5
        endTime = 50
        if self.totalTime >= startTime and self.totalTime <= endTime:
            forces = []
            xForce = startForce + (endForce-startForce) * (self.totalTime-startTime)/(endTime-startTime)
            yForce = startForce + (endForce-startForce) * (self.totalTime-startTime)/(endTime-startTime)
            zForce = startForce + (endForce-startForce) * (self.totalTime-startTime)/(endTime-startTime)
            for i in range(1,32):
                forces.append([xForce,yForce,zForce])
            self.object.CFF.findData('indices').value = self.object.boxROI.findData("indices").value
            self.object.CFF.findData('forces').value = forces


