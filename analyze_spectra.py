# -*- coding: utf-8 -*-
"""analyze_spectra.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1-8761Bmud1phIryy7UKMw-2qmL1-LWO6
"""

import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from skimage.filters import threshold_otsu

def readcsv(file: str, header: bool = False, separator: str = ';') -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """
    Gets the wavenumbers and intensity from a .csv file.

    Args:
        file (str): Path to .csv file.
        header (bool, optional): If True, the headers in the .csv file - which are in the first
            columns - are read and exported. Defaults to False.
        separator (str, optional): Separator between values, can be ';', ',', ':', or '.'. Defaults to ';'.

    Returns:
        tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]: A tuple containing:
            - wavenumbers (np.ndarray): Array containing the wavenumbers.
            - intensities (np.ndarray): 2D array containing intensities of the Raman measurements;
              measurements in rows.
            - headLabels (optional) (np.ndarray): Array of labels corresponding to the titles of the header columns.
            - headColumns (optional) (np.ndarray): Array of heading information corresponding to each measurement.
    """
    # Read the file and extract the header row and data lines
    with open(file, 'r') as f:
        headRow = f.readline().replace("'", "").replace(",", ".")
        headRowArray = headRow.split(separator)

        # Find the starting column index of the wavenumbers
        startcol = next((i for i, v in enumerate(headRowArray) if is_float(v)), 0)

        # Extract the wavenumbers and header labels
        wavenumbers = np.array([float(x) for x in headRowArray[startcol:]])
        headLabels = np.array([label[5:] if label.startswith('META:') else label for label in headRowArray[:startcol]])

        # Read the data lines and store the intensities
        lines = f.readlines()
        nMeasurements = len(lines)
        nFeatures = len(wavenumbers)

        intensities = np.zeros((nMeasurements, nFeatures))
        headColumns = np.zeros((0, startcol))

        for i, line in enumerate(lines):
            elements = line.replace("'", "").replace(",", ".").split(separator)
            headColumns = np.vstack([headColumns, elements[:startcol]])
            intensities[i, :] = [float(x) for x in elements[startcol:]]

    if header:
        headLabels = np.array(headLabels)
        return headLabels, headColumns, wavenumbers, intensities
    else:
        return wavenumbers, intensities


def is_float(value: str) -> bool:
    """
    Checks if a given value can be converted to float.

    Args:
        value (str): Value to be checked.

    Returns:
        bool: True if the value can be converted to float, False otherwise.
    """
    try:
        float(value)
        return True
    except ValueError:
        return False

from google.colab import drive

# Mount Google Drive to access files
drive.mount('/gdrive')

# Set the path to the experimental CSV file
experimental_csv = '/gdrive/MyDrive/assignment/Experimental_sample.csv'

# Set the path to the media CSV file
media_csv = '/gdrive/MyDrive/assignment/Media.csv'

# Read the media CSV file and extract the header labels, header columns, wavenumbers, and intensities
header_labels_media, header_columns_media, wavenumbers_media, intensities_media = readcsv(media_csv, header=True)

# Read the experimental CSV file and extract the header labels, header columns, wavenumbers, and intensities
header_labels, header_columns, wavenumbers, intensities = readcsv(experimental_csv, header=True)

"""
  Plotting the Spectra for all the spectrums in measurement file
"""

# Set the figure size
plt.figure(figsize=(16, 8))

# Define the number of spectra
num_spectra = len(intensities)

# Generate a color palette with the specified number of distinct colors
colors = sns.color_palette('husl', num_spectra)

# Plotting the spectra with unique colors
for i in range(len(intensities)):
    plt.plot(wavenumbers, intensities[i, :], color=colors[i], label=f'Spectrum {i+1}', linewidth=1)

# Customize the plot
plt.xlabel('Wavenumbers', fontsize=14)
plt.ylabel('Intensity', fontsize=14)
plt.title('Raman Spectra', fontsize=16)
plt.grid(True, linestyle='--', alpha=0.5)

# Adjust plot layout
plt.tight_layout(rect=[0.05, 0, 0.8, 1])

# Adjust the linewidth of the plotted lines
linewidth = 1.5

