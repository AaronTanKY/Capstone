import argparse

from pybear import Manager


MOTOR_IDS = list(range(1, 11))
DEFAULT_PORT = 'COM3'
DEFAULT_BAUDRATE = 8000000


def torque_off_all_motors(bear, motor_ids):
    bear.set_torque_enable(*[(motor_id, 0) for motor_id in motor_ids])


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Disable torque on all BEAR motors.')
    parser.add_argument('--port', '-p', default=DEFAULT_PORT, help='Serial port')
    parser.add_argument('--baudrate', '-b', type=int, default=DEFAULT_BAUDRATE, help='Serial baudrate')
    args = parser.parse_args()

    bear = Manager.BEAR(port=args.port, baudrate=args.baudrate)

    try:
        torque_off_all_motors(bear, MOTOR_IDS)
        print('Torque disabled on all motors.')
    finally:
        bear.close_port()