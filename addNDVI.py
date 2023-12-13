import pandas as pd

def main():
    ''' Adds NDVI value to df '''
    df = pd.read_csv('AMF_US-Bi2_BASE_HH_15-5.csv',skiprows=2)

    
    df['NDVI'] = 0
    for i in range(len(df)):
        if (df['SPEC_NIR_OUT'].iloc[i] + df['SPEC_RED_OUT'].iloc[i] == 0): # Ensure no division by zero
            df['NDVI'].iloc[i] = -9999
        elif df['SPEC_NIR_OUT'].iloc[i] == -9999 or df['SPEC_RED_OUT'].iloc[i] == -9999: # Ensure we keep null values
            df['NDVI'].iloc[i]  = -9999
        else:
            df['NDVI'].iloc[i]  = (df['SPEC_NIR_OUT'].iloc[i] - df['SPEC_RED_OUT'].iloc[i]) / (df['SPEC_NIR_OUT'].iloc[i] + df['SPEC_RED_OUT'].iloc[i])

    print(df.head(10))
    df.to_csv('flux_Corn.csv',index=False)

if __name__ == '__main__':
    main()
