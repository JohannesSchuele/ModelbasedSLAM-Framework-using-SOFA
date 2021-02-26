load currI.mat
currI = uint8(currI);
%% Tracking
[currFeatures, currPoints] = helperDetectAndExtractFeatures(currI, scaleFactor, numLevels, intrinsics);

% Track the last key frame
% mapPointsIdx:   Indices of the map points observed in the current frame
% featureIdx:     Indices of the corresponding feature points in the 
%                 current frame
[currPose, mapPointsIdx, featureIdx] = helperTrackLastKeyFrame(mapPointSet, ...
    vSetKeyFrames.Views, currFeatures, currPoints, lastKeyFrameId, intrinsics, scaleFactor);

% Track the local map
% refKeyFrameId:      ViewId of the reference key frame that has the most 
%                     co-visible map points with the current frame
% localKeyFrameIds:   ViewId of the connected key frames of the current frame
[refKeyFrameId, localKeyFrameIds, currPose, mapPointsIdx, featureIdx] = ...
    helperTrackLocalMap(mapPointSet, directionAndDepth, vSetKeyFrames, mapPointsIdx, ...
    featureIdx, currPose, currFeatures, currPoints, intrinsics, scaleFactor, numLevels);

% Check if the current frame is a key frame. 
% A frame is a key frame if both of the following conditions are satisfied:
%
% 1. At least 20 frames have passed since the last key frame or the 
%    current frame tracks fewer than 80 map points
% 2. The map points tracked by the current frame are fewer than 90% of 
%    points tracked by the reference key frame
isKeyFrame = helperIsKeyFrame(mapPointSet, refKeyFrameId, lastKeyFrameIdx, ...
    currFrameIdx, mapPointsIdx);

% Visualize matched features
% updatePlot(featurePlot, currI, currPoints(featureIdx));

if ~isKeyFrame
    currFrameIdx = currFrameIdx + 1;
    return
end

% Update current key frame ID
currKeyFrameId  = currKeyFrameId + 1;

%% Local Mapping
% Add the new key frame 
[mapPointSet, vSetKeyFrames] = helperAddNewKeyFrame(mapPointSet, vSetKeyFrames, ...
    currPose, currFeatures, currPoints, mapPointsIdx, featureIdx, localKeyFrameIds);

% Remove outlier map points that are observed in fewer than 3 key frames
[mapPointSet, directionAndDepth, mapPointsIdx] = helperCullRecentMapPoints(mapPointSet, directionAndDepth, mapPointsIdx, newPointIdx);

% Create new map points by triangulation
minNumMatches = 20;
minParallax = 3;
[mapPointSet, vSetKeyFrames, newPointIdx] = helperCreateNewMapPoints(mapPointSet, vSetKeyFrames, ...
    currKeyFrameId, intrinsics, scaleFactor, minNumMatches, minParallax);

% Update view direction and depth
directionAndDepth = update(directionAndDepth, mapPointSet, vSetKeyFrames.Views, [mapPointsIdx; newPointIdx], true);

% Local bundle adjustment
[mapPointSet, directionAndDepth, vSetKeyFrames, newPointIdx] = helperLocalBundleAdjustment(mapPointSet, directionAndDepth, vSetKeyFrames, ...
    currKeyFrameId, intrinsics, newPointIdx); 

% Visualize 3D world points and camera trajectory
updatePlot(mapPlot, vSetKeyFrames, mapPointSet);

%% Loop Closure
% % Initialize the loop closure database
% if currKeyFrameId == 3
%     % Load the bag of features data created offline
%     bofData         = load('bagOfFeaturesData.mat');
%     loopDatabase    = invertedImageIndex(bofData.bof);
%     loopCandidates  = [1; 2];
% 
% % Check loop closure after some key frames have been created    
% elseif currKeyFrameId > 20
% 
%     % Minimum number of feature matches of loop edges
%     loopEdgeNumMatches = 50;
% 
%     % Detect possible loop closure key frame candidates
%     [isDetected, validLoopCandidates] = helperCheckLoopClosure(vSetKeyFrames, currKeyFrameId, ...
%         loopDatabase, currI, loopCandidates, loopEdgeNumMatches);
% 
%     if isDetected 
%         % Add loop closure connections
%         [isLoopClosed, mapPointSet, vSetKeyFrames] = helperAddLoopConnections(...
%             mapPointSet, vSetKeyFrames, validLoopCandidates, currKeyFrameId, ...
%             currFeatures, currPoints, intrinsics, scaleFactor, loopEdgeNumMatches);
%     end
% end

% % If no loop closure is detected, add the image into the database
% if ~isLoopClosed
%     currds = imageDatastore(sprintf('%s%08d.png',imageSequence,currFrameIdx));
%     addImages(loopDatabase, currds, 'Verbose', false);
%     loopCandidates= [loopCandidates; currKeyFrameId]; 
% end

% Update IDs and indices
lastKeyFrameId  = currKeyFrameId;
lastKeyFrameIdx = currFrameIdx;
addedFramesIdx  = [addedFramesIdx; currFrameIdx]; 
currFrameIdx  = currFrameIdx + 1;

