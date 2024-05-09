def get_ports():
    # Generate a list of port names as strings
    ports = [f"COM{x}" for x in range(1, 10)]
    return ports  # Return the list of ports as a list of strings

def get_baudrates():
    # Define a list of baud rates as strings
    baudrates = ["9600", "19200", "38400", "57600", "115200"]
    return baudrates  # Return the list of baud rates as a list of strings
