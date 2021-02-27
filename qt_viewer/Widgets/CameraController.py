import Sofa
import Sofa.Core
from Sofa.constants import *



class controller(Sofa.Core.Controller):
    """ This is a custom controller to perform actions when events are triggered """
    def __init__(self, *args, **kwargs):
        # These are needed (and the normal way to override from a python class)
        Sofa.Core.Controller.__init__(self, *args, **kwargs)

        self.node = kwargs.get("node")
        self.camera = self.node.camera
        self.totalTime = 0.0
        self.object = self.node.getChild('ellipsoid')
        self.startForce = 0
        self.endForce = 50
        self.startTime = 2
        self.endTime = 15

    def onAnimateEndEvent(self, event):
        self.totalTime += event['dt']
        if self.totalTime <= 1:
            self.node.camera.position += [0., 0.01, 0.]
        elif self.totalTime <= 2:
            self.node.camera.position += [0.01, 0., 0.]
        elif self.totalTime <= 4:
            self.node.camera.position += [0., -0.01, 0.01]
        elif self.totalTime <= 6:
            self.node.camera.position += [-0.01, 0., -0.01]
        elif self.totalTime <= 7:
            self.node.camera.position += [0., 0.01, 0.]
        elif self.totalTime <= 8:
            self.node.camera.position += [0.01, 0., 0.]
            

        if self.totalTime >= self.startTime and self.totalTime <= self.endTime:
            n = len(self.object.boxROI.findData("indices").value)
            forces = []
            xForce = self.startForce + (self.endForce-self.startForce) * (self.totalTime-self.startTime)/(self.endTime-self.startTime)
            yForce = self.startForce + (self.endForce-self.startForce) * (self.totalTime-self.startTime)/(self.endTime-self.startTime)
            zForce = self.startForce + (self.endForce-self.startForce) * (self.totalTime-self.startTime)/(self.endTime-self.startTime)
            for i in range(1,n+1):
                forces.append([xForce,yForce,zForce])
            self.object.CFF.findData('indices').value = self.object.boxROI.findData("indices").value
            self.object.CFF.findData('forces').value = forces
        


#    def onKeypressedEvent(self, event):



