recipes_list = []

ingredients_list = []

def take_recipe():
    name = str(input("Enter recipe name: "))
    cooking_time = int(input("Enter recipe cooking time in minutes: "))
    ingredients = list(input("Enter recipe list of ingredients: ").split(", "))
    recipe = {'name':name, 'cooking_time':cooking_time, 'ingredients':ingredients}
    return recipe

n = int(input("How many recipes would you like to insert? "))

for i in range(0,n):
    recipe = take_recipe()
    print()
    for o in recipe['ingredients']:
        if not o in ingredients_list:
            ingredients_list.append(o)
    recipes_list.append(recipe)

for i in recipes_list:
    recipe = i

    print("Recipe: " + recipe['name'])
    print("Cooking Time (min): " + str(recipe['cooking_time']))
    print("Ingredients:")

    for i in recipe['ingredients']:
        print(i)

    difficulty = ""

    if recipe['cooking_time'] < 10:
        if len(recipe['ingredients']) < 4:
            difficulty = "Easy"
        else:
            difficulty = "Medium"
    else:
        if len(recipe['ingredients']) < 4:
            difficulty = "Intermediate"
        else:
            difficulty = "Hard"
            
    print("Difficulty Level: " + difficulty)
    print("")

print("Ingredients List")
print("-------------------------------------------")
ingredients_list.sort()
for i in ingredients_list:
    print(i)
