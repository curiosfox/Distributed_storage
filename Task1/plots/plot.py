import json
import numpy as np
import matplotlib.pyplot as plt

# Load the JSON data
with open('Task1/testresult.json', 'r') as file:
    data = json.load(file)

def sanitize_filename(filename):
    return filename.replace(":", "_")
# Function to calculate the average and median times
def calculate_stats(times):
    return np.mean(times), np.median(times)

# Function to plot histogram and mark average and median
def plot_times_histogram(times, scenario, operation_type='download'):
    avg_time, median_time = calculate_stats(times)
    
    plt.figure(figsize=(10, 6))
    plt.hist(times, bins=20, color='skyblue', alpha=0.7)
    plt.axvline(avg_time, color='red', linestyle='dashed', linewidth=1, label=f'Average: {avg_time:.4f}')
    plt.axvline(median_time, color='green', linestyle='dashed', linewidth=1, label=f'Median: {median_time:.4f}')
    plt.title(f'Histogram of {operation_type.capitalize()} Times for {scenario}')
    plt.xlabel('Time (Seconds)')
    plt.ylabel('Frequency')
    plt.legend()
    name = f'{scenario}_{operation_type}.png'

    # Save the plot as a PNG file
    plt.savefig(sanitize_filename(name))
    
    # Close the current plot to avoid displaying it in the Jupyter notebook
    plt.close()

# Analyze data
for scenario, values in data.items():
    # Extract download and upload times
    download_times = values['download_time']
    upload_times = values['upload_time']
    
    # Plot histograms for download and upload times
    plot_times_histogram(upload_times, scenario, operation_type='upload')
