from sensor import Sensor
from display import Display
from pathlib import Path
from datetime import datetime
import json


class CarPark:
    def __init__(
        self,
        location,
        capacity,
        log_file="log.txt",
        plates=None,
        sensors=None,
        displays=None,
    ):
        self.location = location
        self.capacity = capacity
        self.plates = plates or []
        self.sensors = sensors or []
        self.displays = displays or []
        self.log_file = Path(log_file)
        if not self.log_file.exists():
        # self.log_file = log_file if isinstance(log_file, Path) else Path(log_file)
        # create the file if it doesn't exist
            self.log_file.touch()

    @property
    # decorator, which allows a methods to act like an attribute
    def available_bays(self):
        # car_park.available_bays
        return max(0, self.capacity - len(self.plates))

    def register(self, component):
        """Registers component of a car park"""
        # if  it's not either a Sensor or a Display, throw an error
        if not isinstance(component, (Sensor, Display)):
            raise TypeError("Invalid component type!")

        # otherwise if it's a Sensor, append to Sensors
        if isinstance(component, Sensor):
            self.sensors.append(component)
        # else, it's a Display, append to Displays
        elif isinstance(component, Display):
            self.displays.append(component)

    def add_car(self, plate):
        self.plates.append(plate)
        self.update_displays()
        self._log_car_activity(plate, "entered")

    def remove_car(self, plate):
        self.plates.remove(plate)
        self.update_displays()
        self._log_car_activity(plate, "exited")

    def update_displays(self):
        for display in self.displays:
            display.update({"Bays": self.available_bays, "Temperature": 42})
            print(f"Updating: {display}")

    # in CarPark class
    def _log_car_activity(self, plate, action):
        with self.log_file.open(mode="a") as f:
            f.write(f"{plate} {action} at {datetime.now():%Y-%m-%d %H:%M:%S}\n")

    def __str__(self):
        return f"Welcome to car park at {self.location}, with {self.capacity} bays."
        # def __str__ returns a string containing the car park's location and capacity
