import Sofa
import Sofa.Core
from pynput.keyboard import Key, Controller
from Sofa.constants import *
import math
#from pynput.keyboard import Key, Controller
from Sofa.constants import *
import matlab.engine
import time
import glob
import os
import re
import numpy as np
from PIL import Image

print('starting matlab engine ...')
# Start matlab engine
mat = matlab.engine.start_matlab() #"-desktop -r 'format short'"
print('started successfully')
# Go to slam directory
dirname = os.path.dirname(__file__)
matDIR = os.path.join(dirname, '../orb_slam_matlab')
mat.cd(matDIR, nargout=0)


# Go to slam directory


class controller(Sofa.Core.Controller):
    """ This is a custom controller to perform actions when events are triggered """
    def __init__(self, *args, **kwargs):
        # These are needed (and the normal way to override from a python class)
        Sofa.Core.Controller.__init__(self, *args, **kwargs)

        self.node = kwargs.get("node")
        self.recCamera = self.node.camera
        self.totalTime = 0.0
        self.startSLAM = 0
        self.isInitalized = 0
        self.hasWaited = 0
        # sofa screenshot directory
        self.sequenceDIR = '/Users/schuele/sofa_20.12/build_20.12/install/screenshots/' #link to sofa screenshot directory
        mat.workspace['imageFolder'] = self.sequenceDIR

        self.startSLAM = True
        # start recording (taking screenshots) immediately
        if self.startSLAM:
            keyboard = Controller()
            keyboard.press('v')
            keyboard.release('v')

        # number of images to take before starting the initialization
        self.numberOfInitialImages = 20

        self.isInitalized = False
        # number of images to take before starting the initialization
        self.numberOfInitialImages = 20
        # sofa screenshot directory

        self.resizedSize = (1530, 1200)
        self.totalTime = 0.0
        # get recordedCamera to keep track of position and orientation

        self.camPosArray = np.array([])
        self.camRotArray = np.array([])
        
        # resave screenshot with lower quality at each step (1) or at the end (0)
        self.lowerQualityImmediately = False
        
        # Get index of last image as integer, starting index
        self.list_of_files = glob.glob(self.sequenceDIR + '*')  # * means all if need specific format then *.csv
        if self.list_of_files == []:
            self.initIm = 1
        else:
            self.latestFile = max(self.list_of_files, key=os.path.getctime)
            self.initIm = int(self.latestFile[-12:-4]) + 1
        print(self.initIm)


    def onAnimateEndEvent(self, event):

        self.totalTime += event['dt']

        if self.startSLAM:
            # get the current latest image in screenshot directory
            self.list_of_files = glob.glob(self.sequenceDIR + '*')  # * means all if need specific format then *.csv
            if self.list_of_files == []:
                self.latestIm = 0
            else:
                self.latestFile = max(self.list_of_files, key=os.path.getctime)
                self.latestIm = int(self.latestFile[-12:-4])
            print('Latest image:' + str(self.latestIm))

            # add ground truth information (position and orientation) for all frames

            if self.latestIm >= self.initIm:
                self.camPos = self.recCamera.findData('position').value
                self.camPosArray = np.append(self.camPosArray, self.camPos)
                self.camRot = self.recCamera.findData('orientation').value
                self.camRotArray = np.append(self.camRotArray, self.camRot)

            # initialize slam when numberOfInitialImages have been taken
            if not self.isInitalized and self.latestIm >= self.initIm + self.numberOfInitialImages:
                print('Initalize SLAM')
                mat.workspace['initIm'] = self.initIm
                mat.workspace['numberOfInitialImages'] = self.numberOfInitialImages
                mat.initialize_slam(nargout=0)
                mat.workspace['step'] = mat.workspace['initIm'] + 1
                self.isInitalized = True

            # slam main loop, needs to be initialized first and latest image in directory needs to be next in line
            if self.isInitalized and self.latestIm >= mat.workspace['step']:  # and not mat.workspace['isLoopClosed']
                mat.main_loop_slam(nargout=0)
                print(mat.workspace['step'])
                mat.workspace['step'] += 1
                # resave screenshot with lower quality at each step
                if self.lowerQualityImmediately:
                    self.currentImage = str(self.latestIm).zfill(8)
                    foo = Image.open(self.sequenceDIR + 'RecordedCameraPython_' + self.currentImage + '.png')
                    foo.save(self.sequenceDIR + 'RecordedCameraPython_' + self.currentImage + '.png', optimize=True,
                             quality=90)

            elif self.isInitalized and mat.workspace['isLoopClosed']:  # detect loop closure
                print('LOOP CLOSED')  # atm loop closures are not used the stop the slam, so this is just fyi




    def onKeypressedEvent(self, event):
        # Start/stop recording whenever keyPressedEvent is triggered
        keyboard = Controller()
        keyboard.press('v')
        keyboard.release('v')


        # 'a' key
        if event['key'] == Key.A:
            # if self.startSLAM is set to 0 initially then this starts the SLAM
            if not self.startSLAM:
                print('Start SLAM')
                self.startSLAM = True
            # stop SLAM
            else:
                print('Stop SLAM')
                self.startSLAM = False
                # create matlab array containing sofa ground truth for all key frames, probably not the best implementation yet
                self.keyCamPos = np.array([])
                self.keyCamRot = np.array([])
                self.camPosArray = np.reshape(self.camPosArray,(-1,3))
                self.camRotArray = np.reshape(self.camRotArray,(-1,4))
                for i in mat.workspace['addedFramesIdx']:
                    # i - initIm is necessary since
                    # addedFramesIdx corresponds with image index (starts at initIm)
                    # while
                    # camPosArray and camRotArray correspond with frame of the current scene (starts at 0)
                    self.keyCamPos = np.append(self.keyCamPos,self.camPosArray[i[0]-self.initIm,:])
                    self.keyCamRot = np.append(self.keyCamRot,self.camRotArray[i[0]-self.initIm,:])
#                print(self.camPosArray)
                n = int(self.keyCamPos.size/3)
                print(self.keyCamPos)
                print(self.keyCamPos.tolist())
                self.matCamPosArray = matlab.double(self.keyCamPos.tolist())
                self.matCamRotArray = matlab.double(self.keyCamRot.tolist())
                self.matCamPosArray.reshape((3,n))
                self.matCamPosArray = mat.transpose(self.matCamPosArray)
                # orientation is in quaternions
                self.matCamRotArray.reshape((4,n))
                self.matCamRotArray = mat.transpose(self.matCamRotArray)
                print(self.matCamPosArray)
                mat.workspace['sofaGroundTruth_trans'] = self.matCamPosArray
                mat.workspace['sofaGroundTruth_rot'] = self.matCamRotArray
                # call finish_slam which optimizes trajectory, scales map according to ground truth and plots ground truth
                mat.finish_slam(nargout=0)
                # stop the simulation
                self.node.animate = False
                # lower screenshot quality of all files in screenshot directory >= initIm (skip images from "previous slam")
                # takes quite some time, so comment out if you just want to test stuff and manually delete the images afterwards
                if not self.lowerQualityImmediately:
                    self.list_of_files = glob.glob(self.sequenceDIR+'*') # * means all if need specific format then *.csv
                    for f in self.list_of_files:
                        if int(f[-12:-4]) >= self.initIm:
                            foo = Image.open(f)
                            foo.save(f, optimize=True, quality=90)
                print('FINISHED!')


