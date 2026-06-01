%% 1. Create the Robot Tree
clc; clear; close all;

robot = rigidBodyTree('DataFormat', 'column');
base = robot.Base;

% Neck
rotatingBaseNeck = rigidBody("rotating_base_neck");
link1 = rigidBody("link1");
link2 = rigidBody("link2");
head = rigidBody("head");
% Left Arm
rotatingBaseLeft = rigidBody("rotating_base_left");
link3 = rigidBody("link3");
link4 = rigidBody("link4");
link5 = rigidBody("link5");
link6 = rigidBody("link6");
gripperLeft = rigidBody("gripperLeft");
% Right Arm
rotatingBaseRight = rigidBody("rotating_base_right");
link7 = rigidBody("link7");
link8 = rigidBody("link8");
link9 = rigidBody("link9");
link10 = rigidBody("link10");
gripperRight = rigidBody("gripperRight");

% Neck
collBaseNeck = collisionCylinder(0.016,0.01); % cylinder: radius,length
collBaseNeck.Pose = trvec2tform([0 0 -0.01/2]);
coll1 = collisionCylinder(0.009,0.025);
coll1.Pose = trvec2tform([0 0 0.025/2]);
coll2 = collisionCylinder(0.009,0.12); 
coll2.Pose = trvec2tform([0 0 0.12/2]);
collHead = collisionSphere(0.09); 
collHead.Pose = trvec2tform([0.03 0 0]);
% Left Arm
collBaseLeft = collisionCylinder(0.016,0.01); % cylinder: radius,length
collBaseLeft.Pose = trvec2tform([0 -0.01/2 0]) * eul2tform([pi/2 0 0], 'XYZ');
coll3 = collisionCylinder(0.009,0.045);
coll3.Pose = trvec2tform([0 0.045/2 0]) * eul2tform([pi/2 0 0], 'XYZ');
coll4 = collisionCylinder(0.009,0.051); 
coll4.Pose = trvec2tform([0 0 -0.051/2-0.016]);
coll5 = collisionCylinder(0.009,0.119); 
coll5.Pose = trvec2tform([0 0 -0.119/2]);
coll6 = collisionCylinder(0.009,0.225); 
coll6.Pose = trvec2tform([0 0 -0.225/2]);
collGripperLeft = collisionSphere(0.040); % sphere: radius
collGripperLeft.Pose = trvec2tform([0 0 0]);
% Right Arm
collBaseRight = collisionCylinder(0.016,0.01); % cylinder: radius,length
collBaseRight.Pose = trvec2tform([0 0.01/2 0]) * eul2tform([pi/2 0 0], 'XYZ');
coll7 = collisionCylinder(0.009,0.045);
coll7.Pose = trvec2tform([0 -0.045/2 0]) * eul2tform([pi/2 0 0], 'XYZ');
coll8 = collisionCylinder(0.009,0.051); 
coll8.Pose = trvec2tform([0 0 -0.051/2-0.016]);
coll9 = collisionCylinder(0.009,0.119); 
coll9.Pose = trvec2tform([0 0 -0.119/2]);
coll10 = collisionCylinder(0.009,0.225); 
coll10.Pose = trvec2tform([0 0 -0.225/2]);
collGripperRight = collisionSphere(0.040); % sphere: radius
collGripperRight.Pose = trvec2tform([0 0 0]);

% Neck
addCollision(rotatingBaseNeck,collBaseNeck)
addCollision(link1,coll1)
addCollision(link2,coll2)
addCollision(head,collHead)
% Left Arm
addCollision(rotatingBaseLeft,collBaseLeft)
addCollision(link3,coll3)
addCollision(link4,coll4)
addCollision(link5,coll5)
addCollision(link6,coll6)
addCollision(gripperLeft,collGripperLeft)
% Right Arm
addCollision(rotatingBaseRight,collBaseRight)
addCollision(link7,coll7)
addCollision(link8,coll8)
addCollision(link9,coll9)
addCollision(link10,coll10)
addCollision(gripperRight,collGripperRight)

