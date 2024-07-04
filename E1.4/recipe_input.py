import pickle

def calc_difficulty(recipe):
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
    
    return difficulty

def take_recipe():
    name = str(input("Enter recipe name: "))
    cooking_time = int(input("Enter recipe cooking time in minutes: "))
    ingredients = list(input("Enter recipe list of ingredients: ").split(", "))
    recipe = {'name':name, 'cooking_time':cooking_time, 'ingredients':ingredients}
    difficulty = calc_difficulty(recipe)
    recipe['difficulty'] = difficulty
    
    return recipe

file_name = str(input("What's the name of the file you want to open/create? "))

try:
    my_file = open(file_name, 'rb')
    data = pickle.load(my_file)
except FileNotFoundError:
    data = { 'recipes_list':[], 'all_ingredients': [] }
except:
    print("An unforeseen error has occurred.")
    data = { 'recipes_list':[], 'all_ingredients': [] }
else:
    my_file.close()
finally:
    recipes_list, all_ingredients = data['recipes_list'],data['all_ingredients']

n = int(input("How many recipes would you like to insert? "))

for i in range(0,n):
    recipe = take_recipe()
    print()
    for o in recipe['ingredients']:
        if o not in all_ingredients:
            all_ingredients.append(o)
    recipes_list.append(recipe)

data = {'recipes_list':recipes_list,'all_ingredients':all_ingredients}

update_file = open(file_name, 'wb')
pickle.dump(data, update_file)
update_file.close()