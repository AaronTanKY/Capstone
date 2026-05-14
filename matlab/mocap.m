%% ASF Base Pose Plotter for Arm Segments
figure('Name', 'VICON Skeleton - Arm Base Pose');
hold on; grid on; axis equal; view(3);

% 1. Global Scaling Factor from :units
scale = 0.45;

% 2. Define Joint Points (Thorax as origin [0,0,0])
thorax = [0, 0, 0];

% --- LEFT ARM CALCULATION ---
% lclavicle (id 17)
l_clav_dir = [0.967963, 0.201165, -0.150269];
l_clav_len = 3.63976 * scale;
l_shoulder = thorax + (l_clav_dir * l_clav_len);

% lhumerus (id 18)
l_hum_dir = [1, -4.48954e-011, -2.92837e-028];
l_hum_len = 5.32462 * scale;
l_elbow = l_shoulder + (l_hum_dir * l_hum_len);

% lradius (id 19)
l_rad_dir = [1, -4.48958e-011, -6.39511e-027];
l_rad_len = 3.48402 * scale;
l_wrist = l_elbow + (l_rad_dir * l_rad_len);

% --- RIGHT ARM CALCULATION ---
% rclavicle (id 24)
r_clav_dir = [-0.964103, 0.264019, -0.0282629];
r_clav_len = 3.54491 * scale;
r_shoulder = thorax + (r_clav_dir * r_clav_len);

% rhumerus (id 25)
r_hum_dir = [-1, -4.48964e-011, -2.45032e-027];
r_hum_len = 5.33589 * scale;
r_elbow = r_shoulder + (r_hum_dir * r_hum_len);

% 3. Plotting the skeleton
% Left Arm (Blue)
plot3([thorax(1) l_shoulder(1) l_elbow(1) l_wrist(1)], ...
      [thorax(2) l_shoulder(2) l_elbow(2) l_wrist(2)], ...
      [thorax(3) l_shoulder(3) l_elbow(3) l_wrist(3)], '-ob', 'LineWidth', 2);

% Right Arm (Red)
plot3([thorax(1) r_shoulder(1) r_elbow(1)], ...
      [thorax(2) r_shoulder(2) r_elbow(2)], ...
      [thorax(3) r_shoulder(3) r_elbow(3)], '-or', 'LineWidth', 2);

title('VICON ASF Base Pose: Arms & Thorax');
xlabel('X'); ylabel('Y'); zlabel('Z');