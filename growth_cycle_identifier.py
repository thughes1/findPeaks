import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import find_peaks

class plot_continuous_graph:
    def __init__(self,df):
        self.df = df
    
    def plot(self):
        ''' Plots the NDVI values over time on a scatter graph '''
        plt.scatter(self.df.index, self.df['NDVI'], marker='o', color='blue')
        plt.title('NDVI Scatter Plot')
        plt.xlabel('Time')
        plt.ylabel('NDVI')
        plt.show()

class preprocess:
    def __init__(self,filename='flux_Corn.csv'):
        self.df = pd.read_csv(filename)
        self.replace_with_nan()
        self.remove_nan_cols()
        self.remove_nan_rows()
        self.convert_to_daily()
        self.identify_peaks()
        self.identify_troughs()
        self.remove_low_values()
        # TEST
        #print(self.df)

    def convert_to_daily(self):
        ''' Converts readings to daily averages rather than half hourly '''
        # Convert TIMESTAMP_START to datetime
        self.df['TIMESTAMP_START'] = pd.to_datetime(self.df['TIMESTAMP_START'], format='%Y%m%d%H%M')
        self.df.set_index('TIMESTAMP_START', inplace=True)
        # Resample data to daily frequency and calculate the mean for each day
        self.df = self.df.resample('D').mean()

    def replace_with_nan(self):
        ''' Replaces -9999 values with NaN '''
        self.df.replace(-9999, np.nan, inplace=True)

    def remove_nan_cols(self):
        ''' Removes columns that only include NaN '''
        self.df.dropna(axis=1, how='all', inplace=True)

    def remove_nan_rows(self):
        ''' Remove rows that only contain NaN and where NDVI is NaN '''
        # Remove Rows that only contain NaN
        self.df.dropna(axis=0, how='all', subset=self.df.columns[2:], inplace=True)
        # Remove rows where NDVI is NaN
        self.df.dropna(subset=['NDVI'], inplace=True)

    def remove_anomolies(self):
        ''' Removes anomolous values '''
        pass 

    def identify_peaks(self):
        ''' Identifies true peaks, i.e. not local maxima '''
        self.peaks, _ = find_peaks(self.df['NDVI'].values,
                                    distance=10,
                                    prominence=0.5) 
        #print(self.peaks)
        #print(self.df.iloc[38],self.df.iloc[454],self.df.iloc[821])
    
    def identify_troughs(self):
        ''' Identifies start of growth cycles, ignoring noise '''
        self.troughs, _ = find_peaks(-self.df['NDVI'].values,
                                      distance=10,
                                      prominence=0.1)
        print(self.troughs)
        # Identify the closest two troughts to the peaks
        closest_troughs = {}
        for peak in self.peaks:
            left = self.troughs[self.troughs < peak]
            right = self.troughs[self.troughs > peak]

            if len(left) > 0:
                closest_left_trough = left[np.argmax(left)]
            else:
                closest_left_trough = None

            if len(right) > 0:
                closest_right_trough = right[np.argmin(right)]
            else:
                closest_right_trough = None
            
            closest_troughs[peak] = (closest_left_trough, closest_right_trough)
            self.isolate_cycles(closest_troughs)
        ''' Test
        print(closest_troughs)
        print(self.df.iloc[40])
        print(self.df.iloc[396])
        print(self.df.iloc[529])
        print(self.df.iloc[740])
        print(self.df.iloc[909])
        #print(self.df.iloc[613])
        '''
        
    def isolate_cycles(self, closest_troughs):
        ''' Sets values between troughs to zero '''
        ## This needs editing 
        prev_right_trough = 0
        for peak, (left_trough, right_trough) in closest_troughs.items():
            if left_trough is not None:
                # Set values between previous right trough and next left trough to zero
                self.df.iloc[prev_right_trough:left_trough,
                              self.df.columns.get_loc('NDVI')] = 0
            prev_right_trough = right_trough#

    def remove_low_values(self):
        ''' Removes values below 0.2 (maybe change this) '''
        self.df = self.df[(self.df['NDVI'] > 0.2)]
        #print(self.head)

p = preprocess()
# Get the processed DataFrame from the preprocess class
processed_df = p.df

# Use the processed DataFrame in the plot_continuous_graph class
plotter = plot_continuous_graph(processed_df)
plotter.plot()

## Todo 
# Remove values between certain NDVI values, e.g. 0.2