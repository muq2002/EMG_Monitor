import pandas as pd
from PyQt5.QtWidgets import QMessageBox
from matplotlib.figure import Figure


def read_csv_and_plot(filename, figure: Figure):
    try:
        # Read the CSV file using pandas
        df = pd.read_csv(filename)

        # Extract data from the CSV file
        # time = df["time"]
        pressure = df["Pressure"]
        # volume = df["volume"]
        flowrate = df["Flowrate"]

        ax1, ax2, ax3, ax4 = figure.get_axes()

        # Clear existing plots
        ax1.clear()
        ax2.clear()
        ax3.clear()
        ax4.clear()

        ax1.plot(
            pressure, label="Pressure", linestyle="-", color="blue", marker="o"
        )
        ax2.plot(flowrate, label="Volume", linestyle="-", color="blue", marker="o")
        # ax3.plot(
        #     time, flowrate, label="Flow Rate", linestyle="-", color="blue", marker="o"
        # )
        # ax4.plot(
        #     volume,
        #     flowrate,
        #     label="Volume vs Flow Rate",
        #     linestyle="-",
        #     color="blue",
        #     marker="o",
        # )

        ax1.set_xlabel("Time")
        ax1.set_ylabel("Pressure")
        ax1.set_title("Pressure over Time")
        ax1.legend()

        ax2.set_xlabel("Time")
        ax2.set_ylabel("Volume")
        ax2.set_title("Volume over Time")
        ax2.legend()

        ax3.set_xlabel("Time")
        ax3.set_ylabel("Flow Rate")
        ax3.set_title("Flow Rate over Time")
        ax3.legend()

        ax4.set_xlabel("Volume")
        ax4.set_ylabel("Flow Rate")
        ax4.set_title("Volume vs Flow Rate")
        ax4.legend()

        figure.tight_layout()

        figure.canvas.draw()

    except Exception as e:
        QMessageBox.warning(None, "Error", f"Failed to read CSV file: {e}")
