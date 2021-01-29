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

mat = matlab.engine.start_matlab() #"-desktop -r 'format short'"
print('started successfully')
mat.cd('/Users/jona/Documents/Uni/Bachelorarbeit/capture_scene/orb_slam_matlab', nargout=0)




class controller(Sofa.PythonScriptController):

    def initGraph(self, node):
        self.node = node
        self.recCamera = self.node.getObject('recCamera')
#        self.startSLAM = 0
#        self.isInitalized = 0
#        self.numberOfInitialImages = 20
#        self.sequenceDIR = '/Users/jona/sofa/build/screenshots/'
#        self.resizedSize = (1530,1200)
        self.totalTime = 0.0
        self.camPosArray = []
#        self.camRotArray = matlab.double([])
#        # Get index of last image as integer
#        self.list_of_files = glob.glob(self.sequenceDIR+'*') # * means all if need specific format then *.csv
#        if self.list_of_files == []:
#            self.initIm = 1
#        else:
#            self.latestFile = max(self.list_of_files, key=os.path.getctime)
#            self.initIm = int(self.latestFile[-12:-4])+1
#        print(self.initIm)
        
    def onEndAnimationStep(self, dt):
        self.totalTime += dt
        self.camPos = self.recCamera.findData('position').value[0]
#        self.camPosArray = matlab.double([self.camPosArray, self.camPos])
        self.camPosArray.append(self.camPos)
#        print('Position:')
#        print(self.camPos)
        if self.totalTime >= 50:
            n = len(self.camPosArray)
            self.matCamPosArray = matlab.double(self.camPosArray)
            self.matCamPosArray.reshape((n,3))
            mat.workspace['sofaGroundTruth_trans'] = self.matCamPosArray
            mat.evaluateGroundTruth(nargout=0)
#            print(self.matCamPosArray)
            self.node.animate = False
        
        
        
#        savemat("sofa_groundTruth.mat", mdic)
#        if self.startSLAM:
#            self.list_of_files = glob.glob(self.sequenceDIR+'*') # * means all if need specific format then *.csv
#            if self.list_of_files == []:
#                self.latestIm = 0
#            else:
#                self.latestFile = max(self.list_of_files, key=os.path.getctime)
#                self.latestIm = int(self.latestFile[-12:-4])
#            print('Latest image:'+str(self.latestIm))
#            if not self.isInitalized and self.latestIm >= self.initIm+self.numberOfInitialImages:
#                print('Initalize SLAM')
#                mat.workspace['initIm'] = self.initIm
#                mat.workspace['numberOfInitialImages'] = self.numberOfInitialImages
#                mat.initialize_slam(nargout=0)
#                mat.workspace['step'] = mat.workspace['initIm']+1
#                self.isInitalized = 1
#
#            if self.isInitalized and self.latestIm >= mat.workspace['step']:#and not mat.workspace['isLoopClosed']
#                mat.main_loop_slam(nargout=0)
#                print(mat.workspace['step'])
#                mat.workspace['step'] += 1
#                self.currentImage = str(self.latestIm).zfill(8)
#                foo = Image.open(self.sequenceDIR+'RecordedCameraPython_'+self.currentImage+'.png')
#                foo.save(self.sequenceDIR+'RecordedCameraPython_'+self.currentImage+'.png',optimize=True,quality=90)
#            elif self.isInitalized and mat.workspace['isLoopClosed']:
#                print('LOOP CLOSED')

    

#    def onKeyPressed(self, c):
#
#        # Start Recording
#        keyboard = Controller()
#        keyboard.press('v')
#        keyboard.release('v')
        #stop animation and recording - recording continues if animation is started again
        #start animation again not possible from inside controller, has to be done manually
        # 'a' key
#        if ord(c) == 65:
#            if not self.startSLAM:
#                print('Start SLAM')
#                self.startSLAM = 1
#            else:
#                print('Stop SLAM')
#                mat.finish_slam(nargout=0)
##                mat.quit()
#                self.startSLAM = 0

#            mat.mono_slam(nargout=0)
#            mat.quit()
#            self.node.animate = 0
       
