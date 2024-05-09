def get_ports():
    ports = [f"COM{x}" for x in range(1, 10)]
    return ports

def get_baudrates():
    baudrates = ["9600", "19200", "38400", "57600", "115200"]
    return baudrates

def apply_dark_mode_to_pyqt(app):
    """Apply a dark theme to the PyQt application."""
    dark_style = """
    QWidget {
        background-color: #2E2E2E;
        color: #E0E0E0;
    }
    QLabel {
        color: #E0E0E0;
    }
    """
    app.setStyleSheet(dark_style)

def apply_dark_mode_to_plot(figure, ax):
    """Apply a dark theme to the Matplotlib plot."""
    figure.patch.set_facecolor('#2E2E2E')
    ax.set_facecolor('#2E2E2E')

    # Set the plot and text colors to light
    ax.xaxis.label.set_color('#E0E0E0')
    ax.yaxis.label.set_color('#E0E0E0')
    ax.title.set_color('#E0E0E0')
    ax.tick_params(axis='x', colors='#E0E0E0')
    ax.tick_params(axis='y', colors='#E0E0E0')
    ax.spines['bottom'].set_color('#E0E0E0')
    ax.spines['left'].set_color('#E0E0E0')
    ax.spines['right'].set_color('#E0E0E0')
    ax.spines['top'].set_color('#E0E0E0')

    # Redraw the canvas to apply the new styles
    figure.canvas.draw()

