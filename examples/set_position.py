#!usr/bin/env python
__author__    = "Westwood Robotics Corporation"
__email__     = "info@westwoodrobotics.io"
__copyright__ = "Copyright 2025 Westwood Robotics Corporation"
__date__      = "July 29, 2025"
__project__   = "PyBEAR"
__version__   = "0.1.3"
__status__    = "Production"

'''
Move BEAR from the current angle to a specified angle
'''

import time
import sys
from pathlib import Path

try:
    from pybear import Manager
except ModuleNotFoundError:
    project_root = Path(__file__).resolve().parents[1]
    if str(project_root) not in sys.path:
        sys.path.insert(0, str(project_root))
    from pybear import Manager


error = False
bear = Manager.BEAR(port="COM3", baudrate=8000000)  # change this to your device port

m_id = 3 # BEAR ID (default is 1)

BEAR_connected = bear.ping(m_id)[0][1] is not None
if not BEAR_connected:
    # BEAR is offline
    print("BEAR is offline. Check power and connection.")
    error = True
    exit()

if not error:
    # BEAR is online
    # This example intentionally avoids changing configured gains/limits.
    print("Welcome aboard, Captain!")

    # Start demo
    input('Press Enter to start demo. ')

    # Get home position
    home = bear.get_present_position(m_id)[0][0][0]
    print(home)

    # Set goal position before enabling torque
    bear.set_goal_position((m_id, home))

    # Enable BEAR
    bear.set_torque_enable((m_id, 1))

    # Set goal velocity (this allows the motor to actually move)
    bear.set_goal_velocity((m_id, 2))  # Adjust this value for desired speed

    # Move to the user-selected target angle.
    print('You can move BEAR now using your existing configuration.')
    time.sleep(2)

    # Get command position
    angle = float(input('Input the angle in radians you want to move BEAR to (e.g., -0.2): '))

    # Let's move to the target angle smoothly
    num = 100                  # split it into 100 pieces
    delta_angle = angle / num  # angle for each time
    for i in range(num):
        goal_pos = home + delta_angle * (i + 1)
        print(f"Setting goal position to: {goal_pos:.4f}")
        bear.set_goal_position((m_id, goal_pos))
        time.sleep(0.01)
        if i % 20 == 0:  # Check position every 20 iterations
            current_pos = bear.get_present_position(m_id)[0][0][0]
            print(f"Current position: {current_pos:.4f}")

    print('BEAR arrived target angle!')
    time.sleep(2)

    # Turn off BEAR
    input('Press Enter to turn off BEAR.')

    # Disable BEAR
    bear.set_torque_enable((m_id, 0))
    print("Thanks for using BEAR!")