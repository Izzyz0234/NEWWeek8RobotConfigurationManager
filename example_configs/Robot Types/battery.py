class Battery():
    """Represent a robot battery and its charge level."""

    def __init__(self, capacity, current_level):
        """Initialize a battery.

        Args:
            capacity: Maximum charge level of the battery.
            current_level: Charge level currently stored in the battery.
        """
        self._capacity = capacity
        self._current_level = current_level

    @property
    def current_level(self):
        """Get battery level."""
        return self._current_level

    @current_level.setter
    def current_level(self, value):
        """Set battery level with validation.

        Args:
            value: New battery level percentage (float, 0-100)
        Raises:
            ValueError: If battery level is not in valid range
        """
        if not (0 <= value <= 100):
            raise ValueError("Battery level must be between 0 and 100")
        self._current_level = value

    def drain(self, amount):
        """Remove charge from the battery.

        Args:
            amount: Amount of charge to remove.
        Raises:
            ValueError: If the amount is greater than the current charge.
        """
        if self._current_level < amount:
            raise ValueError("Battery drain level must be lower or equal to current level")
        self.current_level = self.current_level - amount

    def charge(self):
        """Report whether the battery is fully charged.

        Returns:
            A message indicating whether the battery is fully charged.
        """
        if self.current_level == self._capacity:
            return (f"Battery level is charged")
        else:
            return (f"Battery level is not charged")

    def get_percentage(self):
        """Calculate the battery charge as a fraction of its capacity.

        Returns:
            The current charge fraction formatted as a string.
        """
        return (f"{self.current_level / self._capacity}")

    def is_depleted(self):
        """Report whether the battery has no charge remaining.

        Returns:
            A message indicating whether the battery is depleted.
        """
        if self._current_level == 0:
            return (f"Battery level is depleted")
        else:
            return (f"Battery level is not depleted")
        
        
#drain(amount)
#charge()
#get_percentage()
#is_depleted()