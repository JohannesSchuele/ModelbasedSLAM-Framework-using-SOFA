% Set up point cloud player
% xlimits = [-10 10];
% ylimits = [-10 10];
% zlimits = [-10 10];
% player = pcplayer(xlimits,ylimits,zlimits);
% xlabel(player.Axes,'X (m)');
% ylabel(player.Axes,'Y (m)');
% zlabel(player.Axes,'Z (m)');
addpath '../helperFunctions'
load resultsTest.mat
% Convert map points to pointCloudObject
ptCloud = [mapPlot.Axes.Children(end).XData;...
    mapPlot.Axes.Children(end).YData;...
    mapPlot.Axes.Children(end).ZData]';
ptCloud = pointCloud(ptCloud);
ptCloud = pcdenoise(ptCloud);
gridStep = 0.1;
ptCloudA = pcdownsample(ptCloud,'gridAverage',gridStep);
% Load stl and convert to pointCloud
data = stlread('../../mesh/blender_ellipsoid.stl');
theta = 0;
rot = [cos(theta) sin(theta) 0; ...
      -sin(theta) cos(theta) 0; ...
               0          0  1];
trans = [0, 0, 5];
tform = rigid3d(rot,trans);
ptCloud_STL = pctransform(pointCloud(data.Points),tform);

% ptCloud_STL = pointCloud(data.Points+[0 0 5]);
% Display both
pcshowpair(ptCloudA, ptCloud_STL)
