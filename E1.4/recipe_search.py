import pickle

def display_recipe(recipe):
    print("Recipe: " + recipe['name'])
    print("Cooking Time (min): " + str(recipe['cooking_time']))
    print("Ingredients:")

    for i in recipe['ingredients']:
        print(i)
    
    print("Difficulty: " + recipe['difficulty'])
    print()

def search_ingredient(data):
    for count, value in enumerate(data['all_ingredients']):
        print(count, value)
    
    print()

    try:
        index = int(input("Which ingredient would you like to search for? "))
    except:
        print("Something went wrong with your input. Are you sure it's a valid number?")
    else:
        ingredient_searched = data['all_ingredients'][index]
        for i in data['recipes_list']:
            if ingredient_searched in i['ingredients']:
                display_recipe(i)

file_name = str(input("What is the name of the file that holds your recipes? "))

try:
    my_file = open(file_name, 'rb')
    data = pickle.load(my_file)
except:
    print("Sorry, we couldn't find that file.")
else:
    search_ingredient(data)