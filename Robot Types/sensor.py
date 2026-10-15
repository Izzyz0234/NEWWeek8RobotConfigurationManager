class Sensor():
    """Represent a sensor that gathers environmental information."""

    def __init__(self, sensor_type):
        """Initialize a sensor.

        Args:
            sensor_type: Type of information detected by the sensor.
        """
        self._sensor_type = sensor_type

    def read_data(self):
        """Read environmental data from the sensor.

        Returns:
            Sensor data. The base implementation returns ``None``.
        """
        pass
    
    def detect_obstacle(self):
        """Detect whether an obstacle is present.

        Returns:
            Obstacle information. The base implementation returns ``None``.
        """
        pass
    
    def get_reading(self):
        """Get the current sensor reading.

        Returns:
            The sensor reading. The base implementation returns ``None``.
        """
        pass


#read_data()
#detect_obstacle()
#get_reading()