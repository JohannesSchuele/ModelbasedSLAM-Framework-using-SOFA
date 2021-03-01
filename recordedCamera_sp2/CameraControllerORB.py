import Sofa
import math
from pynput.keyboard import Key, Controller
import matlab.engine
import time
import glob
import os
import re
from PIL import Image


print('starting matlab engine ...')
# Start matlab engine
mat = matlab.engine.start_matlab() #"-desktop -r 'format short'"
print('started successfully')
# Go to slam directory
dirname = os.path.dirname(__file__)
matDIR = os.path.join(dirname, '../orb_slam_matlab')
mat.cd(matDIR, nargout=0)




class controller(Sofa.PythonScriptController):

    def initGraph(self, node):
        self.node = node
        # resave screenshot with lower quality at each step (1) or at the end (0)
        self.lowerQualityImmediately = 0
        # start SLAM immediately when starting the simulation
        self.startSLAM = 1
        # start recording (taking screenshots) immediately
        if self.startSLAM:
            keyboard = Controller()
            keyboard.press('v')
            keyboard.release('v')
            
        self.isInitalized = 0
        # number of images to take before starting the initialization
        self.numberOfInitialImages = 20
        # sofa screenshot directory
        self.sequenceDIR = '/Users/jona/sofa/build/screenshots/'
        self.resizedSize = (1530,1200)
        self.totalTime = 0.0
        # get recordedCamera to keep track of position and orientation
        self.recCamera = self.node.getObject('recCamera')
        self.camPosArray = []
        self.camRotArray = []
        # Get index of last image as integer, starting index
        self.list_of_files = glob.glob(self.sequenceDIR+'*') # * means all if need specific format then *.csv
        if self.list_of_files == []:
            self.initIm = 1
        else:
            self.latestFile = max(self.list_of_files, key=os.path.getctime)
            self.initIm = int(self.latestFile[-12:-4])+1
        print(self.initIm)

        
    def onEndAnimationStep(self, dt):
        self.totalTime += dt
        if self.startSLAM:
            # get the current latest image in screenshot directory
            self.list_of_files = glob.glob(self.sequenceDIR+'*') # * means all if need specific format then *.csv
            if self.list_of_files == []:
                self.latestIm = 0
            else:
                self.latestFile = max(self.list_of_files, key=os.path.getctime)
                self.latestIm = int(self.latestFile[-12:-4])
            print('Latest image:'+str(self.latestIm))
            
            #add ground truth information (position and orientation) for all frames
            if self.latestIm >= self.initIm:
                self.camPos = self.recCamera.findData('position').value[0]
                self.camPosArray.append(self.camPos)
                self.camRot = self.recCamera.findData('orientation').value[0]
                self.camRotArray.append(self.camRot)
            
            # initialize slam when numberOfInitialImages have been taken
            if not self.isInitalized and self.latestIm >= self.initIm+self.numberOfInitialImages:
                print('Initalize SLAM')
                mat.workspace['initIm'] = self.initIm
                mat.workspace['numberOfInitialImages'] = self.numberOfInitialImages
                mat.initialize_slam(nargout=0)
                mat.workspace['step'] = mat.workspace['initIm']+1
                self.isInitalized = 1
                
            # slam main loop, needs to be initialized first and latest image in directory needs to be next in line
            if self.isInitalized and self.latestIm >= mat.workspace['step']:#and not mat.workspace['isLoopClosed']
                mat.main_loop_slam(nargout=0)
                print(mat.workspace['step'])
                mat.workspace['step'] += 1
                # resave screenshot with lower quality at each step
                if self.lowerQualityImmediately:
                    self.currentImage = str(self.latestIm).zfill(8)
                    foo = Image.open(self.sequenceDIR+'RecordedCameraPython_'+self.currentImage+'.png')
                    foo.save(self.sequenceDIR+'RecordedCameraPython_'+self.currentImage+'.png',optimize=True,quality=90)

            elif self.isInitalized and mat.workspace['isLoopClosed']: #detect loop closure
                print('LOOP CLOSED') #atm loop closures are not used the stop the slam, so this is just fyi
                

    def onKeyPressed(self, c):
    
        # Start/stop recording whenever keyPressedEvent is triggered
        keyboard = Controller()
        keyboard.press('v')
        keyboard.release('v')
        
        # 'a' key
        if ord(c) == 65:
            # if self.startSLAM is set to 0 initially then this starts the SLAM
            if not self.startSLAM:
                print('Start SLAM')
                self.startSLAM = 1
            # stop SLAM
            else:
                print('Stop SLAM')
                self.startSLAM = 0
                # create matlab array containing sofa ground truth for all key frames, probably not the best implementation yet
                self.keyCamPos = []
                self.keyCamRot = []
                for i in mat.workspace['addedFramesIdx']:
                    # i - initIm is necessary since
                    # addedFramesIdx corresponds with image index (starts at initIm)
                    # while
                    # camPosArray and camRotArray correspond with frame of the current scene (starts at 0)
                    self.keyCamPos.append(self.camPosArray[i[0]-self.initIm])
                    self.keyCamRot.append(self.camRotArray[i[0]-self.initIm])
                n = len(self.keyCamPos)
                self.matCamPosArray = matlab.double(self.keyCamPos)
                self.matCamRotArray = matlab.double(self.keyCamRot)
                self.matCamPosArray.reshape((n,3))
                # orientation is in quaternions
                self.matCamRotArray.reshape((n,4))
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
                            foo.save(f,optimize=True,quality=90)
                print('FINISHED!')

       


