from time import sleep
from typing import Any, List

from pythonosc.dispatcher import Dispatcher


class OSCMessageReceiver:
    def __init__(self):
        self.values = None
        self.dispatcher = Dispatcher()

        # Map commands to the set_filter method
        self.dispatcher.map("/location", self.handle_location)
        self.dispatcher.map("/rotation", self.handle_rotation)
        self.dispatcher.map("/project", self.handle_project)
        self.dispatcher.set_default_handler(self.handle_invalid_command)

    def handle_location(
        self, address: str, *args: List[Any]
    ) -> tuple[float, float, float]:
        # Logic to handle location path

        # This check is necessary
        if address == "/location":
            # Split the string argument into three float values
            values = args[0].split(",")
            x, y, z = map(float, values)
            self.values = x, y, z
            return self.values

    def handle_rotation(
        self, address: str, *args: List[Any]
    ) -> tuple[float, float, float]:
        if address == "/rotation":
            values = args[0].split(",")
            roll, pitch, yaw = map(float, values)
            self.values = roll, pitch, yaw
            return self.values

    def handle_project(self, address: str, *args: List[Any]) -> str:
        if address == "/project":
            # Logic to handle the project path
            if not len(args) == 1 or type(args[0]) is not str:
                return
            self.values = args[0]
            return self.values

    def handle_invalid_command(self, address, *args) -> None:
        # Logic to handle invalid commands with an exception.
        print(f"Invalid command: {address}")
        raise Exception(f"Invalid command: {address}")

    def wait_for_response(self) -> object:
        """We wait for values to get assigned and then reset values to None for next check."""
        while not self.values:
            sleep(0.01)
        response = self.values
        self.values = None
        return response