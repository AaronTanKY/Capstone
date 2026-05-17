%%
load("head_idle3.mat");
load("head_idle2.mat");

num_rows = size(head_idle3, 1);
zeros_col = zeros(num_rows, 1);

head_idle4 = [head_idle3(:,1:2), head_idle2(:,3), head_idle3(:,3), ...
    head_idle2(:,4), head_idle3(:,4), head_idle2(:,5), ...
    head_idle3(:,5), head_idle2(:,6), head_idle3(:,6), zeros_col];

save('head_idle4.mat','head_idle4');

%%
% Your original column vector (10x1)
A = [0; 0; 0.0003; 0.1800; -0.3654; -0.2845; -0.0003; -0.1800; 0.3654; 0.2845;];

% 1. Get the number of rows dynamically
num_rows = size(A, 1);

% 2a. Create a column of zeros for the front
zeros_col = zeros(num_rows, 1);

% 2b. Create a column of other end
B = [0; 0; 0.0003; -0.0563; 0.3069; -0.2845; -0.0003; 0.0563; -0.3069; 0.2845;];

% 3. Append the zeros to the front and back to make a 10x3 matrix
padded_matrix = [A, B];

% 4. Duplicate the padded matrix 3 times horizontally
result = repmat(padded_matrix, 1, 3);
result = [zeros_col, result];

% 5. Save!
idle = result;
save('idle.mat','idle');