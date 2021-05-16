addpath ../helperFunctions
load final_results_3/prediction_immediate_force3/resultsProjection.mat
mapPlot = helperVisualizeMotionAndStructure(vSetKeyFrames, mapPointSet);
plot3(mapPlot.Axes, sofaGroundTruth_pos_slam(:,1), sofaGroundTruth_pos_slam(:,2), sofaGroundTruth_pos_slam(:,3), ...
                'r','LineWidth',2, 'DisplayName', 'Actual trajectory');
% showLegend(mapPlot);
% set(gcf,'color','w');
% set(gca,'color','w');

% 
figure
points = mapPointSet.WorldPoints(:,:);
plot3(points(:,1),points(:,2),points(:,3),'.','MarkerSize',0.5)
hold on
grid on
axis([-1.5 1.5 -1.5 1.5 -0.5 2.5]);
views = vSetKeyFrames.Views;
poses = zeros(vSetKeyFrames.NumViews,3);
for i = 1:vSetKeyFrames.NumViews
    poses(i,:) = views.AbsolutePose(i).Translation;
end
plot3(poses(:,1),poses(:,2),poses(:,3), 'r','LineWidth',2)
plot3(sofaGroundTruth_pos_slam(:,1), sofaGroundTruth_pos_slam(:,2), sofaGroundTruth_pos_slam(:,3), ...
                'g','LineWidth',2);
legend('Weltpunkte', 'Geschätzte Trajektorie', 'Tatsächliche Trajektorie')


% 
% X = points(:,1);
% S = repmat([50,25,10],numel(X),1);
% C = repmat([1,2,3],numel(X),1);
% s = S(:);
% c = C(:);
% scatter3(points(:,1),points(:,2),points(:,3),c,'filled')
% view(-30,10)