# Loop over the plotted lines to adjust linewidth and linestyle
for line in plt.gca().lines:
    line.set_linewidth(linewidth)
    line.set_linestyle('-')

# Place the legend outside the plot, starting from the same position as the plot
plt.legend(loc='upper left', bbox_to_anchor=(1.05, 1), fontsize=10)

# Display the plot
plt.show()

"""
  Create the dataframe that includes the complete information of the data file measurement
"""

# Create the first dataframe
df1 = pd.DataFrame(header_columns, columns=header_labels)

# Create the second dataframe
df2 = pd.DataFrame(intensities, columns=wavenumbers)

# Merge the dataframes into one based on the column names
measurement_df = pd.concat([df1, df2], axis=1)

# Display the merged dataframe
print(measurement_df.head())

"""
Approach 1: To find strong and weak spectras
The following code generates two plots. The first plot represents the distribution of peak intensities, while the second plot displays the spectra of
various observations in the measurement file. This updated plot distinguishes between weak and strong spectra by highlighting their respective characteristics. The spectrums highlighted
in black color indicates the strong spectras. Here I relax the threshold valuue obtained from Otsu's method by 0.715 which is a heuristic adjustment to account for variations in the dataset
and to tune the threshold for the specific application.
"""

# Set the figure size
plt.figure(figsize=(16, 8))

# Define the number of spectra
num_spectra = len(intensities)

# Generate a color palette with the specified number of distinct colors
colors = sns.color_palette('husl', num_spectra)

# Calculate the peak intensities for each spectrum
peak_intensities = np.max(intensities, axis=1)

# Plot a histogram of the peak intensities
plt.hist(peak_intensities, bins=20, color='lightblue', edgecolor='black')
plt.xlabel('Peak Intensity', fontsize=14)
plt.ylabel('Count', fontsize=14)
plt.title('Distribution of Peak Intensities', fontsize=16)

# Apply Otsu's method to determine the threshold
threshold = threshold_otsu(peak_intensities)

# Relax the threshold by multiplying it with a factor
threshold_relaxed = threshold * 0.715  # Adjust the factor as needed

# Plot a vertical line at the relaxed threshold
plt.axvline(threshold_relaxed, color='green', linestyle='--', linewidth=2, label='Relaxed Threshold')

# Adjust plot layout
plt.tight_layout()

# Display the histogram plot
plt.show()

# Set the figure size
plt.figure(figsize=(16, 8))

# Plotting the spectra with unique colors and labels
for i in range(len(intensities)):
    if peak_intensities[i] < threshold_relaxed:
        label = f'Weak Spectrum {i+1}'
        linewidth = 1
    else:
        label = f'Strong Spectrum {i+1}'
        linewidth = 2

    plt.plot(wavenumbers, intensities[i, :], color=colors[i], label=label, linewidth=linewidth)

# Highlight the strong spectra
strong_indices_relaxed = np.where(peak_intensities >= threshold_relaxed)[0]
for idx in strong_indices_relaxed:
    plt.plot(wavenumbers, intensities[idx, :], color='black', linewidth=3, alpha=0.8)

# Customize the plot
plt.xlabel('Wavenumbers', fontsize=14)
plt.ylabel('Intensity', fontsize=14)
plt.title('Raman Spectra' , fontsize=16)

# Adjust plot layout
plt.tight_layout(rect=[0.05, 0, 0.8, 1])

# Place the legend outside the plot, starting from the same position as the plot
plt.legend(loc='upper left', bbox_to_anchor=(1.05, 1), fontsize=10)

# Display the plot
plt.show()

# Initialize lists to store strong and weak spectra indexes
strong_spectra = []
weak_spectra = []

# Iterate over the peak intensities and determine strong and weak spectra
for i, intensity in enumerate(peak_intensities):
    if intensity >= threshold_relaxed:
        strong_spectra.append(i)
    else:
        weak_spectra.append(i)

# Count the number of strong and weak spectra
num_strong = len(strong_spectra)
num_weak = len(weak_spectra)

# Print the counts
print(f"Number of strong spectra in measurement file: {num_strong}")
print(f"Number of weak spectra in measurement file: {num_weak}")

