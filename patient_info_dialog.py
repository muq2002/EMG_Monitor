import os
import csv
from PyQt5.QtWidgets import QDialog, QGridLayout, QLabel, QLineEdit, QPushButton, QMessageBox
from PyQt5.QtCore import Qt

class PatientInfoDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        # Set window title and modal behavior
        self.setWindowTitle("Patient Information")
        self.setModal(True)

        # Create a grid layout for the input fields
        layout = QGridLayout(self)

        # Create and add input fields for patient information
        # Patient ID
        id_label = QLabel("Patient ID:")
        self.id_input = QLineEdit()
        layout.addWidget(id_label, 0, 0, Qt.AlignRight)
        layout.addWidget(self.id_input, 0, 1)

        # Patient Name
        name_label = QLabel("Patient Name:")
        self.name_input = QLineEdit()
        layout.addWidget(name_label, 1, 0, Qt.AlignRight)
        layout.addWidget(self.name_input, 1, 1)

        # Age
        age_label = QLabel("Age:")
        self.age_input = QLineEdit()
        layout.addWidget(age_label, 2, 0, Qt.AlignRight)
        layout.addWidget(self.age_input, 2, 1)

        # Gender
        gender_label = QLabel("Gender:")
        self.gender_input = QLineEdit()
        layout.addWidget(gender_label, 3, 0, Qt.AlignRight)
        layout.addWidget(self.gender_input, 3, 1)

        # Date of Scan
        date_label = QLabel("Date of Scan:")
        self.date_input = QLineEdit()
        layout.addWidget(date_label, 4, 0, Qt.AlignRight)
        layout.addWidget(self.date_input, 4, 1)

        # Submit button
        submit_button = QPushButton("Submit")
        submit_button.clicked.connect(self.submit_info)
        layout.addWidget(submit_button, 5, 0, 1, 2, Qt.AlignCenter)

    def submit_info(self):
        patient_info = {
            "id": self.id_input.text(),
            "name": self.name_input.text(),
            "age": self.age_input.text(),
            "gender": self.gender_input.text(),
            "date": self.date_input.text(),
        }

        if not all(patient_info.values()):
            QMessageBox.warning(self, "Input Error", "All fields are required.")
            return

        # Create folder using the patient's name
        folder_path = os.path.join(os.getcwd(), "data/" + patient_info["name"])
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

        csv_filename = os.path.join(folder_path, f"patient_info.csv")
        try:
            with open(csv_filename, 'w', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(["ID", "Name", "Age", "Gender", "Date of Scan"])
                writer.writerow([patient_info["id"], patient_info["name"], patient_info["age"], patient_info["gender"], patient_info["date"]])


            QMessageBox.information(self, "Success", f"Patient information exported to {csv_filename}.")
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Failed to export patient information: {e}")

        self.accept()

        # Pass the patient info to the parent
        self.parent().patient_info = patient_info
        self.parent().folder_path = folder_path
