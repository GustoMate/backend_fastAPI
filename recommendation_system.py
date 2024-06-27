import pandas as pd
#from mlxtend.preprocessing import TransactionEncoder
from sklearn.metrics.pairwise import cosine_similarity
from scipy.sparse import csr_matrix
import ast
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import MinMaxScaler
import numpy as np
import re
from openai import OpenAI

# pd.set_option('display.max_columns', None)
# pd.set_option('display.max_colwidth', 1000)

data_low = pd.read_csv('beginner_recipe.csv')
data_mid = pd.read_csv('intermediate_recipe.csv')
data = pd.concat([data_low, data_mid], ignore_index=True)

units = ['?', '?', '??', '???', 'g', 'kg', 'ml', 'L', 'cc', 'cm', 'ea', '?', '?', '/', '??']
unit_pattern = '|'.join(units)
pattern = re.compile(rf'\d+|{unit_pattern}|\[.*?\]|\(.*?\)|[^?-?\s]')

def extract_ingredients(column_data):
    ingredients = []
    
    for item in column_data:
        if pd.notna(item):
            # ??? ??? ? ? ???? ??, ?? ?? ??
            items = item.strip('[]').split(',')
            for sub_item in items:
                # ??, ??, ?? ? ?? ?? ??
                cleaned_item = re.sub(pattern, '', sub_item).strip()
                # ? ?? ?? ??
                cleaned_item = cleaned_item.split()[0] if cleaned_item else ''
                if cleaned_item:
                    ingredients.append(cleaned_item)
    return ingredients

def combine_lists(row):
    combined = []
    for col in ['main_ingredients', 'sub_ingredients', 'seasoning']:
        combined.extend(row[col])
    return combined


data['main_ingredients'] = data['??? ??'].apply(lambda x: extract_ingredients([x]))
data['sub_ingredients'] = data['??? ??'].apply(lambda x: extract_ingredients([x]))
data['seasoning'] = data['??'].apply(lambda x: extract_ingredients([x]))

# ??? ??? ??? ??? ??
data['whole_ingredients'] = data.apply(combine_lists, axis=1)

def calculate_spiciness(row):
    score = 0
    spicy_ingredients = ['??', '??', '??', '????', '??']
    
    # ?? ???? ?? ?? ??
    if isinstance(row['?? ??'], str):
        for spicy in spicy_ingredients:
            if spicy in row['?? ??']:
                score += 3

    # ??? ???? ?? ?? ??
    if isinstance(row['??? ??'], str):
        row['??? ??'] = eval(row['??? ??'])
    
    if isinstance(row['??? ??'], list):
        for ingredient in row['??? ??']:
            if any(spicy in ingredient for spicy in spicy_ingredients):
                score += 1
                
    # ??? ???? ?? ?? ??
    if isinstance(row['??? ??'], str):
        row['??? ??'] = eval(row['??? ??'])
        
    if isinstance(row['??? ??'], list):
        for ingredient in row['??? ??']:
            if any(spicy in ingredient for spicy in spicy_ingredients):
                score += 1
    
    # ???? ?? ?? ??
    if isinstance(row['??'], str):
        row['??'] = eval(row['??'])
    
    if isinstance(row['??'], list):
        for ingredient in row['??']:
            if any(spicy in ingredient for spicy in spicy_ingredients):
                score += 1
                
    return score

data['spiciness'] = data.apply(calculate_spiciness, axis=1)

def is_low_calorie(calorie):
    return 1 if calorie <= 500 else 0

data['low_calorie'] = data['???'].apply(is_low_calorie)

difficulty_mapping = {
    '?? ??': 1,
    '??': 2,
    '??': 3,
    '???': 4
}

# ?? ??
data['difficulty'] = data['??? ??'].map(difficulty_mapping)

data_add_dummies = pd.get_dummies(data, columns=['?? ??'])
data_add_dummies = pd.get_dummies(data_add_dummies, columns=['?? ??'])
data_add_dummies = data_add_dummies.drop(['?? ??', '???', '??', '??? ??', '??? ??', '??', '???'], axis = 1)
data_add_dummies.rename(columns={'?? ??_?????':'is_southeast_asian', 
                                 '?? ??_???':'is_mexican', 
                                 '?? ??_??':'is_western', 
                                 '?? ??_????':'is_italian', 
                                 '?? ??_??':'is_japanese',
                                 '?? ??_??':'is_chinese',
                                 '?? ??_??':'is_mixed',
                                 '?? ??_??':'is_korean',
                                 '?? ??_??':'is_snack',
                                 '?? ??_????':'is_main',
                                 '?? ??_??':'is_side'                            
                                 },
                        inplace=True)

