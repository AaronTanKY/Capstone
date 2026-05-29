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


%% Add zeroes front and back
A = viztree.StoredConfigurations;

% 1. Get the number of rows dynamically
num_rows = size(A, 1);

% 2a. Create a column of zeros for the front
zeros_col = zeros(num_rows, 1);

% 3. Append the zeros to the front and back to make a 10x3 matrix
dab = [zeros_col, A, zeros_col];

save('dab.mat','dab');

%% Modify and Pad Matrix
A = viztree.StoredConfigurations; % Assuming this is a [Rows x 3] matrix
num_rows = size(A, 1);

% 1. Extract the last 2 columns (Columns 2 and 3)
last_two = A(:, 2:3);

% 2. Repeat those columns 2 more times (creating 4 additional columns)
% We concatenate the original A with two copies of the last two columns
% Resulting size: 3 (original) + 2 + 2 = 7 columns
A_expanded = [A, last_two, last_two];

% 3. Pad the matrix with 1 column of zero each
zeros_col = zeros(num_rows, 1);

% Append them to the end (or front and back depending on your preference)
% Based on your request to "pad with 2 columns", here they are at the end:
six_seven = [zeros_col, A_expanded, zeros_col];

% Save the final [num_rows x 9] matrix
save('six_seven.mat', 'six_seven');


%% Run this to save csv

A = [tvec', q'];
writematrix(A, 'six_seven.csv');

%% Change a column of my CSV
% 1. Read the matrix from the CSV file
% Replace 'your_file.csv' with your actual filename
A = readmatrix('dab.csv'); 

% 2. Multiply the whole 4th column by -1
% This works exactly the same as your previous matrix manipulation
A(:, 6) = A(:, 6) * -1;

% 3. Write the modified matrix back to a CSV file
% You can save it as 'six_seven.csv' to keep your naming consistent
writematrix(A, 'dab.csv');

% Optional: Verify the change in the command window
disp('First few rows of the modified 4th column:');
disp(A(1:5, 6));