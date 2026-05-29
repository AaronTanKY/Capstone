from datetime import datetime
from pathlib import Path
import argparse
import time

import pandas as pd

from configure import decode_error_code
from pybear import Manager
from move import run_motion_from_csv


DEFAULT_M_IDS = list(range(1, 11))


def read_positions(bear, m_ids):
    """
    Read present positions for all motors with a single bulk_read call.
    """
    bulk_result = bear.bulk_read(m_ids, ['present_position'])

    positions = []
    errors = []
    for motor_id, (motor_data, error_code) in zip(m_ids, bulk_result):
        position = motor_data[0] if motor_data else None
        positions.append(position)
        errors.append(error_code)

        if error_code is not None:
            error_text = decode_error_code(error_code)
            if error_text != "Good!":
                print(f"Warning: BEAR ID {motor_id} read status: {error_text}")

    return positions, errors


def record_motion(bear, m_ids, sample_hz):
    """
    Continuously sample all motor positions until the user stops recording.
    """
    samples = []
    sample_period = 1.0 / sample_hz
    start_time = time.perf_counter()
    next_sample_time = start_time

    print("Recording motion. Press Ctrl+C to stop.")

    try:
        while True:
            sleep_time = next_sample_time - time.perf_counter()
            if sleep_time > 0:
                time.sleep(sleep_time)

            timestamp = time.perf_counter() - start_time
            positions, _ = read_positions(bear, m_ids)

            if any(position is None for position in positions):
                raise RuntimeError("Failed to read one or more motor positions during recording.")

            samples.append([timestamp, *positions])
            next_sample_time += sample_period
    except KeyboardInterrupt:
        print("Recording stopped.")

    return samples


def save_motion(samples, m_ids, output_path):
    """
    Save the recorded trajectory to a CSV file.
    """
    columns = ["time"] + [f"motor_{motor_id}" for motor_id in m_ids]
    motion_df = pd.DataFrame(samples, columns=columns)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    motion_df.to_csv(output_path, index=False, header=False)
    return motion_df


def resolve_output_path(output_arg):
    """
    Convert an output argument into a concrete CSV file path.
    """
    if output_arg is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        return Path(__file__).resolve().parent / "csv" / f"recorded_motion_{timestamp}.csv"

    output_path = Path(output_arg)

    if output_path.exists() and output_path.is_dir():
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        return output_path / f"recorded_motion_{timestamp}.csv"

    if output_path.suffix.lower() != ".csv":
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        return output_path / f"recorded_motion_{timestamp}.csv"

    return output_path


def replay_motion(bear, m_ids, csv_path):
    """
    Replay the recorded motion by reusing the standard move.py CSV runner.
    """
    run_motion_from_csv(bear, m_ids, csv_path)


def run_record_and_replay(bear, m_ids=None, sample_hz=50.0, output_arg=None):
    """
    Record motion with bulk_read and optionally replay it on the same connection.
    """
    if m_ids is None:
        m_ids = DEFAULT_M_IDS

    if sample_hz <= 0:
        raise ValueError("sample_hz must be greater than 0")

    ping_results = bear.ping(*m_ids)
    offline_motors = [m_ids[index] for index, result in enumerate(ping_results) if result is None]
    if offline_motors:
        print(f"Error: Motors {offline_motors} did not respond.")
        raise SystemExit(1)

    print("System Clear.")
    input("Move the motors, then press Enter to start recording.")

    samples = record_motion(bear, m_ids, sample_hz)

    if not samples:
        print("No samples were recorded.")
        raise SystemExit(1)

    output_path = resolve_output_path(output_arg)

    motion_df = save_motion(samples, m_ids, output_path)
    print(f"Saved recording to {output_path}")

    replay_choice = input("Press Enter to replay the recorded motion, or type q then Enter to quit: ")
    if replay_choice.lower().strip() != 'q':
        replay_motion(bear, m_ids, output_path)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Record BEAR motor motion and replay it.")
    parser.add_argument('--port', '-p', help='Serial port', default='COM3')
    parser.add_argument('--baudrate', '-b', help='Baudrate', type=int, default=8000000)
    parser.add_argument('--sample-hz', help='Recording frequency in Hz', type=float, default=50.0)
    parser.add_argument('--output', '-o', help='Output CSV file path', default=None)
    args = parser.parse_args()

    bear = Manager.BEAR(port=args.port, baudrate=args.baudrate)
    run_record_and_replay(bear, DEFAULT_M_IDS, args.sample_hz, args.output)