%% Compare sofa ground truth with slam trajectory

save('groundTruth/sofaGroundTruth.mat',...
    'sofaGroundTruth_trans','sofaGroundTruth_rot');
 
% Plot the actual camera trajectory 
tweaked_plotActualTrajectory(mapPlot, sofaGroundTruth_trans, optimizedPoses);

% Show legend
showLegend(mapPlot);

% Evaluate tracking accuracy
tweaked_helperEstimateTrajectoryError(sofaGroundTruth_trans, optimizedPoses);




