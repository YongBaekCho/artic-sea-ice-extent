import pandas as pd
import numpy as np
#Author : YongBaek Cho
#Date 2018-10-03
# This file is to dealing with data that is stored on disk in csv format using pandas
def get_data():
#Create and return a Series Object. Use read_csv
    df = pd.read_csv('N_seaice_extent_daily_v3.0.csv', skiprows=[0,1], names=[0,1,2, 'Extent'], usecols = [0,1,2,3], parse_dates = {'Dates': [0,1,2]}, header= None)
    data = df['Extent'].values
    dates = df['Dates'].values
    ts = pd.Series(data, dates)
    new_index = pd.date_range(ts.index[0], ts.index[-1])
    ts = ts.reindex(new_index)
    return ts
def clean_data(a):
#This function takes the Series created in get_data and alters it in place by filling in the missing data.
    for i in range(len(a)):
        if np.isnan(a[i]):
            a[i] = (a[i-1]+a[i+1])/2
    for i in range(len(a)):
        if np.isnan(a[i]) == True:
            a[i] = (a[ i - 365 ] + a[ i +366]) / 2
            
def get_column_labels():
#Generate and return a list of strings that will be used as column labels in a DataFrame  
    dates = pd.date_range('1/1/1978', periods=365)
    list_string = []

    for i in range(len(dates)):
        if dates[i].month < 10:
            if dates[i].day < 10:
                list_string.append(str(0) + str(dates[i].month) + str(0) + str(dates[i].day))
            else:
                list_string.append(str(0) + str(dates[i].month) + str(dates[i].day))
        else:
            if dates[i].day < 10:
                list_string.append(str(dates[i].month) + str(0) + str(dates[i].day))
            else:
                list_string.append(str(dates[i].month) + str(dates[i].day))

    return list_string

def extract_df(a):
#This function takes the cleaned Series as its argument and creates and returns a new DataFrame.
    col = get_column_labels()
    index = range(1979, 2018)
    df = pd.DataFrame(index = index, columns = col, dtype = np.float64)
    for row in df.index:
        for col in df.columns:
            df.loc[row,col] = a.loc[str(row) + "-" + col[:2]+"-"+col[2:]]
    return df
    
def extract_2018(ts):
#This function takes the cleaned Series as its argument and returns Series containing the data for 2018.
    return pd.Series(ts.loc['2018'])
def main():
#Use the above functions to read in the data, clean it, and store it to disk in the two files with using the to_csv methods.
    data = get_data()
    clean = clean_data(data)
    df = extract_df(data)
    df.to_csv("data_79_17.csv")
    df_18 = extract_2018(data)
    df_18.to_csv("data_2018.csv")
main()
    
    

    
