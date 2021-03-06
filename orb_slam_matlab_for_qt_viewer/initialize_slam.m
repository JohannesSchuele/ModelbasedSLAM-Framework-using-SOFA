clear all; close all;
addpath 'helperFunctions' 'initialization_steps' 'groundTruth'
load initI.mat
initIm = 1;
% Inspect the first image
currFrameIdx = initIm;
% currI = readimage(imds, currFrameIdx);
imageSize = double([viewerHeight, viewerWidth]);
currI = uint8(currI);
% himage = imshow(currI);

%% Load camera intrinsics
intrinsics = cameraIntrinsics(focalLength, principalPoint, imageSize);

%% Start of map initialization
% Set random seed for reproducibility
rng(0);

% Detect and extract ORB features
scaleFactor = 1.2;
numLevels   = 8;
[preFeatures, prePoints] = helperDetectAndExtractFeatures(currI, scaleFactor, numLevels, intrinsics); 

currFrameIdx = currFrameIdx + 1;
firstI       = currI; % Preserve the first frame 

isMapInitialized  = false;

%% Map initialization
% map_initialization
