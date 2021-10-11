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
% Load stl, convert to pointCloud, and transform (translate and rotate)
stl_data = stlread('../../mesh/blender_ellipsoid.stl');
% transform directly for trimesh plot
stl_data2 = triangulation(stl_data.ConnectivityList,...
    stl_data.Points + [0 0 5]);

% Transformation of stl_data, creating pointCloud
theta = pi/2;
rotz = [cos(theta) sin(theta) 0; ...
       -sin(theta) cos(theta) 0; ...
                0          0  1];
rotx = [1          0          0; ...
        0  cos(theta) sin(theta); ...
        0 -sin(theta) cos(theta)];
trans = [0, 0, 5];
tform = rigid3d(rotz,trans);
ptCloud_STL = pctransform(pointCloud(stl_data.Points),tform);

% Discard all points with positive z value
k = find(stl_data.Points(:,3)<0);
ptCloud_STL_half = pctransform(pointCloud(stl_data.Points(k,:)),tform);

% ptCloud_STL = pointCloud(data.Points+[0 0 5]);
% Display both
pcshowpair(ptCloudA, ptCloud_STL)
figure
% plot3(ptCloud_STL.Location(:,1),ptCloud_STL.Location(:,2),ptCloud_STL.Location(:,3),'o','Color','k');
trimesh(stl_data2,'FaceColor','k','EdgeColor','w')
hold on
plot3(ptCloudA.Location(:,1),ptCloudA.Location(:,2),ptCloudA.Location(:,3),'.','Color','m');


%% Just for fun
% tform2 = pcregistercpd(ptCloud,ptCloud_STL_half);
% ptCloudAReg = pctransform(ptCloud,tform2);
% 
% figure
% pcshowpair(ptCloudAReg,ptCloud_STL_half)
% xlabel('X')
% ylabel('Y')
% zlabel('Z')
% title('Point clouds after registration')
% legend({'SLAM','SOFA'},'TextColor','w')
% legend('Location','southoutside')


