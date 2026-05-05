import time
import yaml
from pybear import Manager
import argparse

# Replace 'COM3' with the port you found in Device Manager
# Default baudrate for BEAR is 8,000,000 (8M)
# Note: Ensure your USB2BEAR switch is set to the correct baudrate/mode
PORT = 'COM3'
BAUDRATE = 8000000 
BEAR_ID = 1


def read_register(bear, bear_id, getter):
    """
    Read a single register using a Manager getter and return value plus error code.
    """
    data, error_code = getter(bear_id)[0]
    value = data[0] if data else None
    return value, error_code


def get_all_info(bear, bear_id):
    """
    Retrieve all BEAR configuration and status information.
    
    Args:
        bear: Manager.BEAR instance
        bear_id: ID of the BEAR to query
    
    Returns:
        Dictionary containing all BEAR parameters, or None if connection failed
    """
    try:
        info = {}
        errors = {}
        
        # Test connection first
        ping_value, ping_error = bear.ping(bear_id)[0]
        if ping_value[0] is None:
            print(f"Error: Cannot ping BEAR ID {bear_id}")
            return None

        errors['ping'] = ping_error
        
        print(f"Retrieving all information from BEAR ID {bear_id}...")
        
        # === Configuration Registers ===
        info['id'], errors['id'] = read_register(bear, bear_id, bear.get_id)
        info['mode'], errors['mode'] = read_register(bear, bear_id, bear.get_mode)
        info['baudrate'], errors['baudrate'] = read_register(bear, bear_id, bear.get_baudrate)
        info['homing_offset'], errors['homing_offset'] = read_register(bear, bear_id, bear.get_homing_offset)
        
        # ID Control Gains
        info['p_gain_id'], errors['p_gain_id'] = read_register(bear, bear_id, bear.get_p_gain_id)
        info['i_gain_id'], errors['i_gain_id'] = read_register(bear, bear_id, bear.get_i_gain_id)
        info['d_gain_id'], errors['d_gain_id'] = read_register(bear, bear_id, bear.get_d_gain_id)
        
        # IQ Control Gains
        info['p_gain_iq'], errors['p_gain_iq'] = read_register(bear, bear_id, bear.get_p_gain_iq)
        info['i_gain_iq'], errors['i_gain_iq'] = read_register(bear, bear_id, bear.get_i_gain_iq)
        info['d_gain_iq'], errors['d_gain_iq'] = read_register(bear, bear_id, bear.get_d_gain_iq)
        
        # Velocity Control Gains
        info['p_gain_velocity'], errors['p_gain_velocity'] = read_register(bear, bear_id, bear.get_p_gain_velocity)
        info['i_gain_velocity'], errors['i_gain_velocity'] = read_register(bear, bear_id, bear.get_i_gain_velocity)
        info['d_gain_velocity'], errors['d_gain_velocity'] = read_register(bear, bear_id, bear.get_d_gain_velocity)
        
        # Position Control Gains
        info['p_gain_position'], errors['p_gain_position'] = read_register(bear, bear_id, bear.get_p_gain_position)
        info['i_gain_position'], errors['i_gain_position'] = read_register(bear, bear_id, bear.get_i_gain_position)
        info['d_gain_position'], errors['d_gain_position'] = read_register(bear, bear_id, bear.get_d_gain_position)
        
        # Force Control Gains
        info['p_gain_force'], errors['p_gain_force'] = read_register(bear, bear_id, bear.get_p_gain_force)
        info['i_gain_force'], errors['i_gain_force'] = read_register(bear, bear_id, bear.get_i_gain_force)
        info['d_gain_force'], errors['d_gain_force'] = read_register(bear, bear_id, bear.get_d_gain_force)
        
        # Limits
        info['limit_acc_max'], errors['limit_acc_max'] = read_register(bear, bear_id, bear.get_limit_acc_max)
        info['limit_i_max'], errors['limit_i_max'] = read_register(bear, bear_id, bear.get_limit_i_max)
        info['limit_velocity_max'], errors['limit_velocity_max'] = read_register(bear, bear_id, bear.get_limit_velocity_max)
        info['limit_position_min'], errors['limit_position_min'] = read_register(bear, bear_id, bear.get_limit_position_min)
        info['limit_position_max'], errors['limit_position_max'] = read_register(bear, bear_id, bear.get_limit_position_max)
        
        # Voltage Limits
        info['min_voltage'], errors['min_voltage'] = read_register(bear, bear_id, bear.get_min_voltage)
        info['max_voltage'], errors['max_voltage'] = read_register(bear, bear_id, bear.get_max_voltage)
        
        # Temperature Limits
        info['temp_limit_low'], errors['temp_limit_low'] = read_register(bear, bear_id, bear.get_temp_limit_low)
        info['temp_limit_high'], errors['temp_limit_high'] = read_register(bear, bear_id, bear.get_temp_limit_high)
        
        # Watchdog
        info['watchdog_timeout'], errors['watchdog_timeout'] = read_register(bear, bear_id, bear.get_watchdog_timeout)
        
        # === Status Registers ===
        info['torque_enable'], errors['torque_enable'] = read_register(bear, bear_id, bear.get_torque_enable)
        info['goal_id'], errors['goal_id'] = read_register(bear, bear_id, bear.get_goal_id)
        info['goal_iq'], errors['goal_iq'] = read_register(bear, bear_id, bear.get_goal_iq)
        info['goal_velocity'], errors['goal_velocity'] = read_register(bear, bear_id, bear.get_goal_velocity)
        info['goal_position'], errors['goal_position'] = read_register(bear, bear_id, bear.get_goal_position)
        
        # Present Values
        info['present_id'], errors['present_id'] = read_register(bear, bear_id, bear.get_present_id)
        info['present_iq'], errors['present_iq'] = read_register(bear, bear_id, bear.get_present_iq)
        info['present_velocity'], errors['present_velocity'] = read_register(bear, bear_id, bear.get_present_velocity)
        info['present_position'], errors['present_position'] = read_register(bear, bear_id, bear.get_present_position)
        
        # Sensor Values
        info['input_voltage'], errors['input_voltage'] = read_register(bear, bear_id, bear.get_input_voltage)
        info['winding_temperature'], errors['winding_temperature'] = read_register(bear, bear_id, bear.get_winding_temperature)
        info['powerstage_temperature'], errors['powerstage_temperature'] = read_register(bear, bear_id, bear.get_powerstage_temperature)
        info['ic_temperature'], errors['ic_temperature'] = read_register(bear, bear_id, bear.get_ic_temperature)
        
        print("Successfully retrieved all information.")
        return {'values': info, 'errors': errors}
        
    except Exception as e:
        print(f"Error retrieving BEAR information: {e}")
        return None


