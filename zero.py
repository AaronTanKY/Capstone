from pybear import Manager
import argparse
from configure import decode_error_code, read_register

# Replace 'COM3' with the port you found in Device Manager
# Default baudrate for BEAR is 8,000,000 (8M)
PORT = 'COM3'
BAUDRATE = 8000000


def zero_all_motors(bear, motor_ids, position):
    """
    Move every motor to the same absolute position.
    """
    for active_bear_id in motor_ids:
        bear.set_posi((active_bear_id, position, 0.2))


def read_all_positions(bear, motor_ids):
    """
    Read and print the present position for each motor.
    """
    results = []
    for active_bear_id in motor_ids:
        updated_pos, updated_pos_error = read_register(bear, active_bear_id, bear.get_present_position)
        error_text = decode_error_code(updated_pos_error)
        print(f"Set BEAR ID {active_bear_id} position to {updated_pos} | error: {error_text}")
        results.append(error_text)
    return results


def run_zero_sequence(bear, motor_ids=None):
    """
    Zero all motors with the interactive 0.2 and 0 confirmation flow.
    """
    if motor_ids is None:
        motor_ids = list(range(1, 11))

    while True:
        zero_all_motors(bear, motor_ids, 0.2)
        errors = read_all_positions(bear, motor_ids)

        if any(error_text != "Good!" for error_text in errors):
            retry = input("Error detected. Press Enter to rerun the exact same 0.2 move, or type q then Enter to move on to 0: ")
            if retry.lower().strip() == 'q':
                break
            continue

        confirm = input("Press Enter to move all motors to 0 once, or type r then Enter to rerun the 0.2 move: ")
        if confirm.lower().strip() == 'r':
            continue
        break

    while True:
        zero_all_motors(bear, motor_ids, 0)
        errors = read_all_positions(bear, motor_ids)

        if any(error_text != "Good!" for error_text in errors):
            retry = input("Error detected. Press Enter to rerun the exact same 0 move, or type q then Enter to quit: ")
            if retry.lower().strip() == 'q':
                break
            continue

        retry = input("Press Enter to rerun the 0 move, or type q then Enter to quit: ")
        if retry.lower().strip() == 'q':
            break

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Configure BEAR device (override defaults with CLI args)")
    parser.add_argument('--port', '-p', help='Serial port (default from file)', default=None)
    args = parser.parse_args()

    active_port = args.port if args.port is not None else PORT

    # Initialize bear
    bear = Manager.BEAR(port=active_port, baudrate=BAUDRATE)
    run_zero_sequence(bear)
