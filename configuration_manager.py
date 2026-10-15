from typing import Dict, Optional, Any
from configuration_errors import ConfigFileNotFoundError, ConfigParseError, ConfigValidationError
from example_configs.robot_types.week6RobobBaseInheritances import RobotBase, SecurityCamera
import os, logging, json, yaml

logger = logging.getLogger(__name__)


class ConfigurationManager:

    def __init__(self, config_file: str):
        """Initialize with configuration file path."""
        self.config = {}
        self.load(config_file)


    # Load() Json and Yaml file
    # raise ConfigFileNotFOundError and ConfigParseError
    def load(self, config_file):
        """Load configuration, raising typed exceptions on failure.

        Raises:
            ConfigFileNotFoundError: If the config file does not exist.
            ConfigParseError: If the file exists but cannot be parsed.
        """
        # Robot class tied to specific file format
        self.config_file = config_file
        if '.json' in config_file:
            self.file_type = "JSON"
            try:
                with open(config_file, 'r') as file:
                    self.config = json.load(file)
            except json.JSONDecodeError as e:
                print("Error loading JSON file:", e)
                raise ConfigParseError(self.config_file, str(e)) from e
                
        if '.yaml' in config_file:
            self.file_type = "YAML"
            try:
                with open(config_file, 'r') as file:
                    self.config = yaml.safe_load(file)
            except yaml.YAMLError as e:
                print("Error loading YAML file:", e)
                raise ConfigParseError(self.config_file, str(e)) from e

        if not os.path.exists(self.config_file):
            logger.error("Config file not found: %s", self.config_file)
            raise ConfigFileNotFoundError(self.config_file)

    # support value access
    # get('robot_id'), get('sensors.ir_count'), get('unknown_key', default=0)
    def get(self, key, default=None) -> Any:
        """Safely retrieve configuration value.

        Supports dot notation: get('sensors.ir_count')
        Returns default if key not found.
        """
        current = self.config

        for part in key.split('.'):
            if isinstance(current, dict) and part in current:
                current = current[part]
            else:
                return default
        
        return current
    

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
                raise(ConfigValidationError(errors))
            elif 'capacity' not in battery:
                errors.append("battery capacity is required")
                raise(ConfigValidationError(errors))
            elif not isinstance(battery['capacity'], int):
                errors.append("capacity must be an integer")
                raise(ConfigValidationError(errors))
            elif battery['capacity'] <= 0:
                errors.append("capacity must be greater than zero")
                raise(ConfigValidationError(errors))

            if not isinstance(battery, dict):
                errors.append("battery must be a dictionary")
                raise(ConfigValidationError(errors))
            elif 'current_level' not in battery:
                errors.append("battery current_level is required")
                raise(ConfigValidationError(errors))
            elif not isinstance(battery['current_level'], int):
                errors.append("current_level must be an integer")
                raise(ConfigValidationError(errors))
            elif battery['current_level'] < 0:
                errors.append("current_level must be equal to or greater than zero")
                raise(ConfigValidationError(errors))
            elif battery['current_level'] > battery['capacity']:
                errors.append("current_level must be lower then capacity")
                raise(ConfigValidationError(errors))

        if 'motor' in self.config:
            motor = self.config['motor']

            if not isinstance(motor, dict):
                errors.append("motor must be a dictionary")
                raise(ConfigValidationError(errors))
            elif 'speed' not in motor:
                errors.append("motor speed is required")
                raise(ConfigValidationError(errors))
            elif not isinstance(motor['speed'], int):
                errors.append("speed must be an integer")
                raise(ConfigValidationError(errors))
            elif motor['speed'] < 0:
                errors.append("speed must be equal to or greater than zero")
                raise(ConfigValidationError(errors))

            if not isinstance(motor, dict):
                errors.append("motor must be a dictionary")
                raise(ConfigValidationError(errors))
            elif 'is_running' not in motor:
                errors.append("motor is_running is required")
                raise(ConfigValidationError(errors))
            elif not isinstance(motor['is_running'], bool):
                errors.append("is_running must be a bool")
                raise(ConfigValidationError(errors))

        if errors:
            logger.warning("Validation failed with %d error(s)", len(errors))
            # raise CalibrationValidationError(errors)
        logger.debug("Calibration validation passed")


    # Save() configuration
    # write back to file in detected format, printed nicley for readability
    def save(self, output_file=None):
        """Save current configuration to file."""
        target_file = output_file or self.config_file

        if target_file.lower().endswith(".json"):
            with open(target_file, "w") as file:
                json.dump(self.config, file, indent=4)
                file.write("\n")

        elif target_file.lower().endswith((".yaml", ".yml")):
            with open(target_file, "w") as file:
                yaml.safe_dump(self.config, file, sort_keys=False)

        else:
            raise ValueError(f"Unsupported config format: {target_file}")
        
class GrabberRobot:
    """Focuses only on behavior."""


    def __init__(self, robot_id, capacity, current_level, speed, is_running):
        self.robot_id = robot_id
        self.capacity = capacity
        self.current_level = current_level
        self.speed = speed
        self.is_running = is_running

    def read_capacity(self):
        return self.capacity

    def read_current_level(self):
        return self.current_level

    def read_speed(self):
        return self.speed

    def read_is_running(self):
        return self.is_running

    def read_all(self):
        print("Robot ID: ", self.robot_id, "\n",
          "Capacity: ", self.capacity, "\n",
          "Current Level: ", self.current_level, "\n",
          "Speed: ", self.speed, "\n",
          "Is On: ", self.is_running, "\n")



test_config_manager = ConfigurationManager('example_configs/test_get_config.json')
test_config_manager.validate()
robot = GrabberRobot(
    robot_id=test_config_manager.get('robot_id'),
    capacity=test_config_manager.get('battery.capacity'),
    current_level=test_config_manager.get('battery.current_level'),
    speed=test_config_manager.get('motor.speed'),
    is_running=test_config_manager.get('motor.is_running')
)
print(robot.read_all())

json_config_manager = ConfigurationManager('example_configs/grabber_robot.json')
json_config_manager.validate()
json_config_manager.save()

yaml_config_manager = ConfigurationManager('example_configs/vacume_robot.yaml')
yaml_config_manager.validate()
yaml_config_manager.save()

securityCamera = SecurityCamera("Security Camera")
# print(securityCamera.report_status)

#config.get('batter.capacity')