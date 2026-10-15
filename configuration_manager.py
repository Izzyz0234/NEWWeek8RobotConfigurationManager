from typing import Dict, Optional, Any
from configuration_errors import ConfigFileNotFoundError, ConfigParseError, ConfigValidationError
from example_configs.robot_types.week6RobobBaseInheritances import RobotBase, SecurityCamera
import os, logging, json, yaml

logger = logging.getLogger(__name__)


class ConfigurationManager:

    def __init__(self, config_file: str):
        """Initialize with configuration file path."""
        self.data = {}
        self.load(config_file)


    # Load() Json and Yaml file
    # raise ConfigFileNotFOundError and ConfigParseError
    def load(self, config_file):
        self.config_file = config_file
        """Load configuration, raising typed exceptions on failure.

        Raises:
            ConfigFileNotFoundError: If the config file does not exist.
            ConfigParseError: If the file exists but cannot be parsed.
        """
        # Robot class tied to specific file format
        if '.json' in config_file:
            try:
                with open(config_file, 'r') as file:
                    self.config = json.load(file)
            except json.JSONDecodeError as e:
                print("Error loading JSON file:", e)
                raise ConfigParseError(self.config_file, str(e)) from e
                
        if '.yaml' in config_file:
            try:
                with open(config_file, 'r') as file:
                    self.config = yaml.safe_load(file)
            except yaml.YAMLError as e:
                print("Error loading YAML file:", e)
                raise ConfigParseError(self.config_file, str(e)) from e


        self.robot_id = self.config['robot_id']
        self.battery = self.config['battery']
        self.motor = self.config['motor']

        if not os.path.exists(self.config_file):
            logger.error("Config file not found: %s", self.config_file)
            raise ConfigFileNotFoundError(self.config_file)

    # support value access
    # get('robot_id'), get('sensors.ir_count'), get('unknown_key', default=0)
    def get(self, key: str, default: Optional[Any] = None) -> Any:
        """Safely retrieve configuration value."""



    # Valadate() configuration
    # check feilds, type validation, range validation (sensor count > 0)
    # raises ConfigValidationError listing all failures
    def validate(self) -> None:
        """Validate calibration config, raising CalibrationValidationError if invalid."""
        errors = []
        if 'robot_id' not in self.config:
            errors.append("Missing required field: sensor_name")

        if 'battery' in self.config:
            battery = self.config['battery']

            if not isinstance(battery, dict):
                errors.append("battery must be a dictionary")
            elif 'capacity' not in battery:
                errors.append("battery capacity is required")
            elif not isinstance(battery['capacity'], int):
                errors.append("capacity must be an integer")
            elif battery['capacity'] <= 0:
                errors.append("capacity must be greater than zero")

            if not isinstance(battery, dict):
                errors.append("battery must be a dictionary")
            elif 'current_level' not in battery:
                errors.append("battery current_level is required")
            elif not isinstance(battery['current_level'], int):
                errors.append("current_level must be an integer")
            elif battery['current_level'] < 0:
                errors.append("current_level must be equal to or greater than zero")
            elif battery['current_level'] > battery['capacity']:
                errors.append("current_level must be lower then capacity")

        if 'motor' in self.config:
            motor = self.config['motor']

            if not isinstance(motor, dict):
                errors.append("motor must be a dictionary")
            elif 'speed' not in motor:
                errors.append("motor speed is required")
            elif not isinstance(motor['speed'], int):
                errors.append("speed must be an integer")
            elif motor['speed'] < 0:
                errors.append("speed must be equal to or greater than zero")

            if not isinstance(motor, dict):
                errors.append("motor must be a dictionary")
            elif 'is_running' not in motor:
                errors.append("motor is_running is required")
            elif not isinstance(motor['is_running'], bool):
                errors.append("is_running must be a bool")

        if errors:
            logger.warning("Validation failed with %d error(s)", len(errors))
            # raise CalibrationValidationError(errors)
        logger.debug("Calibration validation passed")


    # Save() configuration
    # write back to file in detected format, printed nicley for readability
    def save(self, output_file=None):
        """Save current configuration to file."""
        # Save to file (auto-detect format from extension)

        print(self.robot_id)
        print(self.battery)
        print(self.motor)


print("\nJSON:")
json_config_manager = ConfigurationManager('example_configs/grabber_robot.json')
json_config_manager.validate()
json_config_manager.save()

print("\nYAML:")
yaml_config_manager = ConfigurationManager('example_configs/vacume_robot.yaml')
yaml_config_manager.validate()
yaml_config_manager.save()

# securityCamera = SecurityCamera("Security Camera")
# print(securityCamera.report_status)
