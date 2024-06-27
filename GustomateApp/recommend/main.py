import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics.pairwise import cosine_similarity
from openai import OpenAI

from data_loader import load_data, preprocess_data
from feature_engineering import extract_ingredients, combine_lists, calculate_spiciness, is_low_calorie
from filtering import exclude_allergic_ingredients, contains_all_ingredients, filter_recipes, count_matching_ingredients, count_missing_ingredients
from recommendation import apply_weights, get_top_similar_recipes, recommend_menu
from utils import create_user_dataframe

# Load and preprocess data
data = load_data()
data, pattern = preprocess_data(data)

# Extract and combine ingredients
data['main_ingredients'] = data['주재료 이름'].apply(lambda x: extract_ingredients([x], pattern))
data['sub_ingredients'] = data['부재료 이름'].apply(lambda x: extract_ingredients([x], pattern))
data['seasoning'] = data['양념'].apply(lambda x: extract_ingredients([x], pattern))
data['whole_ingredients'] = data.apply(combine_lists, axis=1)

# Calculate spiciness and low calorie
data['spiciness'] = data.apply(calculate_spiciness, axis=1)
data['low_calorie'] = data['칼로리'].apply(is_low_calorie)

# Mapping difficulty
difficulty_mapping = {'매우 쉬움': 1, '쉬움': 2, '보통': 3, '어려움': 4}
data['difficulty'] = data['난이도 분류'].map(difficulty_mapping)

# One-hot encoding and scaling
data_add_dummies = pd.get_dummies(data, columns=['국가 분류', '테마 분류']).drop(['방법 분류', '조회수', '분량', '주재료 이름', '부재료 이름', '양념', '레시피'], axis=1)

# Renaming columns
data_add_dummies.rename(columns={'국가 분류_동남아시아': 'is_southeast_asian', 
                                 '국가 분류_멕시코': 'is_mexican', 
                                 '국가 분류_서양': 'is_western', 
                                 '국가 분류_이탈리아': 'is_italian', 
                                 '국가 분류_일본': 'is_japanese',
                                 '국가 분류_중국': 'is_chinese',
                                 '국가 분류_퓨전': 'is_mixed',
                                 '국가 분류_한식': 'is_korean',
                                 '테마 분류_간식': 'is_snack',
                                 '테마 분류_메인요리': 'is_main',
                                 '테마 분류_반찬': 'is_side'                            
                                 }, inplace=True)

scaler = MinMaxScaler()
data_add_dummies['spiciness'] = scaler.fit_transform(data_add_dummies['spiciness'].values.reshape(-1, 1))
data_add_dummies['difficulty'] = scaler.fit_transform(data_add_dummies['difficulty'].values.reshape(-1, 1))

# Define user data
user_ingredients = ['참나물', '고추장', '고추가루', '굴', '쌀', '대추', '보리쌀', '콩', '생강', '마늘', '현미', '잣', '호두', '아몬드', '고추', '참깨', '된장', '쌀국수', '바지락', '파프리카', '숙주', '식용유', '다진마늘', '말린고추', '해선장', '굴소스']
market_ingredients = ['오징어', '굴', '쌀', '대추', '보리쌀', '콩', '생강', '마늘', '현미', '잣', '호두', '아몬드', '고추', '참깨', '된장', '쌀국수', '바지락', '파프리카', '숙주', '식용유', '다진마늘', '말린고추', '해선장', '굴소스']
user_data = {
    'spiciness': [1], 'difficulty': [0.4], 'low_calorie': [1], 'is_southeast_asian': [0], 'is_mexican': [1],
    'is_western': [0.5], 'is_italian': [0.5], 'is_japanese': [0.7], 'is_chinese': [0], 'is_mixed': [0],
    'is_korean': [0], 'is_snack': [0], 'is_main': [0], 'is_side': [0]
}
user_df = create_user_dataframe(user_data)

# Filter data
allergic_ingredients = ['계란', '달걀']
max_cooking_time = 30
recommendation_df = data_add_dummies[data_add_dummies.apply(exclude_allergic_ingredients, axis=1, allergic_ingredients=allergic_ingredients)]
recommendation_df = recommendation_df[recommendation_df['조리시간'] < max_cooking_time]

# Recommendation A
recommendation_A_list = recommendation_df[recommendation_df.apply(contains_all_ingredients, axis=1, user_ingredients=user_ingredients)]

recommendation_df['matching_count'] = recommendation_df.apply(count_matching_ingredients, axis=1, user_ingredients=user_ingredients)
recommendation_df['missing_count'] = recommendation_df.apply(count_missing_ingredients, axis=1, user_ingredients=user_ingredients)
recommendation_df['can_make'], recommendation_df['missing_ingredients'], recommendation_df['purchasable_items_in_market'], recommendation_df['additional_items_needed'] = zip(*recommendation_df.apply(filter_recipes, axis=1, user_ingredients=user_ingredients, market_ingredients=market_ingredients, max_additional_items=5))

# Recommendation B
recommendation_B_list = recommendation_df[recommendation_df['can_make'] == True].sort_values(by=['matching_count', 'missing_count'], ascending=[False, True]).head(20)
weights = {
    'spiciness': 1.5, 'difficulty': 0.8, 'low_calorie': 0.5, 'is_southeast_asian': 0.2, 'is_mexican': 0.2,
    'is_western': 0.2, 'is_italian': 0.2, 'is_japanese': 0.2, 'is_chinese': 0.2, 'is_mixed': 0.2, 'is_korean': 0.2,
    'is_snack': 1.0, 'is_main': 1.0, 'is_side': 1.0
}

recipe_df = recommendation_df[[
    'spiciness', 'difficulty', 'low_calorie', 'is_southeast_asian', 'is_mexican', 'is_western',
    'is_italian', 'is_japanese', 'is_chinese', 'is_mixed', 'is_korean', 'is_snack', 'is_main', 'is_side'
]]

new_series = pd.Series(['사용자'])
updated_series = pd.concat([new_series, recommendation_df['메뉴 이름']], ignore_index=True)
combined_df = pd.concat([user_df, recipe_df], ignore_index=True)
combined_df = apply_weights(combined_df, weights)

similarity_matrix = cosine_similarity(combined_df)
similarity_df = pd.DataFrame(similarity_matrix, index=updated_series, columns=updated_series)
top_10_similar = get_top_similar_recipes(similarity_df, '사용자', top_n=10)

client = OpenAI(api_key='YOUR API KEY')
user_context = "오늘 아침에는 토스트를 먹었고, 커피를 두잔 마셨어. 지금은 좀 피곤해서 요리에 많은 시간을 쏟고 싶지 않고, 저녁에는 치킨과 맥주를 먹을 예정이야"
recommended_menus = recommend_menu(client, user_context, top_10_similar)

for recipe, reason in recommended_menus:
    print(f"Recommended Menu: {recipe}\nReason: {reason}\n")