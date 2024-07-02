import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm

# Example data
data = np.random.normal(0, 1, 1000)  # Replace with your actual data

# Fit a normal distribution to the data
mean, std_dev = norm.fit(data)

# Create an array of x values for plotting the PDF
x_values = np.linspace(min(data), max(data), 1000)

# Calculate the PDF values
pdf_values = norm.pdf(x_values, mean, std_dev)

# Plot the data histogram and PDF
plt.hist(data, bins=30, density=True, alpha=0.6, color='g', label='Data Histogram')
plt.plot(x_values, pdf_values, label='Fitted Normal Distribution PDF')
plt.xlabel('x')
plt.ylabel('Probability Density')
plt.title('PDF of Given Data')
plt.legend()
plt.grid(True)
plt.show()