scaler = MinMaxScaler()
spiciness_2d = data_add_dummies['spiciness'].values.reshape(-1, 1)
difficulty_2d = data_add_dummies['difficulty'].values.reshape(-1, 1)

scaled_data = data_add_dummies
scaled_data['spiciness'] = scaler.fit_transform(spiciness_2d)
scaled_data['difficulty'] = scaler.fit_transform(difficulty_2d)

allergic_ingredients = ['??', '??'] # ???? ?? ?? ?? ?? ->DB?? ???
max_cooking_time = 30 # ?? ??

user_ingredients = ['???', '???', '????', '?', '?', '??', '???', '?', '??', '??', '??', '?', '??', '???', '??', '??', '??', '???', '???', '????', '??', '???', '????', '????', '???', '???']
market_ingredients = ['???', '?', '?', '??', '???', '?', '??', '??', '??', '?', '??', '???', '??', '??', '??', '???', '???', '????', '??', '???', '????', '????', '???', '???']
# ??? ??? ??
user_data = {
    'spiciness': [1], # (0, 0.2, 0.4, 0.6, 0.8, 1) ? ?? ?? ??? ???? ?
    'difficulty': [0.4],
    'low_calorie': [1],
    'is_southeast_asian': [0],
    'is_mexican': [1],
    'is_western': [0.5],
    'is_italian': [0.5],
    'is_japanese': [0.7],
    'is_chinese': [0],
    'is_mixed': [0],
    'is_korean': [0],
    'is_snack': [0],
    'is_main': [0],
    'is_side': [0]
}

user_df = pd.DataFrame(user_data)

def exclude_allergic_ingredients(row, allergic_ingredients):
    return not any(ingredient in row['whole_ingredients'] for ingredient in allergic_ingredients)

# ???
recommendation_df = scaled_data[scaled_data.apply(exclude_allergic_ingredients, axis=1, allergic_ingredients=allergic_ingredients)]
recommendation_df = recommendation_df[recommendation_df['????'] < max_cooking_time] 

# ????? A
def contains_all_ingredients(row, user_ingredients):
    return set(row['whole_ingredients']).issubset(set(user_ingredients))

recommendation_A_list = recommendation_df[recommendation_df.apply(contains_all_ingredients, axis=1, user_ingredients=user_ingredients)]
recommendation_A_list[['?? ??', 'whole_ingredients']]

def filter_recipes(row, user_ingredients, market_ingredients, max_additional_items=5):
    recipe_ingredients = set(row['whole_ingredients'])
    
    user_ingredients_set = set(user_ingredients)
    market_ingredients_set = set(market_ingredients)
    
    # ????? ??? ??? (???? ???? ??? ?????)
    missing_ingredients = recipe_ingredients - user_ingredients_set
    
    
    # ??? ?? ? ???? ?? ??? ??
    purchasable_items_in_market = missing_ingredients & market_ingredients_set

    # ??? ?? ? ???? ??? ??? ?? (purchasable_ingredients_in_market? ???)
    additional_items_needed = missing_ingredients - market_ingredients_set

    # ???? ??? ??? ???? ?? ??? ?? max_additional_items ??? ??? True
    can_make = len(missing_ingredients) <= max_additional_items

    return can_make, missing_ingredients, purchasable_items_in_market, additional_items_needed


def count_matching_ingredients(row, user_ingredients):
    recipe_ingredients = set(row['whole_ingredients'])
    matching_ingredients_count = len(recipe_ingredients & set(user_ingredients))
    return matching_ingredients_count


def count_missing_ingredients(row, user_ingredients):
    matching_ingredients_count = len(set(row['whole_ingredients']))
    # matching_ingredients_count = len(recipe_ingredients & set(user_ingredients))
    return matching_ingredients_count


# ???? ?????? ??
recommendation_df['matching_count'] = recommendation_df.apply(count_matching_ingredients, axis=1, user_ingredients=user_ingredients)
recommendation_df['missing_count'] = recommendation_df.apply(count_missing_ingredients, axis=1, user_ingredients=user_ingredients)

recommendation_df['can_make'], recommendation_df['missing_ingredients'], recommendation_df['purchasable_items_in_market'], recommendation_df['additional_items_needed']= zip(*recommendation_df.apply(filter_recipes, axis=1, user_ingredients=user_ingredients, market_ingredients=market_ingredients, max_additional_items=5))
recommendation_B_list = recommendation_df[recommendation_df['can_make']==True]

