import serial
import json
from threading import Thread
import numpy as np
from filters import moving_average_filter, integrate_discrete_signal
import matplotlib.pyplot as plt

class SerialConnection:
    def __init__(self):
        self.serial = None
        self.is_connected = False

        # Changed data structure to handle only EMG data
        self.data = {"emg": []}
        self.filtered_data = {"emg": []}
        self.buffer_data = {"emg": []}

    def connect(self, port, baudrate):
        if self.serial is None or not self.serial.is_open:
            try:
                self.serial = serial.Serial(port, baudrate, timeout=1)
                self.is_connected = True
            except serial.SerialException as e:
                print(f"Error opening serial port: {e}")

    def start_reading(self, update_data):
        def read_serial():
            while self.is_connected:
                data = self.serial.readline().decode().strip()
                if data:
                    try:
                        json_data = json.loads(data)
                        self.append_data(json_data)
                        self.filter_data()
                        update_data(json_data)
                    except (ValueError, json.JSONDecodeError):
                        pass
        
        self.thread = Thread(target=read_serial)
        self.thread.start()

    def append_data(self, json_data):
        self.data["emg"].append(json_data.get("emg", 0))
        self.buffer_data["emg"].append(json_data.get("emg", 0))

    def filter_data(self):
        window_size = 5
        self.filtered_data["emg"] = moving_average_filter(self.data["emg"], window_size)

    def update_plot(self, ax1):

        self.data["emg"] = self.data["emg"][-50:]
        self.filtered_data["emg"] = self.filtered_data["emg"][-50:]

        ax1.clear()
        ax1.plot(self.filtered_data["emg"], color='red', linestyle='-', linewidth=2)

    def get_data(self):
        # Return buffer data containing EMG data
        return self.buffer_data
    
    def close_connection(self):
        if self.serial is not None and self.serial.is_open:
            self.serial.close()
        self.is_connected = False
