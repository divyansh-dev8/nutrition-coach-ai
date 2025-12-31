import pandas as pd

data = pd.read_csv("data/nutrition_data.csv")

preference = input("Enter food preference (veg / non-veg): ")
lifestyle = input("Enter lifestyle (normal / luxury): ")

selected_food = data[
    (data["type"] == "food") &
    (data["category"] == preference) &
    (data["lifestyle"] == lifestyle)
]

print(selected_food)