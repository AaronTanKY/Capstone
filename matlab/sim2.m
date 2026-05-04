%% 1. Create the Robot Tree
clc; clear; close all;

robot = rigidBodyTree('DataFormat', 'column');
base = robot.Base;

rotatingBase = rigidBody("rotating_base");
link1 = rigidBody("link1");
link2 = rigidBody("link2");
link3 = rigidBody("link3");
link4 = rigidBody("link4");
gripper = rigidBody("gripper");

collBase = collisionCylinder(0.016,0.01); % cylinder: radius,length
collBase.Pose = trvec2tform([0 -0.01/2 0]) * eul2tform([pi/2 0 0], 'XYZ');
coll1 = collisionCylinder(0.009,0.045);
coll1.Pose = trvec2tform([0 0.045/2 0]) * eul2tform([pi/2 0 0], 'XYZ');
coll2 = collisionCylinder(0.009,0.051); 
coll2.Pose = trvec2tform([0 0 -0.051/2-0.016]);
coll3 = collisionCylinder(0.009,0.119); 
coll3.Pose = trvec2tform([0 0 -0.119/2]);
coll4 = collisionCylinder(0.009,0.225); 
coll4.Pose = trvec2tform([0 0 -0.225/2]);
collGripper = collisionSphere(0.040); % sphere: radius
collGripper.Pose = trvec2tform([0 0 0]);

addCollision(rotatingBase,collBase)
addCollision(link1,coll1)
addCollision(link2,coll2)
addCollision(link3,coll3)
addCollision(link4,coll4)
addCollision(gripper,collGripper)

% ADDING VISUALS
addVisual(rotatingBase, 'Cylinder', [collBase.Radius,collBase.Length], collBase.Pose);
addVisual(link1, 'Cylinder', [coll1.Radius,coll1.Length], coll1.Pose);
addVisual(link2, 'Cylinder', [coll2.Radius,coll2.Length], coll2.Pose);
addVisual(link3, 'Cylinder', [coll3.Radius,coll3.Length], coll3.Pose);
addVisual(link4, 'Cylinder', [coll4.Radius,coll4.Length], coll4.Pose);
addVisual(gripper, 'Sphere', [collGripper.Radius], collGripper.Pose);

jntBase = rigidBodyJoint("base_joint","revolute");
jnt1 = rigidBodyJoint("jnt1","fixed");
jnt2 = rigidBodyJoint("jnt2","revolute");
jnt3 = rigidBodyJoint("jnt3","revolute");
jnt4 = rigidBodyJoint("jnt4","revolute");
jntGripper = rigidBodyJoint("grip", "fixed");

jntBase.JointAxis = [0 1 0]; % y-axis
jnt2.JointAxis = [1 0 0]; % x-axis
jnt3.JointAxis = [0 0 1]; % z-axis
jnt4.JointAxis = [0 1 0]; % z-axis

setFixedTransform(jntBase, eye(4));
setFixedTransform(jnt1, eye(4));
setFixedTransform(jnt2, trvec2tform([0 0.045 0]));
setFixedTransform(jnt3, trvec2tform([0 0 -0.084]));
setFixedTransform(jnt4, trvec2tform([0 0 -0.152]));
setFixedTransform(jntGripper, trvec2tform([0 0 -0.273]));

bodies = {base,rotatingBase,link1,link2,link3,link4,gripper};
joints = {[],jntBase,jnt1,jnt2,jnt3,jnt4,jntGripper};

figure("Name","Assemble Robot","Visible","on")
for i = 2:length(bodies) % Skip base. Iterate through adding bodies and joints.
            bodies{i}.Joint = joints{i};
            addBody(robot,bodies{i},bodies{i-1}.Name)
            show(robot,"Collisions","on","Frames","on");
            drawnow;
end

%% 1.5. Interactive Rigid Body Tree
viztree = interactiveRigidBodyTree(robot,"MarkerBodyName","link4", "ShowMarker",true);

%% 2. Visualize the Configs
% Play back the "waypoints" you saved
for i = 1:size(viztree.StoredConfigurations, 2)
    viztree.Configuration = viztree.StoredConfigurations(:, i);
    pause(0.5); % Wait half a second between poses
end

% If you want to save the poses:
% addConfiguration(viztree)                     % Run this as many times

%% 3a. Visualize unsaved movement
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

% Once satisfied, store it
% wavePose = viztree.StoredConfigurations;
% save('wavePose.mat','wavePose');

%% 3b. Visualize unsaved movement
load("wavePose.mat");
viztree.StoredConfigurations = wavePose;

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

%% 2. Generalized Inverse Kinematics Setup
% Define solver with constraints
gik = generalizedInverseKinematics('RigidBodyTree', robot, ...
    'ConstraintInputs', {'position', 'orientation', 'joint'});

posTgt = constraintPositionTarget('gripper');
posTgt.PositionTolerance = 0.002;

orienTgt = constraintOrientationTarget('gripper');
orienTgt.TargetOrientation = [1 0 0 0];

jointTgt = constraintJointBounds(robot);

%% 3. Trajectory Planning
numWaypoints = 40; 
theta = linspace(0, 2*pi, numWaypoints);
radius = 0.05;
center = [0, 0.1, -0.1]; 

q0 = homeConfiguration(robot); 
% FIX 1: Pre-allocate with enough columns for all joints [cite: 36, 40]
qWaypoints = repmat(q0', numWaypoints, 1); 

maxJointChange = deg2rad(5);
currentGuess = q0; % This is a 4x1 column vector

for k = 1:numWaypoints
    posTgt.TargetPosition = [center(1) + radius*cos(theta(k)), ...
                             center(2), ...
                             center(3) + radius*sin(theta(k))];
    
    % FIX 2: Bounds must be [N x 2] (Column 1: Min, Column 2: Max) [cite: 177]
    jointTgt.Bounds = [currentGuess - maxJointChange, currentGuess + maxJointChange];
    
    % Solve configuration [cite: 151]
    [qSol, solInfo] = gik(currentGuess, posTgt, orienTgt, jointTgt);
    
    % Store as a row [cite: 179]
    qWaypoints(k,:) = qSol';
    
    % Update guess for next iteration (Back to column for the solver) [cite: 151, 179]
    currentGuess = qSol;
end

%% 4. Animation
% Interpolate for smoothness [cite: 188, 194]
tSteps = linspace(0, 1, numWaypoints);
tInterp = linspace(0, 1, numWaypoints * 5);
qInterp = pchip(tSteps, qWaypoints', tInterp)';

figure;
for i = 1:size(qInterp, 1)
    % Pass each configuration as a column vector to 'show' [cite: 224]
    show(robot, qInterp(i,:)', 'PreservePlot', false, 'Collisions', 'on');
    axis equal; view(3); grid on;
    drawnow;
end