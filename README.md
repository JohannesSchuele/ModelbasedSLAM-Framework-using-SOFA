# GIT_ORB_SLAM_MATLAB
This project is a proof of concept implementation of a model-based localization algorithm for deformable systems. The proposed approach considers a real-time co-simulation to predict deformations. The simulated deformations are incorporated in a state-of-the-art simultaneous localization and mapping (SLAM) algorithm to enable precise localization in an endoscopic, non-rigid environment.
Thefore we use the Simulation Open Framework Architecture https://www.sofa-framework.org/ (SOFA).
An ideal model and accurate knowledge of the acting forces are assumed. 
This work is intended as proof of concept to provide fundamental ideas and the framework to apply a model-based localization algorithm in a real-world endoscopic surgery environment. 
![image](https://user-images.githubusercontent.com/62347327/136781115-92a76623-bb7b-4751-8c9d-59e531e68ec0.png)


 Added matlab orb slam using qt viewer
 Most important controls:
 SPACE: start/ stop simulation
 
 Overview different navigation modes:
 "tofile"
        control the camera and generate a trajectory (array containing position and orientation of the camera at each time step)
        trajectory_path is the folder where the output is written to (.txt-file)
        if trajectory_path=="./trajectories/navigation/": you can navigate however you want and press H to add the current camera configuration to keypoint array
        not that in this case you can select as many keypoints as you like, the path between them is not important (see keypoint_navigation), however by default also the current sim_step (so basically a timestamp) is part of the keypoint and thus determines the navigation speed. You can change the timestamps in keypoints.txt to change the speed of each part of the movement
 "fromfile"
        uses the files in the specified folder trajectory_path and reads out position and orientation of the camera for each simulation step
 "keypoint_navigation"
        keypoints are read and then connected trough linear interpolation to generate a trajectory that passes each keypoint at the specified time
        
-> all of this is a little messy atm but seems to work reliably enough, but I will try to clean this up a little, to/fromfile-mode (no keypoint_navigation) are relatively complicated to use because the camera movement using the key controls is not completely intuitive at times, thus resulting in unwanted movements
-> keypoint navigation allows you to use points of interest and just connect them in a linear fashion, while at the same time determining the speed of the movement
-> however to get a continuous/smooth motion you might need many keypoints (or finetune them) which takes some time
 
# Prerequisites
Sofa Python3 bindings
qtpy, PyQt5
pyqtgraph
networkx
cv2

# Workflow
Load scene with controller commented out -> change viewer -> uncomment line 18 -> reload scene (cmd+'r') -> start animate ->  cmd+'a' to start/stop SLAM 


# Improvements TODO:
 1. outsource all trajectory related computation, read/write, etc. into seperate class
 2. test transformation of map (translation etc.) / accessability of worldPointSet
 3. improve body / texture
 4. export mesh from sofa: vtk exporter, monitor, state exporter
 5. add option to save sequence, groundTruth and map together at the end 
 
 
 # Tuning parameters SLAM:
 1. fps/movement velocity
 2. helperIsKeyFrame: 
     - minimum number of frames that have to pass before new keyFrame is allowed
     - minimum number of map points
     - tracked points ratio between current frame and last keyFrame
     -> obviously more keyFrames "=" more accuracy but also more expensive computationally, thus slower
 3. numLevels, scaleFactor of detectORBFeatures determine feature detection performance
 
 
 
#  Additonal Information:

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

UPDATE 29/01/2021:
1. updated camera calibration, should now work better
2. added comments
3. self.lowerQualityImmediately lets you decide whether to lower image quality/size at the end of the process (after finishing slam) or at each step-> speeds things up quite a bit but takes very long at the end. If you just want to test stuff it is best to leave it at 0 and comment out the stuff at the end
4. added sofa ground truth, also scales the map
5. changed rotation of recordedCamera, now starts at (0,0,0) facing in z-direction. Same starting position as SLAM
6. "real" camera (in sofa) and tracked camera (slam) are now in sync due to 4. and 5. (dimensions, axis,...) 
7. extension of 6.: added automatic SLAM start when starting the animation/simulation in sofa. cmd+'a' still stops SLAM and evaluates ground truth (see orb_slam_matlab/groundTruthcompareGroundTruth.m)
8. added example sequence and corresponding ground truth in 'example', you can test this with slam_whole_in_one.m



