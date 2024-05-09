from PyQt5.QtWidgets import QFileDialog, QMessageBox
import csv
import numpy as np

class Exporter:
    def __init__(self, window):
        self.window = window

    def export_data(self, folder_path, data):
        if not data:
            QMessageBox.warning(self.window, "No Data", "No data to export.")
            return
        
        filename = folder_path + "/data.csv"
        if not all(key in data for key in ['emg']):
            QMessageBox.warning(self.window, "Data Error", "Data format is incorrect.")
            return

        # Export data to a CSV file
        with open(filename, "w", newline="") as csvfile:
            csv_writer = csv.writer(csvfile)

            csv_writer.writerow(["emg"])
            min_length = min(len(data["emg"]), len(data["emg"]))
            for i in range(min_length):
                csv_writer.writerow([data["emg"][i], data["emg"][i]])

        QMessageBox.information(self.window, "Export Complete", f"Data has been exported to {filename}.")
