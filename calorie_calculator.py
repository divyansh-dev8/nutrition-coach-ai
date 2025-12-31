def calculate_nutrition(age, weight, height, gender, activity_level, goal):
    """
    Returns daily calories and protein requirement
    """

    # ---- BMR Calculation (Mifflin-St Jeor) ----
    if gender.lower() == "male":
        bmr = 10 * weight + 6.25 * height - 5 * age + 5
    else:
        bmr = 10 * weight + 6.25 * height - 5 * age - 161

    # ---- Activity Multiplier ----
    activity_map = {
        "low": 1.2,
        "medium": 1.55,
        "high": 1.75
    }

    tdee = bmr * activity_map.get(activity_level, 1.2)

    # ---- Goal Adjustment ----
    if goal == "fat_loss":
        calories = tdee - 500
        protein = weight * 2.0
    elif goal == "muscle_gain":
        calories = tdee + 300
        protein = weight * 2.2
    else:  # maintenance
        calories = tdee
        protein = weight * 1.8

    return round(calories), round(protein)