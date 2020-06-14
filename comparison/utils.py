import datetime
from typing import Sequence

import numpy as np
import pandas


def generate_data(row_num=10):
    df = pandas.DataFrame(np.random.randint(10, 100, size=(row_num, 2)), columns=list('AB'))
    return df


def get_avro(topic: str, suffix: str = "") -> Sequence:
    return f'{topic}.key{suffix}', f'{topic}.value{suffix}'


def unix_time_millis(dt):
    return int((dt - datetime.datetime.utcfromtimestamp(0)).total_seconds() * 1000)
