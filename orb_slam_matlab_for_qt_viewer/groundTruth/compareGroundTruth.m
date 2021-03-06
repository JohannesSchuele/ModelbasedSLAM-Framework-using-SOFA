%% Compare sofa ground truth with slam trajectory
%load ground truth
% transform ground truth into slam coordinates
% update plot based on trajectory (scale..)
% scale??????

% save('groundTruth/sofaGroundTruth.mat',...
%     'sofaGroundTruth_pos','sofaGroundTruth_ori');
load('groundTruth/groundTruth.mat');
translation = -sofaGroundTruth_pos(1,:)';
rotation = [1 0 0; 0 -1 0; 0 0 -1];
sofaGroundTruth_pos_transformed = [eye(3) translation; 0 0 0 1] *...
    [sofaGroundTruth_pos'; ones(1,length(sofaGroundTruth_pos))];
sofaGroundTruth_pos_transformed = [rotation zeros(3,1); 0 0 0 1] *...
    sofaGroundTruth_pos_transformed;
sofaGroundTruth_pos_transformed = sofaGroundTruth_pos_transformed(1:3,:)';
 
% Plot the actual camera trajectory 
tweaked_plotActualTrajectory(mapPlot, sofaGroundTruth_pos_transformed, optimizedPoses);

% Show legend
showLegend(mapPlot);

% Evaluate tracking accuracy
tweaked_helperEstimateTrajectoryError(sofaGroundTruth_pos_transformed, optimizedPoses);




