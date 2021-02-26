#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 22 11:55:53 2021

@author: jona
"""
import matlab.engine
import numpy as np
from scipy.io import savemat

class EngineORB:
   
    def __init__(self, mat_dir, n_init_images=10, skip_images = 0):   
        # print("starting matlab engine ...")
        # # Start matlab engine
        # self.mat = matlab.engine.start_matlab() #"-desktop -r 'format short'"
        # print("started successfully")
        self.mat = matlab.engine.connect_matlab() # share by running "matlab.engine.shareEngine" in matlab command prompt
        # Go to slam directory
        self.mat.cd(mat_dir, nargout=0)
        self.n_init_images = n_init_images
        self.skip_images = skip_images
        self.skip_counter = skip_images #start immediately
        self.is_mapping = False
        self.is_initialized = False
        self.k = 0
        self.step = 1

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
            print("Let's go")
            self.mat.initialize_slam(nargout=0)
            self.is_initialized = True
            self.skip_images = 2
                
    def main_slam(self, image):
        self.step += 1
        maindic = {"currI": image}
        savemat("../orb_slam_matlab_for_qt_viewer/currI.mat", maindic)
        self.mat.main_loop_slam(nargout=0)
        
    def stop_slam(self):
        self.is_mapping = False
        self.mat.finish_slam(nargout=0)
        
    def get_camera_position(self, camera):
        print(camera.position.value)
        return camera.position.value
    
    def get_camera_orientation(self, camera):
        return camera.orientation.value