import os
import re
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from loguru import logger

logger.info('Import OK')

input_path = 'raw_data/'
output_folder = 'results/'

if not os.path.exists(output_folder):
    os.mkdir(output_folder)

direct = pd.read_csv(f'{input_path}direct_messages.csv')
direct.drop([col for col in direct.columns.tolist() if 'Unnamed: ' in col], axis=1, inplace=True)

# Add month column, clean column types
direct['date'] = pd.to_datetime(direct['date'])
direct['month'] = pd.to_datetime(direct.set_index('date').index).month
direct['month_name'] = pd.to_datetime(direct.set_index('date').index).month_name()
direct['day_name'] = direct['day']
direct['day'] = direct['day'].map(dict(zip(['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'], np.arange(0,7))))

# total number of messages per day, per month
fig, ax = plt.subplots()
sns.lineplot(
    data=direct,
    x='day',
    y='number_of_messages',
    hue='month',
    palette='rocket'
)
plt.xticks(ticks=np.arange(7), labels=[
           'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'])
plt.ylabel('Mean messages per day')
plt.xlabel('Day')
plt.legend(bbox_to_anchor=(1.0, 1.0), title='Month')
plt.savefig(f'{output_folder}messages_per_day.png')

# Scatterplot of messages per day
fig, ax = plt.subplots()
sns.swarmplot(
    data=direct,
    x='month',
    y='number_of_messages',
    hue='day_name')
plt.xticks(ticks=np.arange(12), labels=
           direct.groupby(['month', 'month_name']).sum().reset_index()['month_name'].tolist(), rotation=45)
plt.ylabel('Messages per day')
plt.xlabel('Month')
plt.legend(bbox_to_anchor=(1.0, 1.0), title='Day')
plt.savefig(f'{output_folder}messages_per_month.png')

# messages per person
fig, ax = plt.subplots()
sns.lineplot(
    data=direct.groupby(['month', 'name']).sum().reset_index(),
    x='month',
    y='number_of_messages',
    hue='name')
plt.xticks(ticks=np.arange(12), labels=
           direct.groupby(['month', 'month_name']).sum().reset_index()['month_name'].tolist(), rotation=45)
plt.ylabel('Total messages per month')
plt.xlabel('Month')
plt.legend(bbox_to_anchor=(1.0, 1.0), title='Lab member')
plt.savefig(f'{output_folder}messages_per_member.png')


channels = pd.read_csv(f'{input_path}channel_messages.csv')
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
channels['day'] = channels['day'].map(dict(zip(['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'], np.arange(0,7))))

# total number of messages per day, per month
fig, ax = plt.subplots()
sns.lineplot(
    data=channels,
    x='day',
    y='number_of_messages',
    hue='month',
    palette='rocket'
)
plt.xticks(ticks=np.arange(7), labels=[
           'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'])
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
    hue='month',
    palette='rocket'
)

plt.ylabel('Total messages per day')
plt.xlabel('Date')
plt.legend(bbox_to_anchor=(1.0, 1.0), title='Month')
plt.savefig(f'{output_folder}channels_per_day.png')
