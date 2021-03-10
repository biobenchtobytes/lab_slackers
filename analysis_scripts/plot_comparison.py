import os
import re
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from loguru import logger

logger.info('Import OK')

input_path = 'raw_data/'
output_folder = 'results/comparison/'


direct = pd.read_csv(f'{input_path}direct_messages.csv')
direct.drop([col for col in direct.columns.tolist() if 'Unnamed: ' in col], axis=1, inplace=True)

# Add month column, clean column types
direct['date'] = pd.to_datetime(direct['date'])
direct['month'] = pd.to_datetime(direct.set_index('date').index).month
direct['month_name'] = pd.to_datetime(direct.set_index('date').index).month_name()
direct['day_name'] = direct['day']
direct['day'] = direct['day'].map(dict(zip(['Thursday', 'Friday', 'Saturday', 'Sunday', 'Monday', 'Tuesday', 'Wednesday', ], np.arange(0,7))))

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

# compare channels vs direct messages
channels['type'] = 'channel'
channels['name'] = channels['channel']
direct['type'] = 'direct'

comparison = pd.concat(direct, channels)

fig, ax = plt.subplots()
sns.boxplot(
    data=comparison,
    x='day',
    y='number_of_messages',
    hue='type')

plt.ylabel('Messages per day')
plt.xlabel('Day')
plt.xticks(ticks=np.arange(3), labels=[
           'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'], rotation=45)
plt.legend(bbox_to_anchor=(1.0, 1.0), title='Message type')
plt.savefig(f'{output_path}messages_per_type.png')