import pandas as pd
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt

input_path = "/Users/yoonheechoi/Desktop/Github repositories/lab_slackers/Raw_data/raw_data.csv"

raw_data = pd.read_csv(input_path)

df = pd.DataFrame.copy(raw_data)
df['Date'] = pd.to_datetime(df['Date'], infer_datetime_format=True)
df['Year'] = df['Date'].dt.year
df['Month'] = df['Date'].dt.month

pd.DataFrame.groupby(df['Year'])

sum_per_month = df.groupby(['Year','Month']).sum()['Messages posted'].reset_index()
sum_per_month.reset_index(inplace=True)

sns.barplot(x=sum_per_month['index'], y=sum_per_month['Messages posted'])
plt.savefig('/Users/yoonheechoi/Desktop/Github repositories/lab_slackers/yh_plot.png')