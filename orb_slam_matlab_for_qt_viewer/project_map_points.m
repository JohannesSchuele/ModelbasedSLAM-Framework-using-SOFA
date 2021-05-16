%% Initialize projection
% column 1-3 unprojected cartesian coordinates
% column 4-6 projected cartesian coordinates
% column 7 isProjected
% column 8 index of triangulation.ConnectivityList (corresponding triangle)
% column 9-11 barycentric coordinates
% column 12-14 indices of stl points making up the triangle
% need barycentric coordinates and indices of stl points
tic
points = mapPointSet.WorldPoints;
% TODO do all this in a struct instead of matrix
pointsProjection = zeros(length(points),14);
disp(length(points))
for i = 1:length(points)
    P = points(i,:)';
    % TODO save point coordinates or just index??
    pointsProjection(i,1:3) = P'; 
    % remember which triangles you tried to avoid doubles
    k_tried = [];
    % find closest points
    P_distances = vecnorm(P-stlData.Points');
    k = find(P_distances == min(P_distances));
%     k_2 = dsearchn(stl_data2.Points,P');
    k_triangles = vertexAttachments(stlData,k);
    k_toTry = k_triangles{1}(:)';
    % TODO: find k_triangle -> k gibt nur Punkte an, jetzt muss
    % jedes Dreieck, dass diesen Punkt enthält geprüft werden,
    % doppelte vermeiden
    j = 1;
    while pointsProjection(i,7) ~= 1 && j <= length(k_toTry)
%     for k_triangle = k_triangles{1}(:)'
        k_triangle = k_toTry(j);
        % get indices of triangle corners
        vertexIDs = stlData(k_triangle,:);
        % use indices to get triangle corner coordinates
        A = stlData.Points(vertexIDs(1),:)';
        B = stlData.Points(vertexIDs(2),:)';
        C = stlData.Points(vertexIDs(3),:)';
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
            pointsProjection(i,7) = 1; %isProjected
            pointsProjection(i,8) = k; %index of closest point
            pointsProjection(i,9:11) = [alpha beta gamma]; %barycentric coordinates
            pointsProjection(i,12:14) = vertexIDs; 
            mapPointSet = updateWorldPoints(mapPointSet, i, pointsProjection(i,4:6));
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

% %% Plot projection results
% figure
% trimesh(stl_data2,'FaceColor','k','EdgeColor','w')
% hold on
% i_unprojected = find(pointsProjection(:,7)==0);
% pointsProjection(i_unprojected,4:6) = nan;
% plot3(pointsProjection(i_unprojected,1),...
%     pointsProjection(i_unprojected,2),...
%     pointsProjection(i_unprojected,3),'.','Color','r');
% % plot3(pointsProjection(:,1),...
% %     pointsProjection(:,2),...
% %     pointsProjection(:,3),'.','Color','m');
% plot3(pointsProjection(:,4),...
%     pointsProjection(:,5),...
%     pointsProjection(:,6),'.','Color','g');
% legend('STL File','Unprojected Points','Projected Points')
% 
% disp(length(i_unprojected));
%% useful functions
% updateCorrespondences
% removeCorrespondences
% addWorldPoints, mapPointSet = updateWorldPoints(mapPointSet, indices, positionsNew);
% updateWorldPoints
% removeWorldPoints
% vSetKeyFrames = updateView(vSetKeyFrames, refinedAbsPoses);
% vSetKeyFrames = updateConnection(vSetKeyFrames, preViewId, currViewId, relPose);
% directionAndDepth = update(directionAndDepth, mapPointSet, vSetKeyFrames.Views, newPointIdx, true);
% directionAndDepth = update(directionAndDepth, mapPointSet, vSetKeyFrames.Views, [mapPointsIdx; newPointIdx], true);
% mapPlot       = helperVisualizeMotionAndStructure(vSetKeyFrames, mapPointSet);
% updatePlot(mapPlot, vSetKeyFrames, mapPointSet);

% % Add new map points and update connections 
% if any(inlier)
%     xyzPoints   = xyzPoints(inlier,:);
%     indexPairs  = indexPairs(inlier, :);
% 
%     mIndices1   = uIndices1(indexPairs(:, 1));
%     mIndices2   = uIndices2(indexPairs(:, 2));
% 
%     [mapPoints, indices] = addWorldPoints(mapPoints, xyzPoints);
%     recentPointIdx       = [recentPointIdx; indices]; %#ok<AGROW>
% 
%     % Add new observations
%     mapPoints  = addCorrespondences(mapPoints, KcIDs(i),indices, mIndices1);
%     mapPoints  = addCorrespondences(mapPoints, currKeyFrameId, indices, mIndices2);
% 
%     % Update connections with new feature matches
%     [~,ia]     = intersect(vSetKeyFrames.Connections{:,1:2}, ...
%         [KcIDs(i), currKeyFrameId], 'row', 'stable');
%     oldMatches = vSetKeyFrames.Connections.Matches{ia};
%     newMatches = [oldMatches; mIndices1, mIndices2];
%     vSetKeyFrames  = updateConnection(vSetKeyFrames, KcIDs(i), currKeyFrameId, ...
%         'Matches', newMatches);
% end
