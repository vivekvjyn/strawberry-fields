import numpy as np

def calculate_fundamental_frequencies(peak_frequencies, peak_magnitudes):
    """
    Calculate fundamental frequencies from peak frequencies and magnitudes of peaks in a spectrogram.

    Parameters:
        peak_frequencies (array_like): A list containing arrays of peak frequencies of the signal.
        peak_magnitudes (array_like): A list containing arrays of peak magnitudes of the signal.

    Returns:
        fundamental_frequencies (array_like): A list containing fundamental frequencies of the signal.
    """
    fundamental_frequencies = []

    # Iterate through each frame
    for frequencies, magnitudes in zip(peak_frequencies, peak_magnitudes):
        candidate_frequencies = []

        # Identify candidate fundamental frequencies based on differences between consecutive peak frequencies
        for index in range(len(frequencies) - 1):
            frequency_difference = frequencies[index + 1] - frequencies[index]

            # Check if the frequency difference falls within the specified range
            if 80 < frequency_difference < 255:
                candidate_frequencies.append(frequency_difference)

        # If no candidate frequencies are found, default fundamental frequency to 100 Hz
        if not candidate_frequencies:
            fundamental_frequency = 100

        else:
            # Initialize fundamental frequency to the first candidate frequency
            fundamental_frequency = candidate_frequencies[0]
            least_error = float('inf')

            # Iterate through candidate frequencies to find the one with the least error
            for candidate_frequency in candidate_frequencies:
                predicted_to_measured_error = 0
                measured_to_predicted_error = 0
                harmonic_frequency = candidate_frequency
                predicted_frequencies = []

                # Generate predicted frequencies based on the harmonic series of the current candidate frequency
                while harmonic_frequency < frequencies[-1] + candidate_frequency:
                    predicted_frequencies.append(harmonic_frequency)
                    harmonic_frequency += candidate_frequency

                # Calculate error using a weighted error function
                for frequency, magnitude in zip(frequencies, magnitudes):
                    differences = np.array([np.abs(predicted_frequency - frequency) for predicted_frequency in predicted_frequencies])
                    closest_harmonic_frequency = predicted_frequencies[differences.argmin()]

                    # Compute error terms
                    predicted_to_measured_error += (closest_harmonic_frequency - frequency) * (closest_harmonic_frequency) ** (-0.5) + magnitude / (max(magnitudes) - 0.01) * (1.4 * (closest_harmonic_frequency - frequency) * (closest_harmonic_frequency) ** (-0.5) - 0.5)
                    measured_to_predicted_error += (closest_harmonic_frequency - frequency) * (frequency) ** (-0.5) + magnitude / (max(magnitudes) - 0.01) * (1.4 * (closest_harmonic_frequency - frequency) * (frequency) ** (-0.5) - 0.5)

                # Calculate total error and update fundamental frequency if error is reduced
                total_error = (predicted_to_measured_error + measured_to_predicted_error) / len(frequencies)

                if total_error < least_error:
                    least_error = total_error
                    fundamental_frequency = candidate_frequency

        # Append the fundamental frequency for the current frame
        fundamental_frequencies.append(fundamental_frequency)

    return fundamental_frequencies
