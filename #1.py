import tkinter as tk
from tkinter import filedialog
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class PumpDataModel:
    """
    Manages the data related to the pump. It reads data from a file,
    performs the data fitting, and stores the coefficients.
    """
    def __init__(self):
        self.file_path = ""
        self.data = None

    def read_file(self, path):
        """
        Reads the data from the given file path and stores it in the model.

        :param path: Path to the data file.
        :return: The data read from the file.
        """
        self.file_path = path
        self.data = np.loadtxt(path, delimiter=',', skiprows=1)
        return self.data

    def fit_data(self):
        """
        Fits the data using polynomial regression.

        :return: Tuple of coefficients for the quadratic and cubic fits.
        """
        if self.data is not None:
            # Quadratic fit for Head
            head_coeffs = np.polyfit(self.data[:, 0], self.data[:, 1], 2)
            # Cubic fit for Efficiency
            eff_coeffs = np.polyfit(self.data[:, 0], self.data[:, 2], 3)
            return head_coeffs, eff_coeffs

class PumpDataView:
    """
    Represents the GUI of the application. It handles the user interactions
    and displays the data plot.
    """
    def __init__(self, root, controller):
        """
        Initializes the view components.

        :param root: The root window.
        :param controller: The controller handling user actions.
        """
        self.controller = controller
        self.frame = tk.Frame(root)
        self.frame.pack()
        self.plot_button = tk.Button(self.frame, text="Read File and Calculate", command=self.controller.load_data)
        self.plot_button.pack()
        self.figure = plt.Figure(figsize=(6, 4), dpi=100)
        self.ax = self.figure.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.figure, master=root)
        self.canvas.get_tk_widget().pack()

    def plot_data(self, data, head_coeffs, eff_coeffs):
        """
        Plots the raw data and fitted curves.

        :param data: The data to plot.
        :param head_coeffs: Coefficients for the head quadratic fit.
        :param eff_coeffs: Coefficients for the efficiency cubic fit.
        """
        x = data[:, 0]
        y1 = np.polyval(head_coeffs, x)
        y2 = np.polyval(eff_coeffs, x)
        self.ax.clear()  # Clear previous plot
        self.ax.plot(x, data[:, 1], 'r-', label='Head')
        self.ax.plot(x, y1, 'b--', label='Head Fit')
        self.ax.plot(x, data[:, 2], 'g-', label='Efficiency')
        self.ax.plot(x, y2, 'y--', label='Efficiency Fit')
        self.ax.set_title('Pump Data Analysis')
        self.ax.set_xlabel('Flow rate')
        self.ax.set_ylabel('Head / Efficiency')
        self.ax.legend()
        self.canvas.draw()

class PumpDataController:
    """
    Acts as the controller in the MVC pattern, mediating between the view
    and the model.
    """
    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.last_dir = ''

    def load_data(self):
        """
        Handles the event to load data from a file and update the view.
        """
        path = filedialog.askopenfilename(initialdir=self.last_dir)
        if path:
            self.last_dir = '/'.join(path.split('/')[:-1])
            data = self.model.read_file(path)
            head_coeffs, eff_coeffs = self.model.fit_data()
            self.view.plot_data(data, head_coeffs, eff_coeffs)

def main():
    """
    Main function to setup the MVC components and start the GUI loop.
    """
    root = tk.Tk()
    root.title("Pump Data Viewer")
    model = PumpDataModel()
    view = PumpDataView(root, None)
    controller = PumpDataController(model, view)
    view.controller = controller  # Set the controller after its creation
    root.mainloop()

if __name__ == "__main__":
    main()
