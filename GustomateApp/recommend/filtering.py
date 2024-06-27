def exclude_allergic_ingredients(row, allergic_ingredients):
    return not any(ingredient in row['whole_ingredients'] for ingredient in allergic_ingredients)

def contains_all_ingredients(row, user_ingredients):
    return set(row['whole_ingredients']).issubset(set(user_ingredients))

def filter_recipes(row, user_ingredients, market_ingredients, max_additional_items=5):
    recipe_ingredients = set(row['whole_ingredients'])
    user_ingredients_set = set(user_ingredients)
    market_ingredients_set = set(market_ingredients)

    missing_ingredients = recipe_ingredients - user_ingredients_set
    purchasable_items_in_market = missing_ingredients & market_ingredients_set
    additional_items_needed = missing_ingredients - market_ingredients_set
    can_make = len(missing_ingredients) <= max_additional_items

    return can_make, missing_ingredients, purchasable_items_in_market, additional_items_needed

def count_matching_ingredients(row, user_ingredients):
    recipe_ingredients = set(row['whole_ingredients'])
    matching_ingredients_count = len(recipe_ingredients & set(user_ingredients))
    return matching_ingredients_count

def count_missing_ingredients(row, user_ingredients):
    matching_ingredients_count = len(set(row['whole_ingredients']))
    return matching_ingredients_count
