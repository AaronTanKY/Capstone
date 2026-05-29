import argparse
from pathlib import Path

from pybear import Manager

from move import choose_csv_file, run_motion_from_csv
from record_and_replay import run_record_and_replay
from zero import run_zero_sequence


SCRIPT_DIR = Path(__file__).resolve().parent


def prompt_mode():
    """
    Ask the user whether to run a saved CSV motion, record and replay, or quit.
    """
    print("\nWhat do you want to do next?")
    print("  1. Read from a CSV")
    print("  2. Record and replay motion")
    print("  q. Quit")

    while True:
        choice = input("Select 1, 2, or q: ").strip()
        if choice in {"1", "2", "q", "Q"}:
            return choice
        print("Please enter 1, 2, or q.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Main BEAR workflow: zero, then choose motion mode.")
    parser.add_argument('--port', '-p', help='Serial port', default='COM3')
    parser.add_argument('--csv-dir', '-d', help='Directory containing CSV files', default=str(SCRIPT_DIR / 'csv'))
    parser.add_argument('--baudrate', '-b', help='Baudrate for scripts that accept it', type=int, default=8000000)
    parser.add_argument('--sample-hz', help='Recording frequency in Hz for record_and_replay.py', type=float, default=50.0)
    parser.add_argument('--output', '-o', help='Output CSV path for record_and_replay.py', default=str(SCRIPT_DIR / 'csv'))
    args = parser.parse_args()

    bear = Manager.BEAR(port=args.port, baudrate=args.baudrate)

    print("Running zero.py first...")
    run_zero_sequence(bear)

    while True:
        mode = prompt_mode()

        if mode in {'q', 'Q'}:
            break

        if mode == '1':
            print("Launching move.py...")
            selected_csv = choose_csv_file(Path(args.csv_dir))
            run_motion_from_csv(bear, list(range(1, 11)), selected_csv)
        else:
            print("Launching record_and_replay.py...")
            run_record_and_replay(bear, list(range(1, 11)), args.sample_hz, args.output)

    print("Main workflow complete.")
