path_1 = '/isys_1.png';
path_2 = '/isys_2.png';

isys_1 = rgb2gray(imread(path_1));
isys_2 = rgb2gray(imread(path_2));

points_1 = detectORBFeatures(isys_1);
points_2 = detectORBFeatures(isys_2);
points_1 = selectUniform(points_1, 1000, size(isys_1, 1:2));
points_2 = selectUniform(points_2, 1000, size(isys_2, 1:2));

[features_1, validPoints_1] = extractFeatures(isys_1, points_1);
[features_2, validPoints_2] = extractFeatures(isys_2, points_2);

indexPairs  = matchFeatures(features_1, features_2,...
    'Unique', true, 'MaxRatio', 0.7, 'MatchThreshold', 15);
matchedPoints_1 = validPoints_1(indexPairs(:,1),:);
matchedPoints_2 = validPoints_2(indexPairs(:,2),:);

figure; 
showMatchedFeatures(isys_1,isys_2,matchedPoints_1,matchedPoints_2, 'Montage');