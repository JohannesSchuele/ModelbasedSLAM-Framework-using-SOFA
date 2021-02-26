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

#    def onKeypressedEvent(self, event):



