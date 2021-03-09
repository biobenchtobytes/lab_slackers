import os, re
import pandas as pd
import numpy as np
import names

from random import randint, sample
from loguru import logger

logger.info('Import OK')

output_folder = 'raw_data/'

if not os.path.exists(output_folder):
    os.mkdir(output_folder)


def random_with_N_digits(n):
    range_start = 10**(n-1)
    range_end = (10**n)-1
    return randint(range_start, range_end)


def randn_skew_fast(N, alpha=0.0, loc=0.0, scale=1.0):
    sigma = alpha / np.sqrt(1.0 + alpha**2) 
    u0 = np.random.randn(N)
    v = np.random.randn(N)
    u1 = (sigma*u0 + np.sqrt(1.0 - sigma**2)*v) * scale
    u1[u0 < 0] *= -1
    u1 = u1 + loc
    return u1

example_data = {}

# Prepare master students list
males = [names.get_full_name(gender='male') for x in range(6)]
females = [names.get_full_name(gender='female') for x in range(4)]


# Prepare per-person message posts
direct_messages = pd.DataFrame()
direct_messages['date'] = pd.date_range(start='1/1/2020', end='31/12/2020')
direct_messages['day'] = direct_messages['date'].dt.day_name()
for lab_member in males+females:
    direct_messages[lab_member] = [randint(0, 10) if day in ['Saturday', 'Sunday'] else randint(0, 25) for day in direct_messages['day'] ]

direct_messages = pd.melt(
    direct_messages,
    id_vars=['date', 'day'],
    value_vars=males + females,
    var_name='name',
    value_name='number_of_messages',
    )
direct_messages['gender'] = ['M' if name in males else 'F' for name in direct_messages['name']]


# Prepare per-channel messages
channel_messages = pd.DataFrame()
channel_messages['date'] = pd.date_range(start='1/1/2020', end='31/12/2020')
channel_messages['day'] = channel_messages['date'].dt.day_name()
for channel in ['general_gibberish', 'important_info', 'lab_laziness', 'exciting_experiments']:
    channel_messages[channel] = [randint(0, 20) if day in ['Saturday', 'Sunday'] else randint(0, 50) for day in channel_messages['day'] ]
channel_messages['lab_laziness'] = channel_messages['lab_laziness'] * 3
channel_messages['general_gibberish'] = channel_messages['general_gibberish'] * 5

# save to csv
direct_messages.to_csv(f'{output_folder}direct_messages.csv')
channel_messages.to_csv(f'{output_folder}channel_messages.csv')
