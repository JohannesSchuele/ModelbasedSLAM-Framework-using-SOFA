#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 22 11:55:53 2021

@author: jona
"""
from qtpy.QtCore import *
from qtpy.QtWidgets import *
import matlab.engine
import numpy as np
# from numpy.linalg import norm
from scipy.io import savemat
from .SofaGLViewer import SofaGLViewer
from .SofaSim import SofaSim

class EngineORB:
   
    def __init__(self, mat_dir, n_init_images=10, skip_images_init = 0, skip_images_main = 2):   
        # print("starting matlab engine ...")
        # # Start matlab engine
        # self.mat = matlab.engine.start_matlab() #"-desktop -r 'format short'"
        # print("started successfully")
        self.mat = matlab.engine.connect_matlab() # share by running "matlab.engine.shareEngine" in matlab command prompt
        # Go to slam directory
        self.mat.cd(mat_dir, nargout=0)
        self.n_init_images = n_init_images
        self.skip_images = skip_images_init
        self.skip_images_main = skip_images_main
        self.skip_counter = skip_images_init #start immediately
        self.is_mapping = False
        self.is_initialized = False
        self.k = 0
        self.step = 1
        self.position = np.zeros(3)
        self.orientation = np.zeros(4)
        
    def set_viewer(self, viewer: SofaGLViewer):
        self.viewer = viewer
        self._viewer_set = True
        # try:
        #     self._update_timer.disconnect()
        # except TypeError:
        #     pass
        # self._update_timer.timeout.connect(self.viewer.update)
        self.viewer.key_pressed.connect(self.keyPressEvent)
        # self.viewer.key_released.connect(self.keyReleaseEvent)
    
    def set_sim(self, sim: SofaSim):
        self.sofa_sim = sim
        self._sim_set = True

    def viewer_info(self, viewer_size, intrinsics):
        self.viewer_size = viewer_size
        self.intrinsics = intrinsics
        # create an empty array to store all init_images
        self.width = self.viewer_size[0]
        self.height = self.viewer_size[1] 
        self.init_images = np.empty([self.height*self.n_init_images, self.width, 3])
        
    def initialize_slam(self, image):
        self.k += 1
        self.init_images[(self.k-1)*self.height:self.k*self.height,:,:] = image
        if self.k == self.n_init_images:
            # set stuff for matlab: n_init_images, init_images, focalLength, principalPoint, viewer_size
            initdic = {"initImages": self.init_images,
                    "numberOfInitialImages": self.n_init_images,
                    "focalLength": np.array([self.intrinsics[0],self.intrinsics[1]]),
                    "principalPoint": np.array([self.intrinsics[2],self.intrinsics[3]]),
                    "viewerWidth": self.width,
                    "viewerHeight": self.height}
            savemat("../orb_slam_matlab_for_qt_viewer/initImages.mat", initdic)
            # self.mat.workspace['initImages'] = self.matInitImages
            # self.mat.workspace['numberOfInitialImages'] = self.n_init_images
            # self.mat.workspace['focalLength'] = matlab.double(self.intrinsics[0:1])
            # self.mat.workspace['principalPoint'] = matlab.double(self.intrinsics[2:3])
            # self.mat.workspace['viewerWidth'] = self.width
            # self.mat.workspace['viewerHeight'] = self.height 
            self.mat.initialize_slam(nargout=0)
            self.is_initialized = True
            self.skip_images = self.skip_images_main
                
    def main_slam(self, image):
        self.step += 1
        maindic = {"currI": image}
        savemat("../orb_slam_matlab_for_qt_viewer/currI.mat", maindic)
        self.mat.main_loop_slam(nargout=0)
        
    def stop_slam(self):
        self.is_mapping = False
        self.mat.finish_slam(nargout=0)
        
    def get_camera_position(self):
        new_position = np.array(self.sofa_sim.root.camera.position.value)
        change_pos = new_position-self.position
        if self._sim_set and np.linalg.norm(change_pos) != 0:
            print(self.sofa_sim.root.camera.position.value)
        self.position = new_position
        # return camera.position.value
    
    def get_camera_orientation(self):
        new_orientation = np.array(self.sofa_sim.root.camera.orientation.value)
        change_ori = new_orientation-self.orientation
        if self._sim_set and np.linalg.norm(change_ori) != 0:
            print(self.sofa_sim.root.camera.orientation.value)
        self.orientation = new_orientation
        # return camera.orientation.value
    
    def keyPressEvent(self, QKeyEvent):
        if QKeyEvent.key() == Qt.Key_Space:
            if self.sofa_sim.is_animating and self.is_mapping:
                self.stop_slam()
                
        if QKeyEvent.key() == Qt.Key_G: # G for GO
            if self.is_mapping:
                self.stop_slam()
            elif self.sofa_sim.is_animating:
                print("Let's go")
                self.is_mapping = True
                self.sofa_sim.animation_end.connect(self.update_slam) # set a qt signal to update slam after sim step
                self.viewer_info(viewer_size=self.viewer.get_viewer_size(), intrinsics=self.viewer.get_intrinsic_parameters())
    
    def update_slam(self):
        if self.skip_counter == self.skip_images:
            self.skip_counter = 0
            if self.is_initialized:
                self.main_slam(image=self.viewer.get_screen_shot())
            else:
                self.initialize_slam(image=self.viewer.get_screen_shot())
        else:
            self.skip_counter += 1