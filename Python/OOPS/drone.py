class Drone:
    def __init__(self, model_name: str, battery_life: int, max_altitude: int):
        self.model_name = model_name
        self.battery_life = battery_life
        self.max_altitude = max_altitude

    def get_specs(self):
        return f"Model: {self.model_name}\nBattery Life: {self.battery_life} hours\nMax Altitude: {self.max_altitude} meters"

drone = Drone("Phantom 4", 30, 500)
print(drone.get_specs())