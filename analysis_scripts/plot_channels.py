import os
import re
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from loguru import logger

logger.info('Import OK')

input_path = 'raw_data/'
output_folder = 'results/channels/'

if not os.path.exists(output_folder):
    os.makedirs(output_folder)


channels = pd.read_csv(f'{input_path}channel_messages.xlsx')
channels.drop([col for col in channels.columns.tolist() if 'Unnamed: ' in col], axis=1, inplace=True)
channels = pd.melt(
    channels,
    id_vars=['date', 'day'],
    value_vars=['general_gibberish', 'important_info', 'lab_laziness', 'exciting_experiments'],
    var_name='channel',
    value_name='number_of_messages',
)
# Add month column, clean column types
channels['date'] = pd.to_datetime(channels['date'])
channels['month'] = pd.to_datetime(channels.set_index('date').index).month
channels['month_name'] = pd.to_datetime(channels.set_index('date').index).month_name()
channels['day_name'] = channels['day']
channels['day'] = channels['day'].map(dict(zip(['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'], np.arange(0,5))))

# total number of messages per day, per month
fig, ax = plt.subplots()
sns.lineplot(
    data=channels,
    x='day',
    y='message_count',
    hue='month',
    palette='rocket'
)
plt.xticks(ticks=np.arange(7), labels=[
           'Thursday', 'Friday', 'Saturday', 'Sunday', 'Monday', 'Tuesday', 'Wednesday', ])
plt.ylabel('Mean messages per day')
plt.xlabel('Day')
plt.legend(bbox_to_anchor=(1.0, 1.0), title='Month')
plt.savefig(f'{output_folder}channels_per_day.png')

# plot sum of all channel messages over time
fig, ax = plt.subplots()
sns.lineplot(
    data=channels.groupby(['date', 'month_name', 'month']).sum(),
    x='date',
    y='number_of_messages',
    hue='name',
    palette='rocket'
)

plt.ylabel('Total messages per day')
plt.xlabel('Date')
plt.legend(bbox_to_anchor=(1.0, 1.0), title='Month')
plt.savefig(f'{output_folder}channels_per_date.png')
