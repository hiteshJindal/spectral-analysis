# spectral-analysis
This repository contains code for analyzing Raman spectra data. The code is in Python and provides three approaches for identifying strong and weak spectra based on peak intensities.

## Approach 1: Finding strong and weak spectra based on peak intensities

The first approach uses the maximum peak intensity of each spectrum to classify them as strong or weak. The steps involved in this approach are as follows:

1. Read the spectra data from a CSV file.
2. Calculate the peak intensities for each spectrum.
3. Apply Otsu's method to determine the threshold for classifying strong and weak spectra.
4. Relax the threshold to include more spectra if desired.
5. Identify the strong and weak spectra based on the threshold.
6. Count the number of strong and weak spectra.
7. Plot the spectra, highlighting the strong and weak ones.

## Approach 2: Finding outliers using the IQR method

The second approach uses the interquartile range (IQR) to identify spectra with outliers, which are considered strong. The steps involved in this approach are as follows:

1. Read the Raman spectra data from a CSV file.
2. Calculate the IQR for each wavenumber.
3. Define a threshold (e.g., 5 times the IQR) for identifying outliers.
4. Find the indexes of spectra with outliers (strong spectra).
5. Find the indexes of spectra without outliers (weak spectra).
6. Count the number of strong and weak spectra.
7. Plot the spectra, highlighting the strong and weak ones.

## Approach 3: Matching waveform intensities

The third approach focuses on matching the waveform intensities of each spectrum in the measurement file with the waveform intensities in the media file. The spectrums that match the media data are classified as weak spectra, indicating that they do not contain bacterial information in the media. The steps involved in this approach are as follows:

1. Get the waveform intensities from the media data frame.
2. Create a mask for the spectra in the measurement file that do not match with media spectra, indicating strong spectra.
3. Filter out the strong spectra and weak spectra from the measurement data frame.
4. Display the indexes of weak spectra that are not included in the filtered data frame.
5. Plot the spectral graph for the strong spectra.
6. Plot the spectral graph for the weak spectra.

## Temporal Analysis

For each approach discussed above, a temporal analysis is performed to observe changes in the spectra over time. The temporal analysis includes the following steps:

1. Read the temporal information from a separate CSV file.
2. Align the temporal information with the corresponding spectra.
3. Plot the temporal profiles of weak spectra.
4. Analyze the temporal distribution of weak spectra.

## Usage

1. Clone the repository: git clone https://github.com/hiteshJindal/spectral-analysis.git
2. Install the required dependencies:
```python
   pip install numpy pandas seaborn matplotlib scikit-image
```
4. Also add the following import statement to the code:
```python
from skimage.filters import threshold_otsu
```
   Note: Make sure you have Python 3.x and pip installed.

5. Update the path to the CSV files in the code:

```python
measurement_csv = '/path/to/measurement_data.csv'
media_csv = '/path/to/media_data.csv'
temporal_csv = '/path/to/temporal_data.csv'
```

4. Run the code using Python:

```python
python analyze_spectra.py
```














