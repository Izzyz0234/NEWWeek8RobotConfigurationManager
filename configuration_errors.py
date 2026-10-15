class ConfigError(Exception):
    """Base exception for all calibration errors.

    All CalibrationReader exceptions inherit from this,
    allowing callers to catch broadly or specifically.
    """
    pass

class ConfigFileNotFoundError(ConfigError):
    """Raised when the calibration file cannot be found.

    Args:
        file_path: The path that was searched.
    """
    def __init__(self, file_path: str):
        self.file_path = file_path
        super().__init__(f"Calibration file not found: {file_path}")


class ConfigParseError(ConfigError):
    """Raised when a calibration file exists but cannot be parsed.

    Args:
        file_path: The file that failed to parse.
        reason: Human-readable description of the parse failure.
    """
    def __init__(self, file_path: str, reason: str):
        self.file_path = file_path
        self.reason = reason
        super().__init__(f"Failed to parse '{file_path}': {reason}")


class ConfigValidationError(ConfigError):
    """Raised when calibration data fails validation checks.

    Args:
        errors: List of validation error messages.
    """
    def __init__(self, errors: list):
        self.errors = errors
        error_list = "\n  - ".join(errors)
        super().__init__(f"Calibration validation failed:\n  - {error_list}")
