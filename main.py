from calorie_calculator import get_user_nutrition_data
from meal_planner import generate_meal_plan

print("\nWELCOME TO NUTRITION COACH AI\n")

# Step 1: Take user body details
nutrition = get_user_nutrition_data()

# Step 2: Show calculated results
print("\n📊 YOUR NUTRITION SUMMARY")
print(f"BMR: {nutrition['bmr']} calories/day")
print(f"TDEE: {nutrition['tdee']} calories/day")
print(f"Target Calories: {nutrition['calories']} calories/day")
print(f"Protein Target: {nutrition['protein']} g/day")

# Step 3: Ask if user wants diet plan
choice = input("\nDo you want a diet plan? (yes / no): ").lower()

if choice == "yes":
    generate_meal_plan(
        protein_target=nutrition["protein"],
        weight=nutrition["weight"]
    )
else:
    print("\n👍 Okay. Stay healthy!")