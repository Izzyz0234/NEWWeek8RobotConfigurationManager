from typing import Dict, Optional, Any
from configuration_errors import ConfigFileNotFoundError, ConfigParseError, ConfigValidationError
from example_configs.robot_types.week6RobobBaseInheritances import RobotBase, SecurityCamera
import os, logging, json, yaml

logger = logging.getLogger(__name__)


class ConfigurationManager:

    def __init__(self, config_file: str) -> None:
        """Initialize with configuration file path."""
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
        with open(config_file) as f:
            config = json.load(f)
        self.name = config['name']
        self.ir_sensors = config['ir_count']

        if not os.path.exists(self.config_file):
            logger.error("Config file not found: %s", self.config_file)
            raise ConfigFileNotFoundError(self.config_file)

        try:
            with open(self.config_file, 'r') as f:
                self.config = self._parse_file(f)
            logger.info("Loaded config: %s", self.config_file)
        except (json.JSONDecodeError, ValueError) as e:
            logger.error("Parse error in '%s': %s", self.config_file, e)
            raise ConfigParseError(self.config_file, str(e)) from e

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
    def validate(self) -> list:
        """Validate configuration. Returns list of error strings."""



    # Save() configuration
    # write back to file in detected format, printed nicley for readability

config_manager = ConfigurationManager('robot_config.json')
config_manager.validate()

securityCamera = SecurityCamera("Security Camera")
print(securityCamera.report_status)
