% 1. Load the file content into a structure
filename = 'wavePose.mat';
data = load(filename);
varNames = fieldnames(data);

% 2. Iterate through each variable
for i = 1:numeln(varNames)
    currentVar = data.(varNames{i});
    
    % Check if the variable is numeric (to avoid errors on strings/cells)
    if isnumeric(currentVar)
        [rows, cols] = size(currentVar);
        
        % Create 4 rows of zeros with the same number of columns
        newRows = zeros(4, cols);
        
        % Append the zeros to the bottom
        data.(varNames{i}) = [currentVar; newRows];
    end
end

% 3. Save the modified variables back to the file
% Use '-struct' to save the fields of the structure as individual variables
save(filename, 'wavePose');