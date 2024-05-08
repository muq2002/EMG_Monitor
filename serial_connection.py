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

        self.data = {"pressure": [], "flowrate": []}
        self.filtered_data = {"pressure": [], "flowrate": []} 
        self.buffer_data = {"pressure": [], "flowrate": [], "volume": []}

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
        self.data["pressure"].append(json_data.get("pressure", 0))
        self.data["flowrate"].append(json_data.get("flowrate", 0))

        self.buffer_data["pressure"].append(json_data.get("pressure", 0))
        self.buffer_data["flowrate"].append(json_data.get("flowrate", 0))
        
    def filter_data(self):
        window_size = 5
        self.filtered_data["pressure"] = moving_average_filter(self.data["pressure"], window_size)
        self.filtered_data["flowrate"] = moving_average_filter(self.data["flowrate"], window_size)

    def update_plot(self, ax1, ax2, ax3, ax4):

        self.data["pressure"] = self.data["pressure"][-50:]
        self.data["flowrate"] = self.data["flowrate"][-50:]

        self.filtered_data["pressure"] = self.filtered_data["pressure"][-50:]
        self.filtered_data["flowrate"] = self.filtered_data["flowrate"][-50:]

        ax1.clear()
        ax1.plot(self.filtered_data["pressure"])

        ax2.clear()
        ax2.plot(self.filtered_data["flowrate"])

        volume = integrate_discrete_signal(self.filtered_data["flowrate"])

        # if len(volume) > 0:
        #     self.buffer_data["volume"].append(0)
        # else:
        #     self.buffer_data["volume"].append(volume[-1:])
 
        ax3.clear()
        ax3.plot(volume)

        ax4.clear()
        ax4.plot(volume, self.filtered_data["pressure"])

    def get_data(self):
        return self.buffer_data
    
    def close_connection(self):
        if self.serial is not None and self.serial.is_open:
            self.serial.close()
        self.is_connected = False