wave_num = measurement_df.iloc[:, 10:].columns

weak_spectra_measurement = measurement_df[measurement_df.index.isin(set(weak_spectra))].reset_index()

plt.figure(figsize=(16, 8))

# Define the number of spectra
num_spectra = len(intensities)

# Generate a color palette with the specified number of distinct colors
colors = sns.color_palette('husl', num_spectra)

# Plot each spectrum
for i in range(len(weak_spectra_measurement)):
    plt.plot(wave_num, weak_spectra_measurement.loc[i, wave_num], color=colors[i], label=f'Weak Spectra {i+1}', linewidth=2)

# Customize the plot
plt.xlabel('Wavenumbers', fontsize=14)
plt.ylabel('Intensity', fontsize=14)
plt.title('Raman Spectra' , fontsize=16)

# Adjust plot layout
plt.tight_layout(rect=[0.05, 0, 0.8, 1])

# Place the legend outside the plot, starting from the same position as the plot
plt.legend(loc='upper left', bbox_to_anchor=(1.05, 1), fontsize=10)

# Display the plot
plt.show()

strong_spectra_measurement = measurement_df[measurement_df.index.isin(set(strong_spectra))].reset_index()

plt.figure(figsize=(16, 8))

print(len(strong_spectra_measurement))

# Plot each spectrum
for i in range(len(strong_spectra_measurement)):
    plt.plot(wave_num, strong_spectra_measurement.loc[i, wave_num], color=colors[i], label=f'Strong Spectra {i+1}', linewidth=2)

# Set plot title and labels
plt.title('Spectra Visualization')
plt.xlabel('Wavenumbers')
plt.ylabel('Intensity')

# Customize the plot
plt.xlabel('Wavenumbers', fontsize=14)
plt.ylabel('Intensity', fontsize=14)
plt.title('Raman Spectra' , fontsize=16)

# Adjust plot layout
plt.tight_layout(rect=[0.05, 0, 0.8, 1])

# Place the legend outside the plot, starting from the same position as the plot
plt.legend(loc='upper left', bbox_to_anchor=(1.05, 1), fontsize=10)

# Display the plot
plt.show()

"""
  Analysis 2:
  Now we analyse the Temporal Distribution of the weak spectra.
"""

df = measurement_df[~measurement_df.index.isin(set(strong_spectra))]
df['DateTime'] = pd.to_datetime(df['DateTime'])

# Round the timestamps to the nearest 10-minute interval
df['dateTime_rounded'] = df['DateTime'].dt.floor('10Min')

# Count the number of observations for each time interval
count_by_period = df['dateTime_rounded'].value_counts()

# Sort the time intervals in ascending order
count_by_period = count_by_period.sort_index()

# Calculate the start and end times for each interval
interval_start = count_by_period.index
interval_end = interval_start + pd.Timedelta(minutes=10)

# Generate x-axis labels for the bar plot
x_labels = [f'{start.strftime("%H:%M")} - {end.strftime("%H:%M")}' for start, end in zip(interval_start, interval_end)]

# Plotting the bar graph
plt.figure(figsize=(12, 6))
plt.bar(x_labels, count_by_period)

# Set plot title and labels
plt.title('Count of Observations by Time Interval', fontsize=16)
plt.xlabel('Time Interval', fontsize=14)
plt.ylabel('Count', fontsize=14)

# Rotate x-axis labels for better visibility if needed
plt.xticks(rotation=45)

# Display the plot
plt.tight_layout()
plt.show()

# Convert the datetime strings to actual datetime objects
DateTime = np.array([np.datetime64(dt) for dt in df['DateTime']])

# Calculate the mean intensity for each spectrum
mean_intensity = np.mean(df.loc[:, wave_num], axis=1)

# Plot the temporal distribution of the weak spectra
plt.figure(figsize=(16, 8))
plt.plot(DateTime, mean_intensity, marker='o', markersize=5, linestyle='-', linewidth=1)
plt.xlabel('Time', fontsize=14)
plt.ylabel('Mean Intensity', fontsize=14)
plt.title('Temporal Distribution of Weak Spectra', fontsize=16)
plt.xticks(rotation=45)
plt.grid(True)
plt.tight_layout()
plt.show()

