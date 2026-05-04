%% Playback saved file
clc; clear; close all;

numPoses = size(viztree.StoredConfigurations, 2);

% Time step between each waypoint
timeStep = 2;

% 3. Create evenly spaced time points starting from 0
% If numPoses is 6, this creates [0 2 4 6 8 10]
tpts = 0 : timeStep : (numPoses-1) * timeStep;

% 4. Create the fine-grained time vector for the trajectory
% tpts(end) ensures tvec always stops exactly at your last waypoint
tvec = 0 : 0.1 : tpts(end);

[q,qd,qdd,pp] = cubicpolytraj(viztree.StoredConfigurations,tpts,tvec); 

r = rateControl(10);
viztree.ShowMarker = false;  % Hide the marker 

showFigure(viztree)

for i = 1:size(q',1)
    viztree.Configuration = q(:,i);
    waitfor(r);
end     
