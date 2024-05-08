import sys
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QVBoxLayout,
    QComboBox,
    QFileDialog,
    QPushButton,
    QWidget,
    QSizePolicy,
    QMessageBox,
)
from PyQt5.QtCore import QTimer
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import serial
from threading import Thread
import csv
import numpy as np


class SerialPlotter(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Serial Plotter")
        self.setGeometry(100, 100, 1000, 900)

        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QVBoxLayout(main_widget)

        self.port_combo = QComboBox()
        self.baudrate_combo = QComboBox()

        self.connect_button = QPushButton("Connect")
        self.connect_button.clicked.connect(self.connect_serial)

        self.export_start_button = QPushButton("Start Export")
        self.export_start_button.clicked.connect(self.start_export)

        layout.addWidget(self.port_combo)
        layout.addWidget(self.baudrate_combo)
        layout.addWidget(self.connect_button)
        layout.addWidget(self.export_start_button)

        self.figure, self.ax = plt.subplots()
        self.canvas = FigureCanvas(self.figure)
        layout.addWidget(self.canvas)

        self.serial = None
        self.is_running = False

        self.buffer_data = []
        self.x_data = []
        self.y_data = []

        self.exporting = False
        self.export_timer = QTimer()
        self.export_timer.timeout.connect(self.export_data)

        self.populate_ports()
        self.populate_baudrates()

        self.animation = FuncAnimation(self.figure, self.update_plot, interval=100)

    def populate_ports(self):
        ports = [f"COM{x}" for x in range(1, 10)]
        self.port_combo.addItems(ports)

    def populate_baudrates(self):
        baudrates = ["9600", "19200", "38400", "57600", "115200"]
        self.baudrate_combo.addItems(baudrates)

    def connect_serial(self):
        port = self.port_combo.currentText()
        baudrate = int(self.baudrate_combo.currentText())

        if self.serial is None or not self.serial.is_open:
            try:
                self.serial = serial.Serial(port, baudrate, timeout=1)
                self.is_running = True
                Thread(target=self.read_serial).start()
                self.connect_button.setText("Disconnect")
                self.export_start_button.setEnabled(True)
            except serial.SerialException as e:
                print(f"Error opening serial port: {e}")
        else:
            self.serial.close()
            self.is_running = False
            self.connect_button.setText("Connect")
            self.export_start_button.setEnabled(False)

    def read_serial(self):
        while self.is_running:
            data = self.serial.readline().decode().strip()
            if data:
                try:
                    value = float(data)
                    self.update_data(value)
                except ValueError:
                    pass

    def update_data(self, value):
        self.x_data.append(len(self.x_data) + 1)

        self.buffer_data.append(value)
        self.y_data.append(value)

    def update_plot(self, frame):

        self.y_data = self.y_data[-50:]

        self.ax.clear()
        self.ax.plot(self.y_data)
        self.ax.set_xlabel("Time")
        self.ax.set_ylabel("Value")

    def start_export(self):
        if not self.exporting:
            self.exporting = True
            self.export_start_button.setEnabled(False)
            self.export_data()
        else:
            QMessageBox.warning(
                self, "Export Already Started", "Export has already been started."
            )

    def export_data(self):
        filename, _ = QFileDialog.getSaveFileName(
            self, "Save Data", "", "CSV Files (*.csv)"
        )
        if filename:
            with open(filename, "w", newline="") as csvfile:
                csv_writer = csv.writer(csvfile)
                csv_writer.writerow(["Value"])
                csv_writer.writerow(np.transpose(np.array(self.buffer_data)))
            QMessageBox.information(
                self, "Export Complete", f"Data has been exported to {filename}."
            )

    def closeEvent(self, event):
        if self.serial is not None and self.serial.is_open:
            self.serial.close()
        event.accept()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SerialPlotter()
    window.show()
    sys.exit(app.exec_())
