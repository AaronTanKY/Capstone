import time
import yaml
from pybear import Manager

# Replace 'COM3' with the port you found in Device Manager
# Default baudrate for BEAR is 8,000,000 (8M)
# Note: Ensure your USB2BEAR switch is set to the correct baudrate/mode
PORT = 'COM3'
BAUDRATE = 8000000 
BEAR_ID = 1


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
        
        # Test connection first
        ping_result = bear.ping(bear_id)
        if ping_result[0][0] is None:
            print(f"Error: Cannot ping BEAR ID {bear_id}")
            return None
        
        print(f"Retrieving all information from BEAR ID {bear_id}...")
        
        # === Configuration Registers ===
        info['id'] = bear.get_id(bear_id)[0][0][0]
        info['mode'] = bear.get_mode(bear_id)[0][0][0]
        info['baudrate'] = bear.get_baudrate(bear_id)[0][0][0]
        info['homing_offset'] = bear.get_homing_offset(bear_id)[0][0][0]
        
        # ID Control Gains
        info['p_gain_id'] = bear.get_p_gain_id(bear_id)[0][0][0]
        info['i_gain_id'] = bear.get_i_gain_id(bear_id)[0][0][0]
        info['d_gain_id'] = bear.get_d_gain_id(bear_id)[0][0][0]
        
        # IQ Control Gains
        info['p_gain_iq'] = bear.get_p_gain_iq(bear_id)[0][0][0]
        info['i_gain_iq'] = bear.get_i_gain_iq(bear_id)[0][0][0]
        info['d_gain_iq'] = bear.get_d_gain_iq(bear_id)[0][0][0]
        
        # Velocity Control Gains
        info['p_gain_velocity'] = bear.get_p_gain_velocity(bear_id)[0][0][0]
        info['i_gain_velocity'] = bear.get_i_gain_velocity(bear_id)[0][0][0]
        info['d_gain_velocity'] = bear.get_d_gain_velocity(bear_id)[0][0][0]
        
        # Position Control Gains
        info['p_gain_position'] = bear.get_p_gain_position(bear_id)[0][0][0]
        info['i_gain_position'] = bear.get_i_gain_position(bear_id)[0][0][0]
        info['d_gain_position'] = bear.get_d_gain_position(bear_id)[0][0][0]
        
        # Force Control Gains
        info['p_gain_force'] = bear.get_p_gain_force(bear_id)[0][0][0]
        info['i_gain_force'] = bear.get_i_gain_force(bear_id)[0][0][0]
        info['d_gain_force'] = bear.get_d_gain_force(bear_id)[0][0][0]
        
        # Limits
        info['limit_acc_max'] = bear.get_limit_acc_max(bear_id)[0][0][0]
        info['limit_i_max'] = bear.get_limit_i_max(bear_id)[0][0][0]
        info['limit_velocity_max'] = bear.get_limit_velocity_max(bear_id)[0][0][0]
        info['limit_position_min'] = bear.get_limit_position_min(bear_id)[0][0][0]
        info['limit_position_max'] = bear.get_limit_position_max(bear_id)[0][0][0]
        
        # Voltage Limits
        info['min_voltage'] = bear.get_min_voltage(bear_id)[0][0][0]
        info['max_voltage'] = bear.get_max_voltage(bear_id)[0][0][0]
        
        # Temperature Limits
        info['temp_limit_low'] = bear.get_temp_limit_low(bear_id)[0][0][0]
        info['temp_limit_high'] = bear.get_temp_limit_high(bear_id)[0][0][0]
        
        # Watchdog
        info['watchdog_timeout'] = bear.get_watchdog_timeout(bear_id)[0][0][0]
        
        # === Status Registers ===
        info['torque_enable'] = bear.get_torque_enable(bear_id)[0][0][0]
        info['goal_id'] = bear.get_goal_id(bear_id)[0][0][0]
        info['goal_iq'] = bear.get_goal_iq(bear_id)[0][0][0]
        info['goal_velocity'] = bear.get_goal_velocity(bear_id)[0][0][0]
        info['goal_position'] = bear.get_goal_position(bear_id)[0][0][0]
        
        # Present Values
        info['present_id'] = bear.get_present_id(bear_id)[0][0][0]
        info['present_iq'] = bear.get_present_iq(bear_id)[0][0][0]
        info['present_velocity'] = bear.get_present_velocity(bear_id)[0][0][0]
        info['present_position'] = bear.get_present_position(bear_id)[0][0][0]
        
        # Sensor Values
        info['input_voltage'] = bear.get_input_voltage(bear_id)[0][0][0]
        info['winding_temperature'] = bear.get_winding_temperature(bear_id)[0][0][0]
        info['powerstage_temperature'] = bear.get_powerstage_temperature(bear_id)[0][0][0]
        info['ic_temperature'] = bear.get_ic_temperature(bear_id)[0][0][0]
        
        print("Successfully retrieved all information.")
        return info
        
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


def get_info_example(bear, id):
    """
    Example function demonstrating how to use get_all_info.
    """    
    # Get all current information
    all_info = get_all_info(bear, id)
    
    if all_info:
        print("\n=== Current BEAR Configuration ===")
        for key, value in all_info.items():
            print(f"{key}: {value}")

def set_info_example(bear, save_to_flash):
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
        
        return set_all_info(bear, BEAR_ID, new_config, save_to_flash=save_to_flash)
    except FileNotFoundError:
        print("Error: config.yaml not found in current directory")
    except yaml.YAMLError as e:
        print(f"Error parsing config.yaml: {e}")
    return None


if __name__ == "__main__":
    
    # Initialize bear
    bear = Manager.BEAR(port=PORT, baudrate=BAUDRATE)
    
    # Getting all info
    get_info_example(bear=bear, id=3)
    
    # # Setting necessary info
    # updated_bear_id = set_info_example(bear=bear, save_to_flash=True)
    # if updated_bear_id is None:
    #     updated_bear_id = BEAR_ID

    # # Seeing if setting works
    # get_info_example(bear=bear, id=updated_bear_id)
    
    
    