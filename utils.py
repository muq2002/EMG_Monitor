from PyQt5.QtWidgets import QComboBox

def get_ports():
    ports = [f"COM{x}" for x in range(1, 10)]
    port_combo = QComboBox()
    port_combo.addItems(ports)
    return port_combo

def get_baudrates():
    baudrates = ["9600", "19200", "38400", "57600", "115200"]
    baudrate_combo = QComboBox()
    baudrate_combo.addItems(baudrates)
    return baudrate_combo
