import pandas as pd
from scipy.stats import mode


data = '''Region, Alcohol, Tobacco
North, 6.47, 4.03
Yorkshire, 6.13, 3.76
Northeast, 6.19, 3.77
East Midlands, 4.89, 3.34
West Midlands, 5.63, 3.47
East Anglia, 4.52, 2.92
Southeast, 5.89, 3.20
Southwest, 4.79, 2.71
Wales, 5.27, 3.53
Scotland, 6.08, 4.51
Northern Ireland, 4.02, 4.56'''

data = data.splitlines()
data = [i.split(',') for i in data ]
column_names = data[0] # this is the first row
data_rows = data[1::] # these are all the following rows of data
df = pd.DataFrame(data_rows, columns=column_names)
df[' Alcohol'] = df[' Alcohol'].astype(float)
df[' Tobacco'] = df[' Tobacco'].astype(float)

print "The Average Alcohol is: " + str(df[' Alcohol'].mean())
print "The Average Tobacco is: " + str(df[' Tobacco'].mean())
print "The Median Alcohol is: " + str(df[' Alcohol'].median())
print "The Median Tobacco is: " + str(df[' Tobacco'].median())
print "The Range of Alcohol is: " + str(max(df[' Alcohol']) - min(df[' Alcohol']))
print "The Range of Tobacco is: " + str(max(df[' Tobacco']) - min(df[' Tobacco']))
print "The Variance Alcohol is: " + str(df[' Alcohol'].var())
print "The Variance Tobacco is: " + str(df[' Tobacco'].var())
print "The Standard Deviation Alcohol is: " + str(df[' Alcohol'].std())
print "The Standard Deviation Tobacco is: " + str(df[' Tobacco'].std())

