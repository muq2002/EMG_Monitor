from PyQt5.QtWidgets import QFileDialog, QMainWindow, QVBoxLayout, QHBoxLayout, QPushButton, QWidget, QSizePolicy, QMessageBox, QComboBox, QLabel
from PyQt5.QtCore import QTimer, Qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from serial_connection import SerialConnection
from exporter import Exporter
from patient_info_dialog import PatientInfoDialog
from csv_reader import read_csv_and_plot
from choose_port_baudrate import PortBaudrateDialog
from utils import apply_dark_mode_to_plot, apply_dark_mode_to_pyqt
from models_load import calculate_rms, determine_fatigue, calculate_zero_crossing  # Import functions

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
        
        apply_dark_mode_to_plot(self.figure, self.ax)
        apply_dark_mode_to_pyqt(self)

        # Create layout for RMS, fatigue, and zero-crossing labels
        labels_layout = QHBoxLayout()

        # RMS label
        self.rms_label = QLabel("RMS: 0")
        self.rms_label.setStyleSheet("font-size: 40px; color: blue;") 
        labels_layout.addWidget(self.rms_label)
        labels_layout.setAlignment(self.rms_label, Qt.AlignCenter)
        # Zero-crossing label
        self.zero_crossing_label = QLabel("Zero-Crossing: 0")
        self.zero_crossing_label.setStyleSheet("font-size: 40px; color: green;")
        labels_layout.addWidget(self.zero_crossing_label)
        labels_layout.setAlignment(self.zero_crossing_label, Qt.AlignCenter)

        # Fatigue label
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
            if dialog.exec_():
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
        self.serial_connection.append_data(values)


        rms_value = calculate_rms(self.serial_connection.buffer_data['emg'])
        zero_crossing_count = calculate_zero_crossing(self.serial_connection.buffer_data['emg'])

        fatigue_status = "Normal" # determine_fatigue(rms_value, zero_crossing_count)


        # Update labels
        self.rms_label.setText(f"RMS: {rms_value:.2f}")
        self.zero_crossing_label.setText(f"Zero-Crossing: {zero_crossing_count}")
        self.fatigue_label.setText(f"Fatigue: {fatigue_status}")

    def update_plot(self, frame):
        self.ax.clear()
        # Update the plot with EMG data
        self.serial_connection.update_plot(self.ax)
        # Set title and labels for the plot
        self.ax.set_title("EMG Data")
        self.ax.set_xlabel("Time")
        self.ax.set_ylabel("Amplitude")
        self.ax.grid(which='both', color='gray', linestyle='--', linewidth=0.5)
        # Redraw the canvas to display the updated plot
        self.canvas.draw()

    def show_port_baudrate_dialog(self):
        dialog = PortBaudrateDialog(self)
        if dialog.exec_():
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