# ? ? ???? ??? ?? ??? ?? ???? ??, ??? ??? ?? ??? Top 20
recommendation_B_list = recommendation_B_list.sort_values(by='matching_count', ascending=False)[0:20]


recommendation_B_list = recommendation_B_list.sort_values(
    by=['matching_count', 'missing_count'],
    ascending=[False, True]
)

# ?? 20? ? ??
recommendation_B_list = recommendation_B_list.head(20)

weights = {
    'spiciness': 1.5,
    'difficulty': 0.8,
    'low_calorie': 0.5,
    'is_southeast_asian': 0.2,
    'is_mexican': 0.2,
    'is_western': 0.2,
    'is_italian': 0.2,
    'is_japanese': 0.2,
    'is_chinese': 0.2,
    'is_mixed': 0.2,
    'is_korean': 0.2,
    'is_snack': 1.0,
    'is_main': 1.0,
    'is_side': 1.0
}



recipe_df = recommendation_df[['spiciness',
                              'difficulty',
                              'low_calorie',
                              'is_southeast_asian',
                              'is_mexican',
                              'is_western',
                              'is_italian',
                              'is_japanese',
                              'is_chinese',
                              'is_mixed',
                              'is_korean',
                              'is_snack',
                              'is_main',
                              'is_side'
                              ]]

new_series = pd.Series(['???'])

updated_series = pd.concat([new_series, recommendation_df['?? ??']], ignore_index=True)

# ??? ??????? ?? ??????? ??? ??? ??
combined_df = pd.concat([user_df, recipe_df], ignore_index=True)

def apply_weights(df, weights):
    for column in df.columns:
        if column in weights:  # ????? ??? ????? ??
            df[column] = df[column] * weights[column]  # ??? ??
    return df

# ? DataFrame? ??? ??
combined_df = apply_weights(combined_df, weights)

# ??? ??? ??
similarity_matrix = cosine_similarity(combined_df)

# ??? ???? ?? ??? ?? ??? ??
similarity_df = pd.DataFrame(similarity_matrix, index=updated_series, columns=updated_series)

def get_top_similar_recipes(similarity_df, recipe_name, top_n=5):
    # ?? ??? ?? ??? ? ?? ? ??
    similar_scores = similarity_df[recipe_name].sort_values(ascending=False)
    # ?? top_n ?? ?? (?? ?? ??)
    top_similar = similar_scores.iloc[1:top_n+1]
    return top_similar

# ??: 'recipe1'? ?? ?? ?? ??? ?? ?? top 3 ?? ??
top_10_similar = get_top_similar_recipes(similarity_df, '???', top_n=10)
print(top_10_similar)

client = OpenAI(api_key = 'YOUR API KEY')
def recommend_menu(user_context, top_similar_recipes):
    # LLM? ???? 10?? ?? ?? ??? 3?? ??? ???? ??
    prompt = f"""
    You are a smart recipe recommender. Based on the user's context below, choose the 3 most suitable recipes from the given list. You have to consider user's mood and explain reasonable reason.

    User context: {user_context}

    Recipes:
    {', '.join(top_similar_recipes.index)}

    Provide the names of the 3 most suitable recipes and explain why you recommend each of them.
    Preferably, the number of 'items users should buy in market' should be greater than the number of 'additional items'.

    Format the response as:
    Recipe: <recipe name>
    Reason: <reason in Korean>
    items that users should buy in market: <purchasable_items_in_market>
    additional items: <additional_items_needed>

    """


    response = client.completions.create(
        model="gpt-3.5-turbo-instruct",
        prompt=prompt,
        max_tokens=800,
        temperature=0.7
    )
    response_text = response.choices[0].text.strip()
    recommendations = []
    items = response_text.split('\n\n')
    for item in items:
        if 'Recipe:' in item and 'Reason:' in item:
            recipe = item.split('Recipe:')[1].split('Reason:')[0].strip()
            reason = item.split('Reason:')[1].strip()
            recommendations.append((recipe, reason))

    return recommendations[:3]

# ??? ?? ??
user_context = "?? ???? ???? ???, ??? ?? ???. ??? ? ???? ??? ?? ??? ?? ?? ??, ???? ??? ??? ?? ????"

# ?? ??
recommended_menus = recommend_menu(user_context, top_10_similar)

for recipe, reason in recommended_menus:
    print(f"Recommended Menu: {recipe}\nReason: {reason}\n")
    