%% Orthogonale Projektion
% column 1-3 projected cartesian coordinates
% column 4-6 projected barycentric coordinates
% column 7 isMatched?
% column 8 index of triangulation.ConnectivityList (corresponding triangle)
% column 9-11 barycentric coordinates
% column 12-14 indices of stl points making up the triangle
% need barycentric coordinates and indices of stl points
tic
points = [mapPlot.Axes.Children(end).XData',...
    mapPlot.Axes.Children(end).YData',...
    mapPlot.Axes.Children(end).ZData'];
pointsProjection = zeros(length(points),14);

for i = 1:length(points)
%     disp(i)
    P = points(i,:)';
    pointsProjection(i,1:3) = P';
    % remember which triangles you tried to avoid doubles
    k_tried = [];
    % find closest points
    P_distances = vecnorm(P-stl_data2.Points');
    k = find(P_distances == min(P_distances));
%     k_2 = dsearchn(stl_data2.Points,P');
    k_triangles = vertexAttachments(stl_data2,k);
    k_toTry = k_triangles{1}(:)';
    % TODO: find k_triangle -> k gibt nur Punkte an, jetzt muss
    % jedes Dreieck, dass diesen Punkt enthält geprüft werden,
    % doppelte vermeiden
    j = 1;
    while pointsProjection(i,7) ~= 1 && j <= length(k_toTry)
%     for k_triangle = k_triangles{1}(:)'
        k_triangle = k_toTry(j);
        % get indices of triangle corners
        vertexIDs = stl_data2(k_triangle,:);
        % use indices to get triangle corner coordinates
        A = stl_data2.Points(vertexIDs(1),:)';
        B = stl_data2.Points(vertexIDs(2),:)';
        C = stl_data2.Points(vertexIDs(3),:)';
        % define some vectors
        v0 = B-A;
        v1 = C-A;
        v2 = P-A;
%         % compute the unit normal of current triangle
        n = cross(v0, v1);
%         n = n / dot(n,n);
%         % project P onto the plane and compute barycentric coordinates
%         P_proj = P - dot(v2, n) * n;
%         bary = cartesianToBarycentric(stl_data2,k_triangle,double(P_proj'));
%         % check whether point is inside the triangle
%         if bary(1)>=0 && bary(1)<=1 && bary(2)>=0 && bary(2)<=1 &&...
%             bary(3)>=0 && bary(3)<=1 && sum(bary) == 1
%             pointsProjection(i,4:6) = P_proj';
%             pointsProjection(i,7) = 1;
%             pointsProjection(i,8) = k;
%             pointsProjection(i,9:11) = bary;
%             pointsProjection(i,12:14) = vertexIDs;
%         end
        % directly compute barycentric coordinates
        n_norm = dot(n,n); %vecnorm(n)^2,n'*n,sum(n.^2)
        gamma = (dot(cross(v0, v2),n))/n_norm;
        beta = (dot(cross(v2, v1),n))/n_norm;
        alpha = 1-gamma-beta;
        if alpha>=0 && alpha<=1 && beta>=0 && beta<=1 && gamma>=0 && gamma<=1
            pointsProjection(i,4:6) = [alpha beta gamma]*[A'; B'; C'];
            pointsProjection(i,7) = 1;
            pointsProjection(i,8) = k;
            pointsProjection(i,9:11) = [alpha beta gamma];
            pointsProjection(i,12:14) = vertexIDs;
        end
        % add neighbors to toTry list
%         k_neighbors = neighbors(stl_data2,k_triangle);
%         k_new = setdiff(k_neighbors, k_toTry);
%         k_toTry = [k_toTry k_new];
        j = j+1;
    end
    % if no projection is found using the triangles surrounding the closest
    % point, use the neighbors of those triangles to find projection 
end

toc
%% Plot projection results
figure
trimesh(stl_data2,'FaceColor','k','EdgeColor','w')
hold on
i_unprojected = find(pointsProjection(:,7)==0);
pointsProjection(i_unprojected,4:6) = nan;
plot3(pointsProjection(i_unprojected,1),...
    pointsProjection(i_unprojected,2),...
    pointsProjection(i_unprojected,3),'.','Color','r');
% plot3(pointsProjection(:,1),...
%     pointsProjection(:,2),...
%     pointsProjection(:,3),'.','Color','m');
plot3(pointsProjection(:,4),...
    pointsProjection(:,5),...
    pointsProjection(:,6),'.','Color','g');
legend('STL File','Unprojected Points','Projected Points')

disp(length(i_unprojected));


%%
load presentation.mat
close all 
figure
trimesh(stlData,'FaceColor','w','EdgeColor','k')
% view([0 -30 -90])
hold on; grid off; axis off
A1 = stlData.Points(427,:);
B1 = stlData.Points(449,:);
C1 = stlData.Points(429,:);

plot3(A1(1), A1(2), A1(3),'.','Color','k','MarkerSize',10)
% plot3(B1(1), B1(2), B1(3),'x','Color','r')
% plot3(C1(1), C1(2), C1(3),'x','Color','r')
plot3(linspace(A1(1),B1(1)), linspace(A1(2),B1(2)), linspace(A1(3),B1(3)), 'r', 'LineWidth', 1.5)
plot3(linspace(A1(1),C1(1)), linspace(A1(2),C1(2)), linspace(A1(3),C1(3)), 'r', 'LineWidth', 1.5)
plot3(linspace(C1(1),B1(1)), linspace(C1(2),B1(2)), linspace(C1(3),B1(3)), 'r', 'LineWidth', 1.5)


figure
hold on; grid off; axis off
plot3(A1(1), A1(2), A1(3),'x','Color','r')
plot3(B1(1), B1(2), B1(3),'x','Color','r')
plot3(C1(1), C1(2), C1(3),'x','Color','r')
plot3(linspace(A1(1),B1(1)), linspace(A1(2),B1(2)), linspace(A1(3),B1(3)), 'r')
plot3(linspace(A1(1),C1(1)), linspace(A1(2),C1(2)), linspace(A1(3),C1(3)), 'r')
plot3(linspace(C1(1),B1(1)), linspace(C1(2),B1(2)), linspace(C1(3),B1(3)), 'r')
plot3(viewCameraPosition(1), viewCameraPosition(2), viewCameraPosition(3),'.','MarkerSize', 20)
P_proj = 0.5*A1 + 0.25 *B1 + 0.25*C1;
P = P_proj - 0.1 * P_proj;
plot3(P(1), P(2), P(3),'.','Color','b','MarkerSize', 10)

plot3(linspace(viewCameraPosition(1),1.5*P(1)), linspace(viewCameraPosition(2),1.5*P(2)), linspace(viewCameraPosition(3),1.5*P(3)), 'k')

plot3(P_proj(1), P_proj(2), P_proj(3),'.','Color','k','MarkerSize', 10)

viewCameraPosition2 = [0.1, -0.2, 0];
plot3(viewCameraPosition2(1), viewCameraPosition2(2), viewCameraPosition2(3),'.','MarkerSize', 20)


% A = [-0.259, -0.405, 1.316];
A = stlData.Points(448,:);
% B = [-0.233, -0.366,1.367];
B = stlData.Points(450,:);
% C = [-0.296, -0.313, 1.367];
C = stlData.Points(428,:);
% D = [-0.329, -0.346, 1.316];
D = stlData.Points(426,:);
% E = [-0.274, -0.429, 1.262];
E = stlData.Points(446,:);
% F = [-0.189, -0.475, 1.262];
F = stlData.Points(453,:);
% G = [-0.178, -0.449, 1.316];
G = stlData.Points(454,:);

ans_1 = find(points(:,1)==A(1));
ans_2 = find(points(:,2)==A(2));
ans_3 = find(points(:,3)==A(3));
ans_4 = intersect(ans_1,ans_2);
id = intersect(ans_4,ans_3);

close all 
figure
trimesh(stlData,'FaceColor','w','EdgeColor','k')
% view([0 -30 -90])
hold on; grid off; axis off

plot3(linspace(A(1),B(1)), linspace(A(2),B(2)), linspace(A(3),B(3)), 'Color', [0.3010 0.7450 0.9330], 'LineWidth', 1.5)
plot3(linspace(A(1),C(1)), linspace(A(2),C(2)), linspace(A(3),C(3)), 'Color', [0.3010 0.7450 0.9330], 'LineWidth', 1.5)
plot3(linspace(C(1),B(1)), linspace(C(2),B(2)), linspace(C(3),B(3)), 'Color', [0.3010 0.7450 0.9330], 'LineWidth', 1.5)

plot3(linspace(A(1),D(1)), linspace(A(2),D(2)), linspace(A(3),D(3)), 'Color', [0.9290 0.6940 0.1250], 'LineWidth', 1.5)
plot3(linspace(D(1),C(1)), linspace(D(2),C(2)), linspace(D(3),C(3)), 'Color', [0.9290 0.6940 0.1250], 'LineWidth', 1.5)

plot3(linspace(A(1),E(1)), linspace(A(2),E(2)), linspace(A(3),E(3)), 'Color', [0.9290 0.6940 0.1250], 'LineWidth', 1.5)
plot3(linspace(D(1),E(1)), linspace(D(2),E(2)), linspace(D(3),E(3)), 'Color', [0.9290 0.6940 0.1250], 'LineWidth', 1.5)

plot3(linspace(A(1),F(1)), linspace(A(2),F(2)), linspace(A(3),F(3)), 'Color', [0.9290 0.6940 0.1250], 'LineWidth', 1.5)
plot3(linspace(F(1),E(1)), linspace(F(2),E(2)), linspace(F(3),E(3)), 'Color', [0.9290 0.6940 0.1250], 'LineWidth', 1.5)

plot3(linspace(A(1),G(1)), linspace(A(2),G(2)), linspace(A(3),G(3)), 'Color', [0.9290 0.6940 0.1250], 'LineWidth', 1.5)
plot3(linspace(F(1),G(1)), linspace(F(2),G(2)), linspace(F(3),G(3)), 'Color', [0.9290 0.6940 0.1250], 'LineWidth', 1.5)

plot3(linspace(B(1),G(1)), linspace(B(2),G(2)), linspace(B(3),G(3)), 'Color', [0.9290 0.6940 0.1250], 'LineWidth', 1.5)

plot3(A(1), A(2), A(3),'.','Color',[0, 0, 0],'MarkerSize',25)