"""
  Approach 2:
  Now I am also using the second approach IQR to find out the outliers in the measurement data. Here I will try to find out the high peak intensities as outliers. The spectrums which have
  high peak intensity will be considered as outliers and hence I will categorize them as strong spectras.
"""

from scipy import stats
wave_num = measurement_df.iloc[:, 10:].columns

outlier = []
for wave in wave_num:
    q1 = measurement_df[wave].quantile(0.25)
    q3 = measurement_df[wave].quantile(0.75)
    iqr = q3 - q1
    lower_bound = q1 - (5 * iqr) # change the multiplier from 1.5 to another value to increase the threshold for identifying outliers.
    upper_bound = q3 + (4 * iqr)

    if len(measurement_df[(measurement_df[wave] < lower_bound) | (measurement_df[wave] > upper_bound)]) != 0:
        outlier.append(wave)

# Now above steps gives all the wavenumbers which are having outliers
print("Outlier columns:", outlier)

# now find rows which have these outliers in these columns (or strong spectras)

strong_spectra_approach2 = []
for col in outlier:
    q1 = measurement_df[col].quantile(0.25)
    q3 = measurement_df[col].quantile(0.75)
    iqr = q3 - q1
    lower_bound = q1 - 5* iqr
    upper_bound = q3 + 4* iqr

    # Filter the values within the lower and upper bounds
    filtered_values = measurement_df[(measurement_df[col] <= lower_bound) | (measurement_df[col] >= upper_bound)]

    # Find the index of the maximum value within the filtered values
    max_index = filtered_values[col].index.values
    strong_spectra_approach2.extend(max_index)

# Find the indexes of the spectras in the dataframe measurement_df which are strong
print(list(set(strong_spectra_approach2)))

#Now find all the strong spectras waveform information from the measurement dataframe and store all this information in new dataframe measurement_strong
measurement_strong = measurement_df[measurement_df.index.isin(set(strong_spectra_approach2))].reset_index()

# Set the figure size
plt.figure(figsize=(16, 8))

# Define the number of spectra
num_spectra = len(intensities)

# Generate a color palette with the specified number of distinct colors
colors = sns.color_palette('husl', num_spectra)

# Plot each spectrum
for i in range(len(measurement_strong)):
    plt.plot(wave_num, measurement_strong.loc[i, wave_num], color=colors[i], label=f'Strong peak Spectras {i+1}', linewidth=2)

# Customize the plot
plt.xlabel('Wavenumbers', fontsize=14)
plt.ylabel('Intensity', fontsize=14)
plt.title('Raman Spectra', fontsize=16)

# Adjust plot layout
plt.tight_layout(rect=[0.05, 0, 0.8, 1])

# Place the legend outside the plot
plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))

# Display the plot
plt.show()

#Now find all the weak spectras waveform information from the measurement dataframe and store all this information in new dataframe measurement_strong
measurement_weak = measurement_df[~measurement_df.index.isin(set(strong_spectra_approach2))].reset_index()

# Set the figure size
plt.figure(figsize=(16, 8))

# Define the number of spectra
num_spectra = len(intensities)

# Generate a color palette with the specified number of distinct colors
colors = sns.color_palette('husl', num_spectra)

# Plot each spectrum
for i in range(len(measurement_weak)):
    plt.plot(wave_num, measurement_weak.loc[i, wave_num], color=colors[i], label=f'Weak peaks Spectras {i+1}', linewidth=2)

# Customize the plot
plt.xlabel('Wavenumbers', fontsize=14)
plt.ylabel('Intensity', fontsize=14)
plt.title('Raman Spectra', fontsize=16)

# Adjust plot layout
plt.tight_layout(rect=[0.05, 0, 0.8, 1])

# Place the legend outside the plot, starting from the same position as the plot
plt.legend(loc='upper left', bbox_to_anchor=(1.05, 1), fontsize=10)

# Display the plot
plt.show()

"""
  Analysis 2:
  Now we analyse the Temporal Distribution of the weak spectra.
"""

measurement_weak['DateTime'] = pd.to_datetime(df['DateTime'])

