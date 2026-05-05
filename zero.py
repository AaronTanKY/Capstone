from pybear import Manager
import argparse
from configure import read_register

# Replace 'COM3' with the port you found in Device Manager
# Default baudrate for BEAR is 8,000,000 (8M)
PORT = 'COM3'
BAUDRATE = 8000000

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Configure BEAR device (override defaults with CLI args)")
    parser.add_argument('--port', '-p', help='Serial port (default from file)', default=None)
    args = parser.parse_args()

    active_port = args.port if args.port is not None else PORT

    # Initialize bear
    bear = Manager.BEAR(port=active_port, baudrate=BAUDRATE)

    for active_bear_id in range(1, 11):
        bear.set_posi((active_bear_id, 0, 0))
        updated_pos, updated_pos_error = read_register(bear, active_bear_id, bear.get_present_position)
        print(f"Set BEAR ID {active_bear_id} position to {updated_pos} | error: {updated_pos_error}")
