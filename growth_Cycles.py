import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def rem_anomolies(df):
    ''' Removes anomolies / smooves the curve '''
    Error_allowance = 1.5
    for i in range(len(df)-2):
        i+=1
        #if df['NDVI'].iloc[i] > (df['NDVI'].iloc[i-1] * Error_allowance) or df['NDVI'].iloc[i] > (df['NDVI'].iloc[i+1] * Error_allowance):
        if (df['NDVI'].iloc[i] - df['NDVI'].iloc[i-1]) > (0.15) or (df['NDVI'].iloc[i] - df['NDVI'].iloc[i+1]) > (0.15):
            df['NDVI'].iloc[i] = df['NDVI'].iloc[i-1] # Set to the same as previous value (This could be replaced by a regression of the last few points)
        else:
            continue
    return df
     

def get_Daily(df):
    ''' Converts from hourly measurements to daily means '''
    # Set 'TIMESTAMP_START' as the DataFrame index
    df.set_index('TIMESTAMP_START', inplace=True)

    # Resample data to daily frequency and calculate the mean for each day
    daily_mean = df.resample('D').mean()

    return daily_mean

def preprocess(df):
    ''' Convert to daily average NDVI readings and datetime '''
    # Convert time stamp to timedate format 
    
    df['TIMESTAMP_START'] = pd.to_datetime(df['TIMESTAMP_START'], format='%Y%m%d%H%M')

    # Convert -9999 values to NaN
    df.replace(-9999, np.nan, inplace=True)
    # Get daily values
    df = get_Daily(df)

    # Remove columns with all NaN values
    df = df.dropna(axis=1, how='all')
    
    # Remove rows with more than 13 missing values
    # Maybe replace this to just remove where NDVI is missing...
    df = df.dropna(axis=0, thresh=df.shape[1] - 13)
    print(df.head(10))
    return df

def plot_data(df):
    plt.figure(figsize=(10, 6))  
    plt.plot(df.index, df['NDVI'], marker='o', linestyle='-')
    plt.xlabel('Date')
    plt.ylabel('NDVI')
    plt.title('NDVI Over Time')
    plt.xticks(rotation=45)
    plt.show()

def get_peaks(df):
    ''' returns location of peaks (not local maxima) '''
    Percentage = int(len(df) * 0.40) # Percentage of data to remove (40%)
    
    peaks = []
    # Remove n% of lowest values
    sorted_NDVI_df = df.sort_values(by='NDVI',ascending=False)
    sorted_NDVI_df = sorted_NDVI_df.head(len(df) - Percentage) # Removes the last n% of values

    # Resort by date
    sorted_date_df = sorted_NDVI_df.sort_values(by='TIMESTAMP_START')
    #print(sorted_date_df)
    
    # Smoove curve
    df = rem_anomolies(sorted_date_df)

    # Check by plotting NDVI
    plot_data(sorted_date_df)

    return peaks

def get_prominence(location,df):
    ''' returns height of peak '''
    pass

def get_range():
    pass

def main():
    df = pd.read_csv('flux_Corn.csv')
    # Convert to daily readings 
    df = preprocess(df)
    # Find peaks
    peaks = get_peaks(df)

if __name__ == '__main__':
    main()