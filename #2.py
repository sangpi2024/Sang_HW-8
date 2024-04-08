from pyXsteam.XSteam import XSteam

class rankineModel:
    """
    Model for Rankine cycle calculations.
    Handles the thermodynamic calculations using pyXsteam.
    """

    def __init__(self):
        self.steam_table = XSteam(XSteam.UNIT_SYSTEM_MKS)  # Initialize steam table with SI units

    def get_saturation_temperature(self, pressure):
        """Returns the saturation temperature for a given pressure."""
        return self.steam_table.tsat_p(pressure)

    # Add more methods as needed for different thermodynamic properties


from PyQt5.QtWidgets import QApplication, QMainWindow, QLineEdit, QLabel, QRadioButton


class rankineView(QMainWindow):
    """
    View for the Rankine cycle application.
    Contains the UI components.
    """

    def __init__(self):
        super().__init__()
        # UI components setup
        self.lineEdit_P_High = QLineEdit(self)
        self.label_T_Sat = QLabel("Saturation Temperature:", self)
        self.radio_T_High = QRadioButton("T High", self)
        self.radio_SI = QRadioButton("SI Units", self)
        self.radio_English = QRadioButton("English Units", self)

        # Positioning elements (simplified)
        self.lineEdit_P_High.move(10, 10)
        self.label_T_Sat.move(10, 40)
        self.radio_T_High.move(10, 70)
        self.radio_SI.move(10, 100)
        self.radio_English.move(10, 130)

        # Set default states
        self.radio_SI.setChecked(True)

        # More setup as needed...

    # Additional methods to update UI components


class rankineController:
    """
    Controller for Rankine cycle application.
    Interacts with both the model and the view.
    """

    def __init__(self, model, view):
        self.model = model
        self.view = view
        # Connect signals and slots
        self.view.radio_T_High.clicked.connect(self.update_T_High)
        self.view.lineEdit_P_High.editingFinished.connect(self.update_Properties)
        self.view.radio_SI.clicked.connect(lambda: self.updateUnits(SI=True))
        self.view.radio_English.clicked.connect(lambda: self.updateUnits(SI=False))

    def update_T_High(self):
        """Updates the Turbine Inlet temperature based on the high pressure."""
        if self.view.radio_T_High.isChecked():
            pressure = float(self.view.lineEdit_P_High.text())
            t_sat = self.model.get_saturation_temperature(pressure)
            self.view.label_T_Sat.setText(f"Saturation Temperature: {t_sat}")

    def update_Properties(self):
        """Updates the properties displayed in the view based on the pressure inputs."""
        pressure = float(self.view.lineEdit_P_High.text())
        t_sat = self.model.get_saturation_temperature(pressure)
        self.view.label_T_Sat.setText(f"Saturation Temperature: {t_sat}")

    def updateUnits(self, SI):
        """Updates the units for the entire application based on the selected radio button."""
        unit_system = XSteam.UNIT_SYSTEM_MKS if SI else XSteam.UNIT_SYSTEM_ENGLISH
        self.model.steam_table.unitSystem = unit_system
        # Update all labels and calculations in the view accordingly

        # Example update
        pressure = float(self.view.lineEdit_P_High.text())
        t_sat = self.model.get_saturation_temperature(pressure)
        self.view.label_T_Sat.setText(
            f"Saturation Temperature: {t_sat} {(unit_system == XSteam.UNIT_SYSTEM_MKS and '°C' or '°F')}")

# Main application setup and execution logic here...

def main():
    app = QApplication([])
    model = rankineModel()
    view = rankineView()
    controller = rankineController(model, view)
    view.show()
    app.exec_()

if __name__ == '__main__':
    main()
