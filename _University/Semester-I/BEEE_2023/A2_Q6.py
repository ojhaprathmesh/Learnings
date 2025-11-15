import numpy as np

# Circuit parameters
R = 15  # Resistance in ohms
L = 0.6  # Inductance in henries
C = 15e-6  # Capacitance in farads
f = 100  # Frequency in hertz
V = 100  # Voltage in volts

# Calculate angular frequency
omega = 2 * np.pi * f

# Calculate reactances
XL = omega * L
XC = 1 / (omega * C)

# Calculate total impedance
Z = np.sqrt(R**2 + (XL - XC)**2)

# Calculate current
I = V / Z

# Calculate phase angle of current
phi = np.arctan((XL - XC) / R)

# Calculate voltages across each element
VR = I * R
VL = I * XL
VC = I * XC

# Print results
print(XL, XC)
print("Total impedance:", Z, "ohms")
print("Current:", I, "amps")
print("Phase angle of current:", phi, "degrees")
print("Voltage across resistor:", VR, "volts")
print("Voltage across inductor:", VL, "volts")
print("Voltage across capacitor:", VC, "volts")
