from PyQt5.QtWidgets import QFileDialog, QMainWindow, QVBoxLayout, QHBoxLayout, QPushButton, QWidget, QSizePolicy, QMessageBox, QComboBox
from PyQt5.QtCore import QTimer
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from utils import get_ports, get_baudrates
from serial_connection import SerialConnection
from exporter import Exporter
from patient_info_dialog import PatientInfoDialog
from csv_reader import read_csv_and_plot
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas


class SerialPlotter(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Spirometer XL VER. 1.0")
        self.setGeometry(100, 100, 1000, 900)

        main_widget = QWidget()
        self.setCentralWidget(main_widget)

        main_layout = QVBoxLayout(main_widget)
        self.figure, ((self.ax1, self.ax2), (self.ax3, self.ax4)) = plt.subplots(2, 2)
        self.canvas = FigureCanvas(self.figure)
        
        main_layout.addWidget(self.canvas)

        controls_layout = QHBoxLayout()

        self.port_combo = get_ports()
        self.baudrate_combo = get_baudrates()

        # Create the buttons
        self.connect_button = QPushButton("Connect")
        self.connect_button.clicked.connect(self.connect_serial)
        

        # Button to read CSV file
        self.read_csv_button = QPushButton("Open ...")
        self.read_csv_button.clicked.connect(self.read_csv)
        controls_layout.addWidget(self.read_csv_button)

        # Add the controls to the controls layout
        controls_layout.addWidget(self.port_combo)
        controls_layout.addWidget(self.baudrate_combo)
        controls_layout.addWidget(self.connect_button)

        self.export_start_button = QPushButton("Export")
        self.export_start_button.clicked.connect(self.start_export)
        self.export_start_button.setEnabled(True)
        controls_layout.addWidget(self.export_start_button)


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
            self.connect_button.setText("Connect")
            self.export_start_button.setEnabled(True)
        else:
            # Connect to the serial port
            port = self.port_combo.currentText()
            baudrate = int(self.baudrate_combo.currentText())
            try:
                self.serial_connection.connect(port, baudrate)
                if self.serial_connection.is_connected:
                    self.connect_button.setText("Disconnect")
                    self.export_start_button.setEnabled(False)
                    self.serial_connection.start_reading(self.update_data)
                else:
                    QMessageBox.warning(self, "Connection Error", "Failed to connect to the serial port.")
            except Exception as e:
                QMessageBox.warning(self, "Error", f"An error occurred while connecting: {e}")


    def update_data(self, values):
        self.serial_connection.append_data(values)

    def update_plot(self, frame):
        self.ax1.clear()
        self.ax2.clear()
        self.ax3.clear()
        self.ax4.clear()

        # Update each plot with its respective data
        self.serial_connection.update_plot(self.ax1, self.ax2, self.ax3, self.ax4)

        # Set labels for each subplot
        self.ax1.set_title("Differential Pressure")
        self.ax1.set_xlabel("Time (sec)")
        self.ax1.set_ylabel("Pressure (Kpa)")

        self.ax2.set_title("Flow Rate")
        self.ax2.set_xlabel("Time")
        self.ax2.set_ylabel("Flow rate")
        
        self.ax3.set_title("Volume")
        self.ax3.set_xlabel("Time")
        self.ax3.set_ylabel("Volume")
        
        self.ax4.set_title("Volume vs. Flow rate")
        self.ax4.set_xlabel("Volume")
        self.ax4.set_ylabel("Flow rate")

    def start_export(self):
        dialog = PatientInfoDialog(self)
        if dialog.exec_():
            self.exporter.export_data(self.folder_path,  self.serial_connection.get_data())

    def closeEvent(self, event):
        self.serial_connection.close_connection()
        event.accept()
