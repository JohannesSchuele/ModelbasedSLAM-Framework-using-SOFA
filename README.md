# GIT_ORB_SLAM_MATLAB
 
Contains Matlab Code for ORB SLAM + Sofa scene using RecordedCamera component to generate screenshots.
TODO before use:
1. change self.sequenceDIR (line 28, CameraControllerORB.py) to your sofa screenshot directory
2. make sure to have all python modules/libraries (PIL, pynput,...) installed
3. MATLAB 2020b is needed since one of the functions used was added with that release

Important: Since OpenGL Viewer has to be used for RecordedCamera, the scene probably has to be loaded once with line 18 (add Controller) commented out before changing the viewer. 
When changing to OpenGL first and then loading the scene the lighting of the object might be flawed (at least with my current version of sofa). Once the controller is loaded you cannot reload it since Matlab engine won't work anymore - so atm I completely quit sofa and go through this whole process again after trying the scene once which is pretty annoying and inefficient -> Working on a fix.

workflow: load scene with controller commented out -> change viewer -> uncomment line 18 -> reload scene (cmd+'r') -> start animate ->  cmd+'a' to start/stop SLAM 

Everything else should work right off the bat. 
Regarding possible error in line 3 (estimateGeometricTransform2D) of "helperFunctions/helperComputeHomography.m": This function was added in MATLAB 2020b so mat.engine for 2020b has to be used.
More information about this: https://de.mathworks.com/help/matlab/matlab_external/install-the-matlab-engine-for-python.html

Improvements TODO:
1. test deformation of body in sofa, add mechanical properties, force
2. test transformation of map (translation etc.) / accessability of worldPointSet
3. improve body / texture
4. Fix matlab engine problem
5. export mesh from sofa: vtk exporter, monitor, state exporter
6. add NavigationRecordedCameraScene for different movement
7. add option to save sequence, groundTruth and map together at the end

UPDATE 29/01/2021:
1. updated camera calibration, should now work better
2. added comments
3. self.lowerQualityImmediately lets you decide whether to lower image quality/size at the end of the process (after finishing slam) or at each step-> speeds things up quite a bit but takes very long at the end. If you just want to test stuff it is best to leave it at 0 and comment out the stuff at the end
4. added sofa ground truth, also scales the map
5. changed rotation of recordedCamera, now starts at (0,0,0) facing in z-direction. Same starting position as SLAM
6. "real" camera (in sofa) and tracked camera (slam) are now in sync due to 4. and 5. (dimensions, axis,...) 
7. extension of 6.: added automatic SLAM start when starting the animation/simulation in sofa. cmd+'a' still stops SLAM and evaluates ground truth (see orb_slam_matlab/groundTruthcompareGroundTruth.m)
8. added example sequence and corresponding ground truth in 'example', you can test this with slam_whole_in_one.m

Tuning parameters SLAM:
1. fps/movement velocity
2. helperIsKeyFrame: 
    - minimum number of frames that have to pass before new keyFrame is allowed
    - minimum number of map points
    - tracked points ratio between current frame and last keyFrame
    -> obviously more keyFrames "=" more accuracy but also more expensive computationally, thus slower

