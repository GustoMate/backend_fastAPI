import re
import pandas as pd

def extract_ingredients(column_data, pattern):
    ingredients = []
    
    for item in column_data:
        if pd.notna(item):
            items = item.strip('[]').split(',')
            for sub_item in items:
                cleaned_item = re.sub(pattern, '', sub_item).strip()
                cleaned_item = cleaned_item.split()[0] if cleaned_item else ''
                if cleaned_item:
                    ingredients.append(cleaned_item)
    return ingredients

def combine_lists(row):
    combined = []
    for col in ['main_ingredients', 'sub_ingredients', 'seasoning']:
        combined.extend(row[col])
    return combined

def calculate_spiciness(row):
    score = 0
    spicy_ingredients = ['매운', '고추', '김치', '고춧가루', '얼큰']
    
    if isinstance(row['메뉴 이름'], str):
        for spicy in spicy_ingredients:
            if spicy in row['메뉴 이름']:
                score += 3

    if isinstance(row['주재료 이름'], str):
        row['주재료 이름'] = eval(row['주재료 이름'])
    
    if isinstance(row['주재료 이름'], list):
        for ingredient in row['주재료 이름']:
            if any(spicy in ingredient for spicy in spicy_ingredients):
                score += 1

    if isinstance(row['부재료 이름'], str):
        row['부재료 이름'] = eval(row['부재료 이름'])
        
    if isinstance(row['부재료 이름'], list):
        for ingredient in row['부재료 이름']:
            if any(spicy in ingredient for spicy in spicy_ingredients):
                score += 1

    if isinstance(row['양념'], str):
        row['양념'] = eval(row['양념'])
    
    if isinstance(row['양념'], list):
        for ingredient in row['양념']:
            if any(spicy in ingredient for spicy in spicy_ingredients):
                score += 1
                
    return score

def is_low_calorie(calorie):
    return 1 if calorie <= 500 else 0