def set_all_info(bear, bear_id, config_dict, save_to_flash=False):
    """
    Set BEAR configuration parameters from a dictionary.
    
    Args:
        bear: Manager.BEAR instance
        bear_id: ID of the BEAR to configure
        config_dict: Dictionary containing configuration parameters to set
        save_to_flash: If True, saves configuration to flash memory
    
    Note:
        Only configuration registers can be set. Status/present values are read-only.
        Always disables torque before saving to flash.
    """
    try:
        active_bear_id = bear_id
        print(f"Configuring BEAR ID {active_bear_id}...")
        
        # Configuration register names that can be set
        config_setters = {
            'id': bear.set_id,
            'mode': bear.set_mode,
            'baudrate': bear.set_baudrate,
            'homing_offset': bear.set_homing_offset,
            'p_gain_id': bear.set_p_gain_id,
            'i_gain_id': bear.set_i_gain_id,
            'd_gain_id': bear.set_d_gain_id,
            'p_gain_iq': bear.set_p_gain_iq,
            'i_gain_iq': bear.set_i_gain_iq,
            'd_gain_iq': bear.set_d_gain_iq,
            'p_gain_velocity': bear.set_p_gain_velocity,
            'i_gain_velocity': bear.set_i_gain_velocity,
            'd_gain_velocity': bear.set_d_gain_velocity,
            'p_gain_position': bear.set_p_gain_position,
            'i_gain_position': bear.set_i_gain_position,
            'd_gain_position': bear.set_d_gain_position,
            'p_gain_force': bear.set_p_gain_force,
            'i_gain_force': bear.set_i_gain_force,
            'd_gain_force': bear.set_d_gain_force,
            'limit_acc_max': bear.set_limit_acc_max,
            'limit_i_max': bear.set_limit_i_max,
            'limit_velocity_max': bear.set_limit_velocity_max,
            'limit_position_min': bear.set_limit_position_min,
            'limit_position_max': bear.set_limit_position_max,
            'min_voltage': bear.set_min_voltage,
            'max_voltage': bear.set_max_voltage,
            'temp_limit_low': bear.set_temp_limit_low,
            'temp_limit_high': bear.set_temp_limit_high,
            'watchdog_timeout': bear.set_watchdog_timeout,
        }
        
        # Status registers that can also be set
        status_setters = {
            'torque_enable': bear.set_torque_enable,
            'goal_id': bear.set_goal_id,
            'goal_iq': bear.set_goal_iq,
            'goal_velocity': bear.set_goal_velocity,
            'goal_position': bear.set_goal_position,
        }
        
        # Apply ID first so all subsequent writes target the updated device ID.
        if 'id' in config_dict:
            new_bear_id = config_dict['id']
            config_setters['id']((active_bear_id, new_bear_id))
            print(f"  Set id = {new_bear_id}")
            active_bear_id = new_bear_id

        # Apply remaining configuration changes
        for param_name, value in config_dict.items():
            if param_name == 'id':
                continue

            if param_name in config_setters:
                config_setters[param_name]((active_bear_id, value))
                print(f"  Set {param_name} = {value}")
            elif param_name in status_setters:
                status_setters[param_name]((active_bear_id, value))
                print(f"  Set {param_name} = {value}")
            else:
                print(f"  Warning: {param_name} is read-only and cannot be set")
        
        # Explicitly set position if needed
        position_reset = config_dict.get('position_reset')
        if position_reset is not None:
            print(f"  Setting position to {position_reset}...")
            bear.set_posi((active_bear_id, position_reset, 0.2))
        
        # Save to flash if requested
        if save_to_flash:
            print("Disabling torque before saving to flash...")
            bear.set_torque_enable((active_bear_id, 0))
            time.sleep(0.1)
            
            print("Saving configuration to flash memory...")
            bear.save_config(active_bear_id)
            time.sleep(0.1)
            print("Configuration saved successfully.")
        
        print(f"Configuration complete. Active BEAR ID is now {active_bear_id}.")
        return active_bear_id
        
    except Exception as e:
        print(f"Error configuring BEAR: {e}")
        return None


