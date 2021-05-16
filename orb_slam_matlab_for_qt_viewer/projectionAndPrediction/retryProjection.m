function [mapPointSet, projectedPointSet] = retryProjection(projectedPointSet, mapPointSet, stlData, pointIndices, vSetKeyFrames, nodePositions)
    viewId = vSetKeyFrames.NumViews;
    viewCameraPosition = vSetKeyFrames.Views.AbsolutePose(end).Translation;
    isNotProjected = find(projectedPointSet.IsProjected==0);
    pointsOfInterest = intersect(pointIndices, isNotProjected);
    save 'wtf.mat' isNotProjected projectedPointSet pointIndices mapPointSet
    positionsOld = mapPointSet.WorldPoints(pointsOfInterest,:);
    positionsNew = zeros(length(pointsOfInterest),3);
    updateIndices = []; % contains map point indices that have been updated
    updateIndices2 = []; % contains indices of positionsNew that have been updated
    for i = 1:length(pointsOfInterest)
        P = positionsOld(i,:);
        j = pointsOfInterest(i);
        % find closest points
        P_distances = vecnorm(P-nodePositions,2,2);
        k = find(P_distances == min(P_distances));        
        k_triangles = vertexAttachments(stlData,k);
        k_triangles = k_triangles{1}(:)';
        % get indices of triangle corners
        vertexIDs = stlData(k_triangles,:);
        % use indices to get triangle corner coordinates
        A = nodePositions(vertexIDs(:,1),:);
        B = nodePositions(vertexIDs(:,2),:);
        C = nodePositions(vertexIDs(:,3),:);
        phi = pi/2;
%         [alpha_opt, beta_opt, gamma_opt, P_proj_opt, phi_opt] = cameraViewProjection(A,B,C,P,viewCameraPosition);
        [alpha_opt, beta_opt, gamma_opt, P_proj_opt, phi_opt, k_triangle] = test_CameraViewProjection(A,B,C,P,viewCameraPosition);
        if abs(phi_opt-pi) < abs(phi) % phi_opt is always \in [pi/2, pi]
            positionsNew(i,:) = P_proj_opt;
            projectedPointSet.IsProjected(j) = 1;
            projectedPointSet.BarycentricCoordinates(j,:) = [alpha_opt beta_opt gamma_opt];
            projectedPointSet.TrianglePointIdx(j,:) = vertexIDs(k_triangle,:);
            projectedPointSet.ViewId(j) = viewId;
            projectedPointSet.ProjectionAngle(j) = phi_opt;
            updateIndices = [updateIndices; j];
            updateIndices2 = [updateIndices2; i];
        end  
    end
    disp(['Projected ', num2str(length(updateIndices)), ' out of ',...
        num2str(length(pointsOfInterest)), '/', num2str(length(isNotProjected)),' previously unprojected points']);
    if ~isempty(updateIndices2) 
        positionsNew = positionsNew(updateIndices2,:);
        mapPointSet = updateWorldPoints(mapPointSet, updateIndices, positionsNew);
    end
end