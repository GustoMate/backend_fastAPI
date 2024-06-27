import pandas as pd
import re

def load_data():
    data_low = pd.read_csv('beginner_recipe.csv')
    data_mid = pd.read_csv('intermediate_recipe.csv')
    data = pd.concat([data_low, data_mid], ignore_index=True)
    return data

def preprocess_data(data):
    units = ['컵', '개', '큰술', '작은술', 'g', 'kg', 'ml', 'L', 'cc', 'cm', 'ea', '와', '과', '/', '약간']
    unit_pattern = '|'.join(units)
    pattern = re.compile(rf'\d+|{unit_pattern}|\[.*?\]|\(.*?\)|[^가-힣\s]')

    return data, pattern
