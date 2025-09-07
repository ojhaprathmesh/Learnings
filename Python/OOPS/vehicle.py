class Vehicle:
    def __init__(self, name: str, speed: int):
        self.name = name
        self.speed = speed

    def describe(self):
        print(f"This is a {self.name} moving at {self.speed} km/h.")

class Car(Vehicle):
    def __init__(self, name: str, speed: int, num_doors: int):
        super().__init__(name, speed)
        self.num_doors = num_doors

    def describe(self):
        print(f"This is a {self.name} moving at {self.speed} km/h and has {self.num_doors} doors.")

class Bike(Vehicle):
    def __init__(self, name: str, speed: int, engine_type: str):
        super().__init__(name, speed)
        self.engine_type = engine_type

    def describe(self):
        print(f"This is a {self.name} moving at {self.speed} km/h and has a {self.engine_type} engine.")

honda_civic = Car("Honda Civic", 180, 4)
honda_civic.describe()

yamaha_r1 = Bike("Yamaha R1", 299, "inline-four")
yamaha_r1.describe()