# Round the timestamps to the nearest 10-minute interval
measurement_weak['dateTime_rounded'] = measurement_weak['DateTime'].dt.floor('10Min')

# Count the number of observations for each time interval
count_by_period = measurement_weak['dateTime_rounded'].value_counts()

# Sort the time intervals in ascending order
count_by_period = count_by_period.sort_index()

# Calculate the start and end times for each interval
interval_start = count_by_period.index
interval_end = interval_start + pd.Timedelta(minutes=10)

# Generate x-axis labels for the bar plot
x_labels = [f'{start.strftime("%H:%M")} - {end.strftime("%H:%M")}' for start, end in zip(interval_start, interval_end)]

# Plotting the bar graph
plt.figure(figsize=(12, 6))
plt.bar(x_labels, count_by_period)

# Set plot title and labels
plt.title('Count of Observations by Time Interval', fontsize=16)
plt.xlabel('Time Interval', fontsize=14)
plt.ylabel('Count', fontsize=14)

# Rotate x-axis labels for better visibility if needed
plt.xticks(rotation=45)

# Display the plot
plt.tight_layout()
plt.show()

# Convert the 'DateTime' column to datetime objects
DateTime = pd.to_datetime(measurement_weak['DateTime'])

# Calculate the mean intensity for each spectrum
mean_intensity = np.mean(measurement_weak.loc[:, wave_num], axis=1)


# Plot the temporal distribution of the weak spectra
plt.figure(figsize=(16, 8))
plt.plot(DateTime, mean_intensity, marker='o', markersize=5, linestyle='-', linewidth=1)
plt.xlabel('Time', fontsize=14)
plt.ylabel('Mean Intensity', fontsize=14)
plt.title('Temporal Distribution of Weak Spectra', fontsize=16)
plt.xticks(rotation=45)
plt.grid(True)
plt.tight_layout()
plt.show()

"""
  Plotting the Spectra for all the spectrums in media file
"""

import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

# Set the figure size
plt.figure(figsize=(16, 8))

# Define the number of spectra
num_spectra = len(intensities_media)

# Generate a color palette with the specified number of distinct colors
colors = sns.color_palette('husl', num_spectra)

# Plotting the spectra with unique colors
for i in range(num_spectra):
    plt.plot(wavenumbers_media, intensities_media[i, :], color=colors[i], label=f'Spectrum {i+1}', linewidth=2)

# Customize the plot
plt.xlabel('Wavenumbers', fontsize=14 )
plt.ylabel('Intensity', fontsize=14)
plt.title('Raman Spectra', fontsize=16)
plt.grid(True, linestyle='--', alpha=0.5)

# Adjust plot layout
plt.tight_layout(rect=[0.05, 0, 0.8, 1])

# Adjust the linewidth of the plotted lines
linewidth = 1.5

# Loop over the plotted lines to adjust linewidth and linestyle
for line in plt.gca().lines:
    line.set_linewidth(linewidth)
    line.set_linestyle('-')

# Place the legend outside the plot
plt.legend(loc='center left', bbox_to_anchor=(1, 0.5), fontsize=10)

# Display the plot
plt.show()

"""
  Create the dataframe that includes the complete information of the data file media
"""

# Create the first dataframe
df1_media = pd.DataFrame(header_columns_media, columns=header_labels_media)

# Create the second dataframe
df2_media = pd.DataFrame(intensities_media, columns=wavenumbers_media)

# Merge the dataframes into one based on the column names
media_df = pd.concat([df1_media, df2_media], axis=1)

print(media_df.head())

"""
  Approach 3:
  Now I am also using the third approach where I am matching the each spectrum waveform intensities in the measuremnt file with the each spectrum waveform intensities in the media file.
  Then the spectrums which match with media data, I classify them as weak spectras ans those not match as strong spectras as the spectras which match it indiactes that these spectras
  does not have bacteria information in media and hence are weak spectrums in measurement file.
"""

# Get the waveform intensities from the media dataframe
media_intensities = media_df.iloc[:, 11:].values

# Create a mask for the spectras in measurement file which not match with media spectras are therefore strong spectras
mask = np.logical_not(np.isin(measurement_df.iloc[:, 11:].values, media_intensities).all(axis=1))

