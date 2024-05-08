import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Read data from CSV file
data = pd.read_csv('C:\Users\mktad\OneDrive\Desktop\Spirometer\data\Muqtada\data.csv', header=None)  # Assuming there's no header in the CSV file

# Assuming the data is in one column
value = pd.to_numeric(data.iloc[:, 0], errors='coerce')  # Convert data to numeric, ignoring errors

# Apply moving average filter
window_size = 10  # Example: window size for moving average
smoothed_value = value.rolling(window_size).mean()  # Apply moving average

# Generate time values assuming a constant sampling rate
sampling_rate = 1000  # Example: 1000 samples per second
time = np.arange(len(value)) / sampling_rate  # Assuming the data starts at time 0

# Plot original data
plt.figure(figsize=(15, 7))

plt.subplot(2, 2, 1)
plt.plot(time, value, color='blue')
plt.title('Original Data')
plt.xlabel('Time (s)')
plt.ylabel('Flow Rate')

# Plot smoothed data
plt.subplot(2, 2, 2)
plt.plot(time, smoothed_value, color='green')
plt.title('Smoothed Data (Moving Average)')
plt.xlabel('Time (s)')
plt.ylabel('Flow Rate (Smoothed)')

# Integrate the smoothed data
integrated_smoothed_value = np.cumsum(smoothed_value) / sampling_rate  # Simple integration using cumulative sum and assuming constant sampling rate

# Plot integrated smoothed data
plt.subplot(2, 2, 3)
plt.plot(time, integrated_smoothed_value, color='red')
plt.title('Integrated Smoothed Data')
plt.xlabel('Time (s)')
plt.ylabel('Volume (Smoothed)')

# Plot Value vs Integrated Smoothed Value
plt.subplot(2, 2, 4)
plt.plot(integrated_smoothed_value, smoothed_value, color='orange')
plt.title('Integrated Smoothed Value vs Smoothed Value')
plt.xlabel('Integrated Volume (Smoothed)')
plt.ylabel('Volume (Smoothed)')

plt.tight_layout()
plt.show()