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
        with open(config_file, 'r') as file:
            self.config = json.load(file)
        # with open(config_file, 'r') as file:
        #     config = yaml.safe_load(file)
        self.robot_id = self.config['robot_id']
        self.battery = self.config['battery']
        self.motor = self.config['motor']
        self.is_grabbing = self.config['is_grabbing']

        print(self.robot_id)

        if not os.path.exists(self.config_file):
            logger.error("Config file not found: %s", self.config_file)
            raise ConfigFileNotFoundError(self.config_file)

        # try:
        #     with open(self.config_file, 'r') as f:
        #         self.config = self._parse_file(f)
        #     logger.info("Loaded config: %s", self.config_file)
        # except (json.JSONDecodeError, ValueError) as e:
        #     logger.error("Parse error in '%s': %s", self.config_file, e)
        #     raise ConfigParseError(self.config_file, str(e)) from e

    def save(self, output_file=None):
        """Save current configuration to file."""
        # Save to file (auto-detect format from extension)

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
        print("starting validation...")
        if 'robot_id' not in self.config:
            errors.append("Missing required field: sensor_name")
        else:
            print("found id")

        if 'battery' in self.config:
            print("found battery")
            battery = self.config['battery']

            if not isinstance(battery, dict):
                errors.append("battery must be a dictionary")
            elif 'capacity' not in battery:
                errors.append("battery capacity is required")
            elif not isinstance(battery['capacity'], int):
                errors.append("capacity must be an integer")
            elif battery['capacity'] <= 0:
                errors.append("capacity must be greater than zero")
            else:
                print("found capacity")

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
            else:
                print("found current_level")

        if 'motor' in self.config:
            print("found motor")
            motor = self.config['motor']

            if not isinstance(motor, dict):
                errors.append("motor must be a dictionary")
            elif 'speed' not in motor:
                errors.append("motor speed is required")
            elif not isinstance(motor['speed'], int):
                errors.append("speed must be an integer")
            elif motor['speed'] < 0:
                errors.append("speed must be equal to or greater than zero")
            else:
                print("found speed")

            if not isinstance(motor, dict):
                errors.append("motor must be a dictionary")
            elif 'is_running' not in motor:
                errors.append("motor is_running is required")
            elif not isinstance(motor['is_running'], bool):
                errors.append("is_running must be a bool")
            else:
                print("found is_running")

        if errors:
            logger.warning("Validation failed with %d error(s)", len(errors))
            # raise CalibrationValidationError(errors)
        logger.debug("Calibration validation passed")


    # Save() configuration
    # write back to file in detected format, printed nicley for readability

config_manager = ConfigurationManager('example_configs/grabber_robot.json')
config_manager.validate()

print("\n")
print(config_manager.battery)
print(config_manager.motor)
print(config_manager.is_grabbing)


# securityCamera = SecurityCamera("Security Camera")
# print(securityCamera.report_status)
