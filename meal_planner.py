import pandas as pd


def generate_meal_plan(protein_target, weight, preference, lifestyle):
    data = pd.read_csv("data/nutrition_data.csv")

    max_protein = int(2.5 * weight)
    if protein_target > max_protein:
        protein_target = max_protein

    if preference == "both":
        category_filter = data["category"].isin(["veg", "non-veg"])
    else:
        category_filter = data["category"] == preference

    food_data = data[
        (data["type"] == "food") &
        category_filter &
        (data["lifestyle"] == lifestyle)
    ]

    protein_foods = food_data[food_data["protein"] >= 5].sort_values(
        by="protein", ascending=False
    )

    if protein_foods.empty:
        protein_foods = data[
            (data["type"] == "food") &
            category_filter &
            (data["protein"] >= 5)
        ].sort_values(by="protein", ascending=False)

    meal_split = {
        "Breakfast": 0.25,
        "Lunch": 0.30,
        "Dinner": 0.30,
        "Snacks": 0.15
    }

    plan = {}

    foods = protein_foods.head(6).reset_index(drop=True)
    idx = 0

    for meal, ratio in meal_split.items():
        meal_protein = protein_target * ratio
        food = foods.iloc[idx % len(foods)]
        servings = meal_protein / food["protein"]

        plan[meal] = {
            "item": food["item"],
            "servings": int(servings),
            "protein": int(meal_protein)
        }

        idx += 1

    return plan