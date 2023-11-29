import numpy as np
from scipy.io import wavfile
import fractions


# Load the received signal from the file
filename = "dsbmix.wav"
fs, y = wavfile.read(filename)

# Define the duration of the signal
T = 2
t = np.linspace(0, T, T * fs, endpoint=False)

# Candidate the Given carrier frequencies and phases
fc_candidates = np.linspace(12.5e3, 12.9e3, 100)
theta_candidates = [0, np.pi / 4, np.pi / 2, 3 * np.pi / 4, np.pi]

# Decrease volume factor``
volume_factor = 1

# Initialize vars
max_energy = 0
best_fc = 0
best_theta = 0

# Go through candidate frequencies and phases
for fc in fc_candidates:
    for theta in theta_candidates:
        # Mix the received signal with the candidate carrier and decrease volume
        mixed_signal = volume_factor * y * np.cos(2 * np.pi * fc * t + theta)

        # Calculate energy Ey
        Ey = np.sum(mixed_signal**2)

        # Update the maximum energy and corresponding parameters if needed
        if Ey > max_energy:
            max_energy, best_fc, best_theta = Ey, fc, theta
            # Store the Signal
            demodulated_signal = mixed_signal.astype(np.int16)


# Export the best demodulated signal to a WAV file
output_filename = "Updated Voice msg.wav"
wavfile.write(
    output_filename,
    fs,
    demodulated_signal,
)

# Prompt for the word m(t) heard
m_t = input("Enter the word m(t) heard: ")
best_theta_fraction = fractions.Fraction(best_theta / np.pi).limit_denominator()

# Print the results
print(f"\nResults:")
# print(f"{fc_candidates}")
print(f"Energy Ey for the best combination: {max_energy:.4e}")
print(f"Word m(t) heard: {m_t}")
print(f"Frequency fc which the signal mixxed: {best_fc/1e3:.2f} kHz")
# Convert best_theta to the form π/Χ
print(f"Best Phase which the signal got mixxed: ({best_theta_fraction})π radians")
