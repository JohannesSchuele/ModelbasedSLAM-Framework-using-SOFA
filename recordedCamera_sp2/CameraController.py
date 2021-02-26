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
mat.cd('/Users/jona/slam/matlab_slam/openslam_ekfmonoslam/matlab_code', nargout=0)
#updateFrequency = 5



class controller(Sofa.PythonScriptController):

    def initGraph(self, node):
        self.node = node
        self.totalTime = 0.0
        self.startSLAM = 0
        self.isInitalized = 0
        self.hasWaited = 0
        self.sequenceDIR = '/Users/jona/sofa/build/screenshots/'
        self.resizedSize = (1530,1200)
        # Get index of last image as integer
        self.list_of_files = glob.glob(self.sequenceDIR+'*') # * means all if need specific format then *.csv
        if self.list_of_files == []:
            self.initIm = 1
        else:
        self.latest_file = max(self.list_of_files, key=os.path.getctime)
        self.initIm = int(self.latest_file[-12:-4])+1

    
    def onEndAnimationStep(self, dt):
        self.totalTime += dt
        if self.startSLAM:
            self.list_of_files = glob.glob(self.sequenceDIR+'*') # * means all if need specific format then *.csv
            self.latest_file = max(self.list_of_files, key=os.path.getctime)
            self.latestIm = int(self.latest_file[-12:-4])
            if self.latestIm >= self.initIm and not self.isInitalized:
                print('Initalize SLAM')
                mat.workspace['own_sequence'] = 1
                mat.workspace['initIm'] = self.initIm
                mat.initalize_slam(nargout=0)
                mat.workspace['step'] = mat.workspace['initIm']+1
                self.isInitalized = 1
                    
            if self.isInitalized and self.latestIm >= mat.workspace['step']:
            #        time.sleep(5)
                mat.slam_step(nargout=0)
                print(mat.workspace['step'])
                mat.workspace['step'] += 1
                self.currentImage = str(self.latestIm).zfill(8)
                foo = Image.open(self.sequenceDIR+'RecordedCameraPython_'+self.currentImage+'.png')
                foo.save(self.sequenceDIR+'RecordedCameraPython_'+self.currentImage+'.png',optimize=True,quality=90)

    

    def onKeyPressed(self, c):
    
        # Start Recording
        keyboard = Controller()
        keyboard.press('v')
        keyboard.release('v')
        #stop animation and recording - recording continues if animation is started again
        #start animation again not possible from inside controller, has to be done manually
        # 'a' key
        if ord(c) == 65:
            if not self.startSLAM:
                print('Start SLAM')
                self.startSLAM = 1
            else:
                print('Stop SLAM')
                self.startSLAM = 0

#            mat.mono_slam(nargout=0)
#            mat.quit()
#            self.node.animate = 0
       


