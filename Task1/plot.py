import json
import numpy as np
import matplotlib.pyplot as plt

# Load the JSON data
with open('testresult.json', 'r') as file:
    data = json.load(file)

def sanitize_filename(filename):
    return filename.replace(":", "_")

# Define a function to calculate the average and median times
def calculate_stats(times):
    return np.mean(times), np.median(times)

# Define a function to plot histograms
def plot_histogram(times, title, xlabel, ylabel, filename):
    plt.hist(times, bins=20, color='blue', alpha=0.7)
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.grid(True)
    plt.savefig(filename)
    plt.clf()  # Clear the figure for the next plot

# Initialize dictionaries to store results
average_download_times = {}
median_download_times = {}
average_upload_times = {}
median_upload_times = {}

# Analyze data
for key, value in data.items():
    # Calculate average and median download times
    avg_download_time, med_download_time = calculate_stats(value['download_time'])
    average_download_times[key] = avg_download_time
    median_download_times[key] = med_download_time

    # Calculate average and median upload times
    avg_upload_time, med_upload_time = calculate_stats(value['upload_time'])
    average_upload_times[key] = avg_upload_time
    median_upload_times[key] = med_upload_time

    # Plot download time histogram
    """
    plot_histogram(
        value['download_time'],
        f'Download Time Distribution for {key}',
        'Time (s)',
        'Frequency',
        sanitize_filename(f'download_time_histogram_{key}.png')
    )
    """
    # Plot upload time histogram
    """
    plot_histogram(
        value['upload_time'],
        f'Upload Time Distribution for {key}',
        'Time (s)',
        'Frequency',
        sanitize_filename(f'upload_time_histogram_{key}.png')
    )
    """

    
print("Average Download Times:")
print(average_download_times)

print("\nMedian Download Times:")
print(median_download_times)

print("\nAverage Upload Times:")
print(average_upload_times)

print("\nMedian Upload Times:")
print(median_upload_times)
# You can now use the average_download_times, median_download_times, average_upload_times, and median_upload_times
# dictionaries to compare the approaches and discuss the advantages as required by the task.

# NOTE: Replace 'testresult.json' with the actual path to your JSON file.
# NOTE: Make sure you have numpy and matplotlib installed in your Python environment.
