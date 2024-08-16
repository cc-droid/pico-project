# model/model.py
import random

class DataModel:
    def __init__(self):
        self.state = "OFF"
        self.random_value = 0

    def toggle_led(self, status):
        self.state = status

    def fetch_random_value(self):
        self.random_value = random.randint(0, 20)
        return self.random_value