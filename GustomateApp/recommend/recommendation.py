import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

def apply_weights(df, weights):
    for column in df.columns:
        if column in weights:
            df[column] = df[column] * weights[column]
    return df

def get_top_similar_recipes(similarity_df, recipe_name, top_n=5):
    similar_scores = similarity_df[recipe_name].sort_values(ascending=False)
    top_similar = similar_scores.iloc[1:top_n+1]
    return top_similar

def recommend_menu(client, user_context, top_similar_recipes):
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
