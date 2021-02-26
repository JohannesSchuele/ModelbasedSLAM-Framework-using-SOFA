#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 22 14:50:11 2021

@author: jona
"""
import numpy as np
import matlab.engine
mat = matlab.engine.start_matlab()
a = np.array([[[1,2,3],[4,5,6],[7,8,9]],[[10,11,12],[13,14,15],[16,17,18]],[[19,20,21],[22,23,24],[25,26,27]]])
matA = matlab.double(a.tolist())
matA.reshape((3,3,3))
matA = mat.permute(matA,[2 1 3])
print(a[0,0,0])
print(matA)