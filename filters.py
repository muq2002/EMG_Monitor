import numpy as np

def moving_average_filter(data, window_size):
    if window_size < 1:
        raise ValueError("Window size must be at least 1")

    data_array = np.array(data)

    cumulative_sum = np.cumsum(data_array, dtype=float)

    moving_avg = (cumulative_sum[window_size:] - cumulative_sum[:-window_size]) / window_size

    initial_values = data_array[:window_size - 1]

    filtered_data = np.concatenate((initial_values, moving_avg))

    return filtered_data

# print(moving_average_filter([1, 2, 3, 5, 65, 5, 675, 454, 233, 4, 5, 6, 7], 5))


def integrate_discrete_signal(signal):
    signal_array = np.array(signal)

    integrated_signal = np.cumsum(signal_array)

    return integrated_signal