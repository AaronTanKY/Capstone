from pybear import Manager
import pandas as pd
import time
import argparse

def move_motors(bear, m_ids, goal_pos):
    """
    Move multiple BEAR motors simultaneously using bulk_write
    """
    # Bulk write requires a list of lists for data: [[pos1], [pos2], ... [posN]]
    # Each inner list contains the values for the registers specified (here, just one)
    bulk_data = [[pos] for pos in goal_pos]
    
    # Syntax: bear.bulk_write([IDs], [Registers], [[Data_for_ID1], [Data_for_ID2]...])
    bear.bulk_write(m_ids, ['goal_position'], bulk_data)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="BEAR Multi-Motor Control")
    parser.add_argument('--port', '-p', help='Serial port (default from file)', default='COM3')
    parser.add_argument('--data', '-d', help='CSV file name', default='yes.csv')
    parser.add_argument('--baudrate', '-b', help='Baudrate', type=int, default=8000000)
    args = parser.parse_args()
    
    m_ids = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

    # Load the data
    df = pd.read_csv(args.data, header=None)
    # Column 0 is Time, Columns 1+ are Joints
    t_points = df.iloc[:, 0].values
    q_points = df.iloc[:, 1:11].values    # TODO! SET THIS TO 1 instead of 1: to test 1 motor

    # Initialize bear
    bear = Manager.BEAR(port=args.port, baudrate=args.baudrate)

    # Check connection
    results = bear.ping(*m_ids) # The '*' unpacks the list into arguments
    offline_motors = [m_ids[i] for i, res in enumerate(results) if res is None]
    if not offline_motors:
        print("System Clear.")
    else:
        print(f"Error: Motors {offline_motors} did not respond.")
        error = True
        exit()

    # Returns: [([pos1], err1), ([pos2], err2), ...]
    bulk_result = bear.bulk_read(m_ids, ['present_position'])

    # Extract just the position values into a list of lists: [[pos1], [pos2], ...]
    home = [res[0] for res in bulk_result]

    # Note: register names must be in a list, even if it's just one
    bear.bulk_write(m_ids, ['goal_position'], home)

    # Enable BEAR
    bear.set_torque_enable(*[(m_id, 1) for m_id in m_ids])

    for i in range(len(t_points)):
        # 1. Send q_points[i] to your motor SDK here
        move_motors(bear, m_ids, q_points[i])
        
        # 2. Calculate sleep time until the next waypoint
        if i < len(t_points) - 1:
            dt = t_points[i+1] - t_points[i]
            time.sleep(dt)

    print('BEAR performed its motion!')
    time.sleep(2)

    # Turn off BEAR
    input('Press Enter to turn off BEAR.')
    # Disable BEAR
    bear.set_torque_enable(*[(m_id, 0) for m_id in m_ids])

    print("Thanks for using BEAR!")