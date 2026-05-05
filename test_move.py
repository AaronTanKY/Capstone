from pybear import Manager
import pandas as pd
import time
import argparse

def move_motor(bear, bear_id, goal_pos):
    """
    Move motors of bear
    """
    # Move to goal position
    bear.set_goal_position((bear_id, goal_pos))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Configure BEAR device (override defaults with CLI args)")
    parser.add_argument('--bear-id', '-i', help='Bear ID', default=1)
    parser.add_argument('--port', '-p', help='Serial port (default from file)', default='COM3')
    parser.add_argument('--data', '-d', help='CSV file name', default='motor_commands.csv')
    parser.add_argument('--baudrate', '-b', help='Baudrate', default=8000000)
    args = parser.parse_args()

    active_port = args.port
    csv_file = args.data
    baudrate = args.baudrate
    bear_id = args.bear_id
    
    # Load the data
    df = pd.read_csv(csv_file, header=None)
    # Column 0 is Time, Columns 1+ are Joints
    t_points = df.iloc[:, 0].values
    q_points = df.iloc[:, 1:].values    # TODO! SET THIS TO 1 instead of 1: to test 1 motor

    # Initialize bear
    bear = Manager.BEAR(port=active_port, baudrate=baudrate)
    # Get home position
    home = bear.get_present_position(bear_id)[0][0][0]
    # Set goal position before enabling BEAR
    bear.set_goal_position((bear_id, home))
    # Enable BEAR
    bear.set_torque_enable((bear_id, 1))

    for i in range(len(t_points)):
        # 1. Send q_points[i] to your motor SDK here
        move_motor(q_points[i])
        
        # 2. Calculate sleep time until the next waypoint
        if i < len(t_points) - 1:
            dt = t_points[i+1] - t_points[i]
            time.sleep(dt)
        print('BEAR arrived target angle!')
    
    time.sleep(2)

    # Turn off BEAR
    input('Press Enter to turn off BEAR.')
    # Disable BEAR
    bear.set_torque_enable((bear_id, 0))
    print("Thanks for using BEAR!")