# GIT_ORB_SLAM_MATLAB
 
Contains Matlab Code for ORB SLAM + Sofa scene using RecordedCamera component to generate screenshots.
TODO before use:
1. change self.sequenceDIR (line 28, CameraControllerORB.py) to your sofa screenshot directory
2. make sure to have all python modules/libraries (PIL, pynput,...) installed
3. MATLAB 2020b is needed since one of the functions used was added with that release

Everything else should work right off the bat. 
Regarding possible error in line 3 (estimateGeometricTransform2D) of "helperFunctions/helperComputeHomography.m": This function was added in MATLAB 2020b so mat.engine for 2020b has to be used.
More information about this: https://de.mathworks.com/help/matlab/matlab_external/install-the-matlab-engine-for-python.html

Improvements TODO:
1. change focalLength and principalPoint (camera intrinsics) according to calibration (only change if mapping does not work) -> update calibration??
2. change camera trajectory and generate ground truth from sofa
3. test deformation of body in sofa
4. test transformation of map (translation etc.) / accessability of worldPointSet
5. improve body / texture