def scan_bear_ids(bear, verbose=False):
    """
    Scan all possible BEAR IDs (1-255) and report which ones can be pinged.
    
    Args:
        bear: Manager.BEAR instance
        verbose: If True, prints status for each ID checked; if False, only prints found IDs
    
    Returns:
        List of IDs that successfully responded to ping
    """
    found_ids = []
    print("Scanning for BEAR motors on the bus...")
    
    for bear_id in range(0, 255):
        ping_value, ping_error = bear.ping(bear_id)[0]
        if ping_value[0] is None:
            print(f"  ✗ ID {bear_id}: No response")
        else:
            found_ids.append(bear_id)
            print(f"  ✓ Found BEAR ID {bear_id}")
        
    
    print(f"\nScan complete. Found {len(found_ids)} BEAR(s): {found_ids}")
    return found_ids


def get_info_example(bear, id):
    """
    Example function demonstrating how to use get_all_info.
    """    
    # Get all current information
    all_info = get_all_info(bear, id)
    
    if all_info:
        print("\n=== Current BEAR Configuration ===")
        values = all_info['values']
        errors = all_info['errors']
        for key, value in values.items():
            print(f"{key}: {value} | error: {errors.get(key)}")

def set_info_example(bear, save_to_flash, bear_id=BEAR_ID):
    """
    Example function demonstrating how to use set_all_info.
    """    
    # Example: Load configuration from YAML file
    print("\n=== Applying New Configuration ===")
    try:
        with open('config.yaml', 'r') as f:
            new_config = yaml.safe_load(f)
            # Remove None values to avoid setting unchanged parameters
            new_config = {k: v for k, v in new_config.items() if v is not None}
        
        return set_all_info(bear, bear_id, new_config, save_to_flash=save_to_flash)
    except FileNotFoundError:
        print("Error: config.yaml not found in current directory")
    except yaml.YAMLError as e:
        print(f"Error parsing config.yaml: {e}")
    return None


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Configure BEAR device (override defaults with CLI args)")
    parser.add_argument('--port', '-p', help='Serial port (default from file)', default=None)
    parser.add_argument('--bear-id', '-i', type=int, help='BEAR ID (default from file)', default=None)
    args = parser.parse_args()

    active_port = args.port if args.port is not None else PORT
    active_bear_id = args.bear_id if args.bear_id is not None else BEAR_ID

    # Initialize bear
    bear = Manager.BEAR(port=active_port, baudrate=BAUDRATE)
    
    # # Scan for ID
    # scan_bear_ids(bear=bear)

    # Getting all info
    get_info_example(bear=bear, id=active_bear_id)
    input('This is current config. Press ENTER to set configs.')
    
    # Setting necessary info
    updated_bear_id = set_info_example(bear=bear, save_to_flash=True, bear_id=active_bear_id)
    if updated_bear_id is None:
        updated_bear_id = active_bear_id
    input('Configs updated. Press ENTER to see new configs.')

    # Seeing if setting works
    get_info_example(bear=bear, id=updated_bear_id)
    input('New config printed. Press ENTER to close.')
    
    # To run: python configure.py --port COM4 --bear-id 2
    