# Filter out the strong spectra from the measurement dataframe
strong_filtered_measurement_df = measurement_df[mask]

# Display the indexes that are not included in the filtered dataframe and are the indices for the weak spectrums
non_matching_indexes = measurement_df[~mask].index.tolist()
print("Indexes not included in filtered dataframe:", non_matching_indexes)

# Now plot the specral graph for the strong spectras

# Set the figure size
plt.figure(figsize=(16, 8))

# Get the wavenumbers and intensities from the filtered measurement dataframe
wavenumbers = strong_filtered_measurement_df.columns[11:].astype(float)
intensities = strong_filtered_measurement_df.iloc[:, 11:].values

# Define the number of spectra
num_spectra = len(intensities)

# Generate a color palette with the specified number of distinct colors
colors = sns.color_palette('husl', num_spectra)

# Plotting the spectra with unique colors
for i in range(num_spectra):
    plt.plot(wavenumbers, intensities[i, :], color=colors[i], label=f'Strong Spectras {i+1}', linewidth=2)

# Customize the plot
plt.xlabel('Wavenumbers', fontsize=14 )
plt.ylabel('Intensity', fontsize=14)
plt.title('Raman Spectra', fontsize=16)
plt.grid(True, linestyle='--', alpha=0.5)

# Adjust the linewidth of the plotted lines
linewidth = 1.5

# Loop over the plotted lines to adjust linewidth and linestyle
for line in plt.gca().lines:
    line.set_linewidth(linewidth)
    line.set_linestyle('-')

# Adjust plot layout
plt.tight_layout(rect=[0.05, 0, 0.8, 1])

# Place the legend outside the plot, starting from the same position as the plot
plt.legend(loc='upper left', bbox_to_anchor=(1.05, 1), fontsize=10)

# Display the plot
plt.show()

# Now plot the specral graph for the weak spectras

# Set the figure size
plt.figure(figsize=(16, 8))

# Get the indexes of spectra not included in the filtered dataframe
non_matching_indexes = measurement_df[~mask].index.tolist()


# Plot the spectra not included in the filtered dataframe
for index in non_matching_indexes:
    spectrum = measurement_df.iloc[index, 11:]
    plt.plot(wavenumbers, spectrum, label=f'Weak Spectra {index}')

# Customize the plot
plt.xlabel('Wavenumbers', fontsize=14 )
plt.ylabel('Intensity', fontsize=14)
plt.title('Raman Spectra', fontsize=16)
plt.grid(True, linestyle='--', alpha=0.5)

# Adjust the linewidth of the plotted lines
linewidth = 1.5

# Loop over the plotted lines to adjust linewidth and linestyle
for line in plt.gca().lines:
    line.set_linewidth(linewidth)
    line.set_linestyle('-')

# Adjust plot layout
plt.tight_layout(rect=[0.05, 0, 0.8, 1])

# Place the legend outside the plot, starting from the same position as the plot
plt.legend(loc='upper left', bbox_to_anchor=(1.05, 1), fontsize=10)

# Display the plot
plt.show()

"""
  Analysis 2:
  Now we analyse the Temporal Distribution of the weak spectra.
"""

plt.figure(figsize=(16, 8))

# Convert the datetime strings to actual datetime objects for non-matching indexes
non_matching_datetime = np.array([np.datetime64(dt) for dt in measurement_df.loc[non_matching_indexes, 'DateTime']])

# Calculate the mean intensity for each spectrum for non-matching indexes
non_matching_mean_intensity = np.mean(measurement_df.loc[non_matching_indexes, wave_num], axis=1)

# Calculate the total number of observations used in weak spectras
total_observations = len(non_matching_indexes)

# Plot the temporal distribution of the non-matching spectra
plt.plot(non_matching_datetime, non_matching_mean_intensity, marker='o', markersize=5, linestyle='-', linewidth=1)
plt.xlabel('Time', fontsize=14)
plt.ylabel('Mean Intensity', fontsize=14)
plt.title('Temporal Distribution of Weak Spectras', fontsize=16)
plt.xticks(rotation=45)
plt.grid(True)
plt.tight_layout()
plt.show()