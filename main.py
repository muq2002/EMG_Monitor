import sys
from PyQt5.QtWidgets import QApplication
from serial_plotter import SerialPlotter

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SerialPlotter()
    window.show()
    sys.exit(app.exec_())
