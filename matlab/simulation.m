clc; clear; close all;

%% 1. Create the Robot Tree
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
coll3 = collisionCylinder(0.009,0.119-0.01); 
coll3.Pose = trvec2tform([0 0 -0.119/2-0.01]);
% collGripper = collisionSphere(0.025); % sphere: radius
% collGripper.Pose = trvec2tform([0 -0.015 0.025/2]);

addCollision(rotatingBase,collBase)
addCollision(link1,coll1)
addCollision(link2,coll2)
addCollision(link3,coll3)
% addCollision(link4,coll4)
% addCollision(gripper,collGripper)

jntBase = rigidBodyJoint("base_joint","revolute");
jnt1 = rigidBodyJoint("jnt1","fixed");
jnt2 = rigidBodyJoint("jnt2","revolute");
jnt3 = rigidBodyJoint("jnt3","revolute");

jntBase.JointAxis = [0 1 0]; % y-axis
jnt2.JointAxis = [1 0 0]; % x-axis
jnt3.JointAxis = [0 0 1]; % z-axis

setFixedTransform(jntBase, eye(4));
setFixedTransform(jnt1, eye(4));
setFixedTransform(jnt2, trvec2tform([0 0.045 0]));
setFixedTransform(jnt3, trvec2tform([0 0 -0.067]));

bodies = {base,rotatingBase,link1,link2,link3};
joints = {[],jntBase,jnt1,jnt2,jnt3};

figure("Name","Assemble Robot","Visible","on")
for i = 2:length(bodies) % Skip base. Iterate through adding bodies and joints.
            bodies{i}.Joint = joints{i};
            addBody(robot,bodies{i},bodies{i-1}.Name)
            show(robot,"Collisions","on","Frames","off");
            drawnow;
end