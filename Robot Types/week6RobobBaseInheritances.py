from abc import ABC, abstractmethod
from battery import Battery
from sensor import Sensor
from motor import Motor

class RobotBase(ABC):
    """Provide shared components and behavior for robot types."""

    def __init__(self, name):
        """Initialize a robot with its default components.

        Args:
            name: Name used to identify the robot.
        """
        self._name = name
        self._battery = Battery(100, 50)
        self._motor = Motor(1, True)
        self._sensor = Sensor("object")

    @property
    def name(self):
        """Return the robot's name.

        Returns:
            The robot name.
        """
        return self._name

    def report_status(self):
        """Report the robot's current status.

        Returns:
            ``None`` in the base implementation.
        """
        return

    def __str__(self):
        """Return a compact string containing the robot's status."""
        return (f"RobotBase {self._name!r} {self._battery.current_level} {self._battery.charge()} "
                f"{self._battery.get_percentage()} {self._battery.is_depleted()}"
                f"{self._motor._speed!r} {self._motor.is_running!r}"
                f"{self._sensor.read_data()!r} {self._sensor.detect_obstacle()!r} {self._sensor.get_reading()!r}\n")

    def __repr__(self):
        """Return a detailed string representation of the robot."""
        return (f"Robot Name: {self._name!r}\n"
                "Battery: \n"
                f"Battery Level: {self._battery.current_level}\n"                
                f"Battery Charge: {self._battery.charge()}\n"
                f"Battery Persentage: {self._battery.get_percentage()}\n"                
                f"Battery depleted: {self._battery.is_depleted()}\n"  

                "\nMotor: \n"
                f"Speed: {self._motor._speed!r}\n"
                f"Is Moving: {self._motor.is_running!r}\n"

                "\nSensor: \n"
                f"Sensor Read Data: {self._sensor.read_data()!r}\n"
                f"Sensor Detect Obstacle: {self._sensor.detect_obstacle()!r}\n"
                f"Sensor Get Reading: {self._sensor.get_reading()!r}\n")


class Vacume(RobotBase):
    """Represent a robot that can vacuum."""

    def __init__(self, name, sucking):
        """Initialize a vacuum robot.

        Args:
            name: Name used to identify the robot.
            sucking: Whether the vacuum is currently sucking.
        """
        super().__init__(name)
        self._battery = Battery(100, 50)
        self._motor = Motor(20, True)
        self._sensor = Sensor("object")
        self.sucking = sucking

    def vacuming(self, vacuming):
        """Set the vacuuming state when vacuuming is requested.

        Args:
            vacuming: Whether vacuuming should be active.
        """
        if vacuming == True:
            self.sucking == True

class SecurityCamera(RobotBase):
    """Represent a stationary robot with a security camera sensor."""

    def __init__(self, name):
        """Initialize a security camera robot.

        Args:
            name: Name used to identify the robot.
        """
        super().__init__(name)
        self._battery = Battery(100, 100)
        self._motor = Motor(0, False)
        self._sensor = Sensor("object")

class PickupAndPutdown(RobotBase):
    """Represent a robot that can pick up and put down objects."""

    def __init__(self, name, is_holding):
        """Initialize a pickup-and-putdown robot.

        Args:
            name: Name used to identify the robot.
            is_holding: Whether the robot is currently holding an item.
        """
        super().__init__(name)
        self._battery = Battery(100, 40)
        self._motor = Motor(10, True)
        self._sensor = Sensor("object")
        self.is_holding = is_holding

    def grabber(self, grabbing_item):
        """Set the holding state when an item is grabbed.

        Args:
            grabbing_item: Whether the robot is grabbing an item.
        """
        if grabbing_item == True:
            self.is_holding == True
        

    
vacume = Vacume("Vacume", True)
securityCamera = SecurityCamera("Security Camera")
pickupAndPutDown = PickupAndPutdown("Pickup & Putdown", True)

print(vacume.report_status)
print(securityCamera.report_status)
print(pickupAndPutDown.report_status)
