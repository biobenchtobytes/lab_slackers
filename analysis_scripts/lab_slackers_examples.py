import os
import re
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import altair as alt

from pandas_profiling import ProfileReport
from loguru import logger
from GEN_Utils import FileHandling

logger.info('Import OK')

input_path = 'Raw_data/raw_data.csv'
output_folder = 'dc_results/'

if not os.path.exists(output_folder):
    os.mkdir(output_folder)

raw_data = pd.read_csv(input_path)

# convert date-time column
summary_data = raw_data.copy()
summary_data['Date'] = pd.to_datetime(
    summary_data['Date'], infer_datetime_format=True)
summary_data['day_of_week'] = summary_data['Date'].dt.dayofweek
summary_data['total_messages'] = summary_data['Messages in public channels'] + \
    summary_data['Messages in private channels'] + \
    summary_data['Messages in shared channels'] + \
    summary_data['Messages in DMs']
summary_data.describe()
ProfileReport(summary_data)

summary_data.columns.tolist()

# number of messages per day
fig, ax = plt.subplots()
cmap = sns.cubehelix_palette(light=1, as_cmap=True)
sns.kdeplot(data=summary_data['day_of_week'].astype(
    int), data2=summary_data['total_messages'].astype(int), shade=True, cmap=cmap,)
plt.xticks(ticks=np.arange(7), labels=[
           'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'])
plt.ylim(-10, 50)
plt.savefig(f'{output_folder}dc_messages_per_day.png')

# Scatterplot of messages per day
fig, ax = plt.subplots()
cmap = sns.cubehelix_palette(light=1, as_cmap=True)
sns.swarmplot(x=summary_data['day_of_week'].astype(
    int), y=summary_data['total_messages'].astype(int))
plt.xticks(ticks=np.arange(7), labels=[
           'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'])
plt.ylim(-10, 50)


