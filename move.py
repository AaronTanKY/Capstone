from pybear import Manager
import pandas as pd
import time
import argparse
from pathlib import Path
import random


def choose_csv_file(csv_dir):
    """
    Prompt the user to select a CSV file from the local csv directory.
    """
    csv_files = sorted(csv_dir.glob('*.csv'))

    if not csv_files:
        raise FileNotFoundError(f"No CSV files found in {csv_dir}")

    print("Available CSV files:")
    for index, csv_file in enumerate(csv_files, start=1):
        print(f"  {index}. {csv_file.name}")

    while True:
        selection = input(f"Select a CSV file to run (1-{len(csv_files)}): ").strip()
        try:
            selected_index = int(selection)
        except ValueError:
            print("Please enter a number from the list.")
            continue

        if 1 <= selected_index <= len(csv_files):
            return csv_files[selected_index - 1]

        print("Selection out of range. Try again.")


def choose_random_csv_file(csv_dir):
    """
    Select a CSV file at random from the local csv directory.
    """
    csv_files = sorted(csv_dir.glob('*.csv'))

    if not csv_files:
        raise FileNotFoundError(f"No CSV files found in {csv_dir}")

    return random.choice(csv_files)

def move_motors(bear, m_ids, goal_pos):
    """
    Move multiple BEAR motors simultaneously using bulk_write
    """
    # Bulk write requires a list of lists for data: [[pos1], [pos2], ... [posN]]
    # Each inner list contains the values for the registers specified (here, just one)
    bulk_data = [[pos] for pos in goal_pos]
    
    # Syntax: bear.bulk_write([IDs], [Registers], [[Data_for_ID1], [Data_for_ID2]...])
    bear.bulk_write(m_ids, ['goal_position'], bulk_data)


def run_motion_from_csv(bear, m_ids, csv_path, wait_for_user=True, disable_torque_at_end=True):
    """
    Run the standard CSV motion routine for an already-connected BEAR instance.
    """
    try:
        df = pd.read_csv(csv_path, header=None)
        t_points = df.iloc[:, 0].values
        q_points = df.iloc[:, 1:11].values

        results = bear.ping(*m_ids)
        offline_motors = [m_ids[i] for i, res in enumerate(results) if res is None]
        if offline_motors:
            print(f"Error: Motors {offline_motors} did not respond.")
            raise SystemExit(1)

        print("System Clear.")

        bulk_result = bear.bulk_read(m_ids, ['present_position'])
        home = [res[0] for res in bulk_result]
        bear.bulk_write(m_ids, ['goal_position'], home)

        bear.set_goal_velocity(*[(m_id, 2) for m_id in m_ids])
        bear.set_torque_enable(*[(m_id, 1) for m_id in m_ids])

        print("Homing to start position...")
        bulk_result = bear.bulk_read(m_ids, ['present_position'])
        current_positions = [res[0][0] for res in bulk_result]
        target_start = q_points[0]

        homing_duration = 2.0
        hz = 100
        steps = int(homing_duration * hz)

        for step in range(steps + 1):
            alpha = step / steps
            interp_pos = [
                (1 - alpha) * curr + alpha * targ
                for curr, targ in zip(current_positions, target_start)
            ]

            move_motors(bear, m_ids, interp_pos)
            time.sleep(1.0 / hz)

        print("Ready. Starting CSV motion...")
        time.sleep(0.5)

        start_time = time.time()

        for index in range(len(t_points)):
            move_motors(bear, m_ids, q_points[index])

            if index < len(t_points) - 1:
                next_time = start_time + t_points[index + 1]
                sleep_time = max(0, next_time - time.time())
                time.sleep(sleep_time)

        print('BEAR performed its motion!')
        time.sleep(2)

        if wait_for_user:
            input('Press Enter to turn off BEAR.')

        if disable_torque_at_end:
            bear.set_torque_enable(*[(m_id, 0) for m_id in m_ids])
        else:
            print('Leaving torque enabled for the next random playback.')

        print("Thanks for using BEAR!")
    except KeyboardInterrupt:
        bear.set_torque_enable(*[(m_id, 0) for m_id in m_ids])
        print("Motion interrupted. BEAR torque disabled.")


def run_random_csv_playback(bear, m_ids, csv_dir):
    """
    Keep selecting random CSV files and replaying them until the user stops.
    """
    csv_dir = Path(csv_dir)

    try:
        while True:
            selected_csv = choose_random_csv_file(csv_dir)
            print(f"Randomly selected: {selected_csv.name}")
            run_motion_from_csv(
                bear,
                m_ids,
                selected_csv,
                wait_for_user=False,
                disable_torque_at_end=False,
            )
            time.sleep(2)
    except KeyboardInterrupt:
        bear.set_torque_enable(*[(m_id, 0) for m_id in m_ids])
        print("Random playback interrupted. BEAR torque disabled.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="BEAR Multi-Motor Control")
    parser.add_argument('--port', '-p', help='Serial port (default from file)', default='COM3')
    parser.add_argument('--csv-dir', '-d', help='Directory containing CSV files', default=None)
    parser.add_argument('--baudrate', '-b', help='Baudrate', type=int, default=8000000)
    args = parser.parse_args()
    
    m_ids = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

    csv_dir = Path(args.csv_dir) if args.csv_dir is not None else Path(__file__).resolve().parent / 'csv'
    selected_csv = choose_csv_file(csv_dir)

    # Initialize bear
    bear = Manager.BEAR(port=args.port, baudrate=args.baudrate)
    run_motion_from_csv(bear, m_ids, selected_csv)