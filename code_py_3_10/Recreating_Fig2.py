import json
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm


def plot_pdf(data_t):
    for key, values in data_t.items():
        # Extract the data, mean, and standard deviation
        data = np.array(values)
        mean = data[4]  # Assuming the 5th value is the mean
        std_dev = data[5]  # Assuming the 6th value is the standard deviation

        # Create an array of x values for plotting the PDF
        x_values = np.linspace(min(data), max(data), 1000)

        # Calculate the PDF values
        pdf_values = norm.pdf(x_values, mean, std_dev)

        # Plot the data histogram and PDF
        plt.figure()  # Create a new figure for each key
        plt.hist(data, bins=30, density=True, alpha=0.6, color='g', label='Data Histogram')
        plt.plot(x_values, pdf_values, label='Fitted Normal Distribution PDF')
        plt.xlabel('x')
        plt.ylabel('Probability Density')
        plt.title(f'PDF of Given Data for {key}')
        plt.legend()
        plt.grid(True)
        plt.show()


if __name__ == '__main__':
    with open('../data/exp_1/measurments_results/Feature_extraction_results_section_4_1.json', 'r') as file:
        data = json.load(file)
