clear all; close all;
addpath 'helperFunctions' 'initialization_steps' 'groundTruth'
load initImages.mat
initIm = 1;
% Inspect the first image
currFrameIdx = initIm;
% currI = readimage(imds, currFrameIdx);
imageSize = double([viewerHeight, viewerWidth]);
initImages = uint8(initImages);
currI = initImages(1:viewerHeight,:,:);
% himage = imshow(currI);

%% Load camera intrinsics
intrinsics = cameraIntrinsics(focalLength, principalPoint, imageSize);
%% Map initialization
map_initialization

%% Store Initial Key Frames and Map Points
store_initial_key_frames_and_map_points

%% Refine and Visualize the Initial Reconstruction
refine_and_visualize_initial_reconstruction

%% Tracking
% ViewId of the current key frame
currKeyFrameId    = currViewId;

% ViewId of the last key frame
lastKeyFrameId    = currViewId;

% ViewId of the reference key frame that has the most co-visible 
% map points with the current key frame
refKeyFrameId     = currViewId;

% Index of the last key frame in the input image sequence
lastKeyFrameIdx   = currFrameIdx - 1; 

% Indices of all the key frames in the input image sequence
addedFramesIdx    = [initIm; lastKeyFrameIdx];

isLoopClosed      = false;
