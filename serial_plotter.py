from PyQt5.QtWidgets import QFileDialog, QMainWindow, QVBoxLayout, QHBoxLayout, QPushButton, QWidget, QSizePolicy, QMessageBox, QComboBox, QLabel
from PyQt5.QtCore import QTimer, Qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from utils import get_ports, get_baudrates
from serial_connection import SerialConnection
from exporter import Exporter
from patient_info_dialog import PatientInfoDialog
from csv_reader import read_csv_and_plot
from choose_port_baudrate import PortBaudrateDialog

class SerialPlotter(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("EMG Monitor XL VER. 1.0")
        self.setGeometry(100, 100, 1000, 900)

        # Create main widget and layout
        main_widget = QWidget()
        self.setCentralWidget(main_widget)

        main_layout = QVBoxLayout(main_widget)

        # Create figure and canvas for the plot
        self.figure, self.ax = plt.subplots()
        self.canvas = FigureCanvas(self.figure)
        main_layout.addWidget(self.canvas)

        # Create layout for RMS and fatigue labels
        labels_layout = QHBoxLayout()

        # Create the RMS label
        self.rms_label = QLabel("RMS: 0")
        self.rms_label.setStyleSheet("font-size: 40px; color: blue;") 
        labels_layout.addWidget(self.rms_label)
        labels_layout.setAlignment(self.rms_label, Qt.AlignCenter)

        # Create the fatigue label
        self.fatigue_label = QLabel("Fatigue: Normal")
        self.fatigue_label.setStyleSheet("font-size: 40px; color: red;")
        labels_layout.addWidget(self.fatigue_label)
        labels_layout.setAlignment(self.fatigue_label, Qt.AlignCenter)

        # Add labels layout to main layout
        main_layout.addLayout(labels_layout)

        # Create controls layout
        controls_layout = QHBoxLayout()
        self.port_combo = QComboBox()
        self.baudrate_combo = QComboBox()

        self.port_baudrate_button = QPushButton("Config")
        self.port_baudrate_button.clicked.connect(self.show_port_baudrate_dialog)
        controls_layout.addWidget(self.port_baudrate_button)

        self.connect_button = QPushButton("Collect")
        self.connect_button.clicked.connect(self.connect_serial)
        controls_layout.addWidget(self.connect_button)

        self.export_start_button = QPushButton("Export")
        self.export_start_button.clicked.connect(self.start_export)
        self.export_start_button.setEnabled(True)
        controls_layout.addWidget(self.export_start_button)

        # Add controls layout to main layout
        main_layout.addLayout(controls_layout)

        self.serial_connection = SerialConnection()
        self.exporter = Exporter(self)

        # Create an animation for updating the plots
        self.animation = FuncAnimation(self.figure, self.update_plot, interval=100)

    def read_csv(self):
        filename, _ = QFileDialog.getOpenFileName(
            self, "Open CSV File", "", "CSV Files (*.csv)"
        )
        if filename:
            read_csv_and_plot(filename, self.figure)

    def connect_serial(self):
        if self.serial_connection.is_connected:
            # Disconnect the serial connection
            self.serial_connection.close_connection()
            self.connect_button.setText("Collect")
            self.export_start_button.setEnabled(True)
        else:
            # Connect to the serial port
            dialog = PortBaudrateDialog(self)
            if dialog.exec_():  # Show the dialog and check if the user confirmed their selection
                port, baudrate = dialog.get_selected_port_and_baudrate()
                try:
                    self.serial_connection.connect(port, baudrate)
                    if self.serial_connection.is_connected:
                        self.connect_button.setText("Stop")
                        self.export_start_button.setEnabled(False)
                        self.serial_connection.start_reading(self.update_data)
                    else:
                        QMessageBox.warning(self, "Connection Error", "Failed to connect to the serial port.")
                except Exception as e:
                    QMessageBox.warning(self, "Error", f"An error occurred while connecting: {e}")

    def update_data(self, values):
        # Append data and update labels
        self.serial_connection.append_data(values)

        # Calculate RMS and fatigue status (adjust calculations as needed)
        emg_values = values.get('emg_values', [])
        rms_value = self.calculate_rms(emg_values)
        fatigue_status = self.determine_fatigue(rms_value)

        # Update RMS label text
        self.rms_label.setText(f"RMS: {rms_value:.2f}")

        # Update fatigue label text
        self.fatigue_label.setText(f"Fatigue: {fatigue_status}")

    def calculate_rms(self, values):
        # Calculate the RMS value from EMG values
        import numpy as np
        if not values:
            return 0
        squared_values = np.square(values)
        mean_squared = np.mean(squared_values)
        rms = np.sqrt(mean_squared)
        return rms

    def determine_fatigue(self, rms_value):
        # Define RMS thresholds for fatigue status (adjust as needed)
        if rms_value < 10:
            return "Normal"
        elif rms_value < 20:
            return "Moderate"
        else:
            return "High"

    def update_plot(self, frame):
        self.ax.clear()

        # Update the plot with EMG data
        self.serial_connection.update_plot(self.ax)
       

        # Set title and labels for the plot
        self.ax.set_title("EMG Data")
        self.ax.set_xlabel("Time")
        self.ax.set_ylabel("Amplitude")

        # Redraw the canvas to display the updated plot
        self.canvas.draw()

    def show_port_baudrate_dialog(self):
        dialog = PortBaudrateDialog(self)
        if dialog.exec_():  # Show the dialog and check if the user confirmed their selection
            port, baudrate = dialog.get_selected_port_and_baudrate()
            try:
                self.serial_connection.connect(port, baudrate)
                if self.serial_connection.is_connected:
                    self.connect_button.setText("Stop")
                    self.export_start_button.setEnabled(False)
                    self.serial_connection.start_reading(self.update_data)
                else:
                    QMessageBox.warning(self, "Connection Error", "Failed to connect to the serial port.")
            except Exception as e:
                QMessageBox.warning(self, "Error", f"An error occurred while connecting: {e}")

    def start_export(self):
        dialog = PatientInfoDialog(self)
        if dialog.exec_():
            self.exporter.export_data(self.folder_path, self.serial_connection.get_data())

    def closeEvent(self, event):
        self.serial_connection.close_connection()
        event.accept()
