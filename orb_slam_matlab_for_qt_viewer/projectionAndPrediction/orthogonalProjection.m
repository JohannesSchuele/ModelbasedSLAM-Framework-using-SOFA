function [alpha, beta, gamma] = orthogonalProjection(A,B,C,P)
    % Given a triangle consisting of three points in space A, B, and C
    % and an arbitrary point P compute the barycentric coordinates of the 
    % orthogonal projection of P onto the plane defined by A, B, and C. 
    
    % define some vectors
    v0 = B-A;
    v1 = C-A;
    v2 = P-A;
    % compute the unit normal of the triangle
    n = cross(v0, v1);
    % directly compute barycentric coordinates
    n_norm = dot(n,n); %vecnorm(n)^2,n'*n,sum(n.^2)
    gamma = (dot(cross(v0, v2),n))/n_norm;
    beta = (dot(cross(v2, v1),n))/n_norm;
    alpha = 1-gamma-beta;
end

