import os
import re
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from loguru import logger

logger.info('Import OK')

input_path = 'raw_data/'
output_folder = 'results/direct/'

if not os.path.exists(output_folder):
    os.makedirs(output_folder)

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
    data=direct_messages,
    x='day',
    y='number_of_messages',
    hue='month',
    palette='rocketship'
)
plt.xticks(ticks=np.arange(7), labels=[
           'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'])
plt.ylabel('Mean messages per day')
plt.xlabel('Day')
plt.legend(bbox_to_anchor=(1.0, 1.0), title='Month')
plt.savefig(f'{output_folder}messages_per_day.png')

# Scatterplot of messages per day
fig, ax = plt.subplots()
sns.beeswarmplot(
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
    data=direct.groupby('month', 'name').sum().reset_index(),
    x='month',
    y='number_of_messages',
    hue='name')
plt.xticks(ticks=np.arange(12), labels=
           direct.groupby(['month', 'month_name']).sum().reset_index()['month_name'].tolist(), rotation=45)
plt.ylabel('Total messages per month')
plt.xlabel('Month')
plt.legend(bbox_to_anchor=(1.0, 1.0), title='Lab member')
plt.savefig(f'{output_folder}messages_per_member.png')