% ADDING VISUALS (LEFT ARM)
addVisual(rotatingBaseNeck, 'Cylinder', [collBaseNeck.Radius,collBaseNeck.Length], collBaseNeck.Pose);
addVisual(link1, 'Cylinder', [coll1.Radius,coll1.Length], coll1.Pose);
addVisual(link2, 'Cylinder', [coll2.Radius,coll2.Length], coll2.Pose);
addVisual(head, 'Sphere', [collHead.Radius], collHead.Pose);
% ADDING VISUALS (LEFT ARM)
addVisual(rotatingBaseLeft, 'Cylinder', [collBaseLeft.Radius,collBaseLeft.Length], collBaseLeft.Pose);
addVisual(link3, 'Cylinder', [coll3.Radius,coll3.Length], coll3.Pose);
addVisual(link4, 'Cylinder', [coll4.Radius,coll4.Length], coll4.Pose);
addVisual(link5, 'Cylinder', [coll5.Radius,coll5.Length], coll5.Pose);
addVisual(link6, 'Cylinder', [coll6.Radius,coll6.Length], coll6.Pose);
addVisual(gripperLeft, 'Sphere', [collGripperLeft.Radius], collGripperLeft.Pose);
% ADDING VISUALS (RIGHT ARM)
addVisual(rotatingBaseRight, 'Cylinder', [collBaseRight.Radius,collBaseRight.Length], collBaseRight.Pose);
addVisual(link7, 'Cylinder', [coll7.Radius,coll7.Length], coll7.Pose);
addVisual(link8, 'Cylinder', [coll8.Radius,coll8.Length], coll8.Pose);
addVisual(link9, 'Cylinder', [coll9.Radius,coll9.Length], coll9.Pose);
addVisual(link10, 'Cylinder', [coll10.Radius,coll10.Length], coll10.Pose);
addVisual(gripperRight, 'Sphere', [collGripperRight.Radius], collGripperRight.Pose);

% Neck
jntBaseNeck = rigidBodyJoint("base_joint_neck","revolute");
jnt1 = rigidBodyJoint("jnt1","fixed");
jnt2 = rigidBodyJoint("jnt2","revolute");
jntHead = rigidBodyJoint("head", "fixed");
% Left Arm
jntBaseLeft = rigidBodyJoint("base_joint_left","revolute");
jnt3 = rigidBodyJoint("jnt3","fixed");
jnt4 = rigidBodyJoint("jnt4","revolute");
jnt5 = rigidBodyJoint("jnt5","revolute");
jnt6 = rigidBodyJoint("jnt6","revolute");
jntGripperLeft = rigidBodyJoint("gripLeft", "fixed");
% Right Arm
jntBaseRight = rigidBodyJoint("base_joint_right","revolute");
jnt7 = rigidBodyJoint("jnt7","fixed");
jnt8 = rigidBodyJoint("jnt8","revolute");
jnt9 = rigidBodyJoint("jnt9","revolute");
jnt10 = rigidBodyJoint("jnt10","revolute");
jntGripperRight = rigidBodyJoint("gripRight", "fixed");

% Neck
jntBaseNeck.JointAxis = [0 0 1]; % z-axis
jnt2.JointAxis = [0 1 0]; % y-axis
% Left Arm
jntBaseLeft.JointAxis = [0 1 0]; % y-axis
jnt4.JointAxis = [1 0 0]; % x-axis
jnt5.JointAxis = [0 0 -1]; % z-axis
jnt6.JointAxis = [0 1 0]; % y-axis
% Right Arm
jntBaseRight.JointAxis = [0 -1 0]; % y-axis
jnt8.JointAxis = [1 0 0]; % x-axis
jnt9.JointAxis = [0 0 -1]; % z-axis
jnt10.JointAxis = [0 -1 0]; % y-axis

% Neck
setFixedTransform(jntBaseNeck, trvec2tform([0 0 0.1]));
setFixedTransform(jnt1, trvec2tform([0 0 0]));
setFixedTransform(jnt2, trvec2tform([0 0 0.035]));
setFixedTransform(jntHead, trvec2tform([0 0 0.13]));
% Left Arm
setFixedTransform(jntBaseLeft, trvec2tform([0 0.21 0]));
setFixedTransform(jnt3, trvec2tform([0 0 0]));
setFixedTransform(jnt4, trvec2tform([0 0.045 0]));
setFixedTransform(jnt5, trvec2tform([0 0 -0.084]));
setFixedTransform(jnt6, trvec2tform([0 0 -0.152]));
setFixedTransform(jntGripperLeft, trvec2tform([0 0 -0.273]));
% Right Arm
setFixedTransform(jntBaseRight, trvec2tform([0 -0.21 0]));
setFixedTransform(jnt7, trvec2tform([0 0 0]));
setFixedTransform(jnt8, trvec2tform([0 -0.045 0]));
setFixedTransform(jnt9, trvec2tform([0 0 -0.084]));
setFixedTransform(jnt10, trvec2tform([0 0 -0.152]));
setFixedTransform(jntGripperRight, trvec2tform([0 0 -0.273]));

% Joining neck
bodiesNeck = {base,rotatingBaseNeck,link1,link2,head};
jointsNeck = {[],jntBaseNeck,jnt1,jnt2,jntHead};
for i = 2:length(bodiesNeck) % Skip base. Iterate through adding bodiesNeck and jointsNeck.
            bodiesNeck{i}.Joint = jointsNeck{i};
            addBody(robot,bodiesNeck{i},bodiesNeck{i-1}.Name)
