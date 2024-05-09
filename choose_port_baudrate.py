from PyQt5.QtWidgets import QComboBox, QDialog, QVBoxLayout, QPushButton, QLabel, QHBoxLayout
from utils import get_ports, get_baudrates

class PortBaudrateDialog(QDialog):
    """Dialog for selecting serial port and baud rate."""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Select Port and Baud Rate")
        
        layout = QVBoxLayout()
        
        # Create and populate the port combo box
        self.port_combo = QComboBox()
        # Ensure get_ports() returns a list of strings
        ports = get_ports()
        self.port_combo.addItems(ports)
        layout.addWidget(QLabel("Port:"))
        layout.addWidget(self.port_combo)
        
        # Create and populate the baud rate combo box
        self.baudrate_combo = QComboBox()
        # Ensure get_baudrates() returns a list of strings
        baudrates = get_baudrates()
        self.baudrate_combo.addItems(baudrates)
        layout.addWidget(QLabel("Baud Rate:"))
        layout.addWidget(self.baudrate_combo)
        
        # Buttons for confirm and cancel actions
        button_layout = QHBoxLayout()
        self.confirm_button = QPushButton("Confirm")
        self.confirm_button.clicked.connect(self.accept)
        button_layout.addWidget(self.confirm_button)
        
        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(self.cancel_button)
        
        layout.addLayout(button_layout)
        
        self.setLayout(layout)
        
    def get_selected_port_and_baudrate(self):
        port = self.port_combo.currentText()
        baudrate = int(self.baudrate_combo.currentText())
        return port, baudrate
