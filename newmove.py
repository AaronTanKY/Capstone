import argparse
import random
import glob
import time
from pybear import Manager
import numpy as np
import pandas as pd


def move_motors(bear, m_ids, goal_pos):
    """Move multiple BEAR motors simultaneously using bulk_write"""
    bulk_data = [[pos] for pos in goal_pos]
    bear.bulk_write(m_ids, ["goal_position"], bulk_data)


def interpolate_trajectory(t_points, q_points, current_time):
    """Interpolate positions if the loop frequency doesn't perfectly match the CSV timestamps."""
    # Clamp time to the limits of the animation file
    if current_time >= t_points[-1]:
        return q_points[-1], True  # Returns True if animation is finished

    # Linear interpolation between frames
    target_pos = []
    for col in range(q_points.shape[1]):
        pos = np.interp(current_time, t_points, q_points[:, col])
        target_pos.append(pos)

    return np.array(target_pos), False


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="BEAR Multi-Motor Control")
    parser.add_argument(
        "--port", "-p", help="Serial port (default from file)", default="COM3"
    )
    parser.add_argument(
        "--arm_data", "-a", help="Arm CSV file name", default="yes.csv"
    )
    parser.add_argument(
        "--head_data", "-h", help="Head CSV file name", default="yes.csv"
    )
    parser.add_argument(
        "--baudrate", "-b", help="Baudrate", type=int, default=8000000
    )
    args = parser.parse_args()

    # --- DEFINING MOTOR GROUP SEPARATIONS ---
    # Example separation: Change these lists to match your robot layout!
    arm_ids = [3, 4, 5, 6, 7, 8, 9, 10]
    head_ids = [1, 2]
    all_m_ids = arm_ids + head_ids

    # Load consistent arm animation data
    df_arm = pd.read_csv(args.arm_data, header=None)
    arm_t = df_arm.iloc[:, 0].values
    arm_q = df_arm.iloc[
        :, 3 : len(arm_ids) + 1
    ].values  # Slice exact count of arm columns

    # Gather all available head animation CSV files from a directory
    # Assumes you name them: head_idle1.csv, head_idle2.csv, etc.
    head_files = glob.glob("csv/head_idle*.csv")
    if not head_files:
        print(
            "Error: No head animation files found matching pattern 'head_idle*.csv'"
        )
        exit()

    # Initialize BEAR
    bear = Manager.BEAR(port=args.port, baudrate=args.baudrate)

    # Check connection
    results = bear.ping(*all_m_ids)
    offline_motors = [
        all_m_ids[i] for i, res in enumerate(results) if res is None
    ]
    if offline_motors:
        print(f"Error: Motors {offline_motors} did not respond.")
        exit()
    print("System Clear.")

    # Enable BEAR torque
    bear.set_torque_enable(*[(m_id, 1) for m_id in all_m_ids])

    # Dynamic animation tracking variables
    start_time = time.time()
    head_start_time = start_time

    # Load the first random head animation data setup
    current_head_file = random.choice(head_files)
    df_head = pd.read_csv(current_head_file, header=None)
    head_t = df_head.iloc[:, 0].values
    head_q = df_head.iloc[:, 1 : len(head_ids) + 1].values

    print(f"Starting loop. Initial Head track: {current_head_file}")

    # Set loop frequency control (e.g., 50Hz updates / 20ms steps)
    loop_hz = 50
    dt = 1.0 / loop_hz

    try:
        while True:
            loop_start = time.time()

            # 1. Calculate time relative to the tracks
            current_time = time.time()
            arm_elapsed = (current_time - start_time) % arm_t[-1]  # Loop arm endlessly
            head_elapsed = current_time - head_start_time

            # 2. Extract arm targets
            arm_targets, _ = interpolate_trajectory(arm_t, arm_q, arm_elapsed)

            # 3. Extract head targets and swap track if the current one finished
            head_targets, head_finished = interpolate_trajectory(
                head_t, head_q, head_elapsed
            )

            if head_finished:
                # Pick a new unique random head track
                new_head_file = random.choice(head_files)
                df_head = pd.read_csv(new_head_file, header=None)
                head_t = df_head.iloc[:, 0].values
                head_q = df_head.iloc[:, 1 : len(head_ids) + 1].values

                # Reset the head clock tracking relative to standard clock
                head_start_time = time.time()
                print(f"Switching Head Track to: {new_head_file}")
                # Re-evaluate targets instantly for the new file boundary
                head_targets, _ = interpolate_trajectory(head_t, head_q, 0)

            # 4. Combine the command lists together for a single bulk_write packet
            combined_ids = arm_ids + head_ids
            combined_targets = np.concatenate((arm_targets, head_targets))

            move_motors(bear, combined_ids, combined_targets)

            # 5. Precise loop timing maintenance
            elapsed_work = time.time() - loop_start
            sleep_time = max(0, dt - elapsed_work)
            time.sleep(sleep_time)

    except KeyboardInterrupt:
        print("\nStopping animations safely...")

    # Disable BEAR
    bear.set_torque_enable(*[(m_id, 0) for m_id in all_m_ids])
    print("Motors safely powered down. Thanks for using BEAR!")