end
% Joining left arm
bodiesLeft = {base,rotatingBaseLeft,link3,link4,link5,link6,gripperLeft};
jointsLeft = {[],jntBaseLeft,jnt3,jnt4,jnt5,jnt6,jntGripperLeft};
for i = 2:length(bodiesLeft) % Skip base. Iterate through adding bodiesLeft and jointsLeft.
            bodiesLeft{i}.Joint = jointsLeft{i};
            addBody(robot,bodiesLeft{i},bodiesLeft{i-1}.Name)
end
% Joining right arm
bodiesRight = {base,rotatingBaseRight,link7,link8,link9,link10,gripperRight};
jointsRight = {[],jntBaseRight,jnt7,jnt8,jnt9,jnt10,jntGripperRight};
figure("Name","Assemble Robot","Visible","on")
for i = 2:length(bodiesRight) % Skip base. Iterate through adding bodiesRight and jointsRight.
            bodiesRight{i}.Joint = jointsRight{i};
            addBody(robot,bodiesRight{i},bodiesRight{i-1}.Name)
            show(robot,"Collisions","on","Frames","on");
            drawnow;
end
%% 1.5. Interactive Rigid Body Tree
viztree = interactiveRigidBodyTree(robot,"MarkerBodyName","link6", ...
    "ShowMarker",true, "Frames","on");

%% 2. Visualize the Configs
% Play back the "waypoints" you saved
for i = 1:size(viztree.StoredConfigurations, 2)
    viztree.Configuration = viztree.StoredConfigurations(:, i);
    pause(0.5); % Wait half a second between poses
end

% If you want to save the poses:
% addConfiguration(viztree)                     % Run this as many times

%% 3a. Visualize unsaved movement
[numDOF, numPoses] = size(viztree.StoredConfigurations);
movement = viztree.StoredConfigurations;

% Time step between each waypoint
timeStep = 2;

% 3. Create evenly spaced time points starting from 0
% If numPoses is 6, this creates [0 2 4 6 8 10]
tpts = 0 : timeStep : (numPoses-1) * timeStep;

% 4. Create the fine-grained time vector for the trajectory
% tpts(end) ensures tvec always stops exactly at your last waypoint
tvec = 0 : 0.1 : tpts(end);

% 2. Calculate "Average" velocities for intermediate points
% This is a simple heuristic: (NextPoint - PreviousPoint) / Time
waypointVelocities = zeros(numDOF, numPoses);
for j = 2:numPoses-1
    waypointVelocities(:,j) = (movement(:,j+1) - movement(:,j-1)) / (tpts(j+1) - tpts(j-1));
end

[q,qd,qdd,pp] = cubicpolytraj(viztree.StoredConfigurations,tpts,tvec, ...
    'VelocityBoundaryCondition', waypointVelocities); 

r = rateControl(10);
viztree.ShowMarker = false;  % Hide the marker 

showFigure(viztree)

pause(5);

for i = 1:size(q',1)
    viztree.Configuration = q(:,i);
    waitfor(r);
end     

% Once satisfied, store it
% wavePose = viztree.StoredConfigurations;
% save('wavePose.mat','wavePose');


%% 3b. Visualize saved movement
% --- USER DEFINED VARIABLE ---
myMotionName = 'wavePose'; % Replace 'idle' with your desired string
% -----------------------------

% Use the functional form load('filename.mat') to handle variables
data = load([myMotionName, '.mat']);

% Use dynamic field naming data.(variable) to access the struct field
viztree.StoredConfigurations = data.(myMotionName);

% Replace 'idle' with the dynamic data in the rest of the script
[numDOF, numPoses] = size(viztree.StoredConfigurations);

% Time step between each waypoint
timeStep = 2;

% 3. Create evenly spaced time points starting from 0
tpts = 0 : timeStep : (numPoses-1) * timeStep;

% 4. Create the fine-grained time vector for the trajectory
tvec = 0 : 0.001 : tpts(end);

% 2. Calculate "Average" velocities for intermediate points
waypointVelocities = zeros(numDOF, numPoses);
for j = 2:numPoses-1
    % Use the stored configurations directly to avoid repeated dynamic naming
    waypointVelocities(:,j) = (viztree.StoredConfigurations(:,j+1) - ...
                               viztree.StoredConfigurations(:,j-1)) / (tpts(j+1) - tpts(j-1));
end

[q,qd,qdd,pp] = cubicpolytraj(viztree.StoredConfigurations, tpts, tvec, ...
    'VelocityBoundaryCondition', waypointVelocities); 

r = rateControl(1000);
viztree.ShowMarker = false;  % Hide the marker 
showFigure(viztree)

for i = 1:size(q',1)
    viztree.Configuration = q(:,i);
    waitfor(r);
end


% A = [tvec', q']
% writematrix(A, 'wave_trajectory.csv')