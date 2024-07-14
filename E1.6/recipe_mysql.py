import mysql.connector

conn = mysql.connector.connect(
    host = 'localhost',
    user = 'cf-python',
    passwd = 'password'
)

cursor = conn.cursor()

cursor.execute("CREATE DATABASE IF NOT EXISTS task_database")

cursor.execute("USE task_database")

cursor.execute('''CREATE TABLE IF NOT EXISTS Recipes(
id INT PRIMARY KEY AUTO_INCREMENT,
name VARCHAR(50),
ingredients VARCHAR(255),
cooking_time INT,
difficulty VARCHAR(20)
)
''')

def create_recipe(conn,cursor):
    name = str(input("Name of the recipe: "))
    cooking_time = int(input("How long to cook: "))
    ingredients = list(input("List of ingredients: ").split(", "))

    difficulty = calculate_difficulty(cooking_time, ingredients)

    ingredients_to_str = ", ".join(ingredients)

    sql = "INSERT INTO Recipes (name, ingredients, cooking_time, difficulty) VALUES (%s, %s, %s, %s)"
    val = (name, ingredients_to_str, cooking_time, difficulty)

    cursor.execute(sql, val)

    conn.commit()

    print("Your " + name + " recipe has been added to the Recipes table.\n")

def search_recipe(conn,cursor):
    all_ingredients = []

    cursor.execute("SELECT ingredients FROM Recipes")
    results = cursor.fetchall()

    for ingredients in results:
        for recipe_ingredients in ingredients:
            ingredients_to_list = recipe_ingredients.split(', ')
            for i in ingredients_to_list:
                if not i in all_ingredients:
                    all_ingredients.append(i)
    
    all_ingredients.sort()

    print("Found the following ingredients:")
    for count, value in enumerate(all_ingredients):
        print(count, value)

    ingredient_index = int(input("Which ingredient would you like to search for? "))
    search_ingredient = all_ingredients[ingredient_index]

    sql = ("SELECT * FROM Recipes WHERE ingredients LIKE %s")
    val = ("%" + search_ingredient + "%",)

    cursor.execute(sql, val)

    results = cursor.fetchall()

    print("Found the following recipes with " + search_ingredient + " as an ingredient: \n")
    display_recipes(results)

def update_recipe(conn,cursor):
    cursor.execute("SELECT * FROM Recipes")
    results = cursor.fetchall()
    display_recipes(results)

    recipe_id = int(input("Enter ID of recipe to change: "))

    cursor.execute("SELECT * FROM Recipes WHERE id LIKE " + str(recipe_id))
    result = cursor.fetchall()[0]

    column_to_change = str(input("What will you be updating for the " + result[1] + " recipe (name, cooking_time, ingredients)?"))

    if column_to_change == "name":
        new_name = str(input("What is this recipe's new name? "))
        update_one_field("name",new_name,recipe_id)

    elif column_to_change == "cooking_time":
        new_time = int(input("What is this recipe's new cooking time? "))
        update_one_field("cooking_time",new_time,recipe_id)

        ingredients_to_list = result[2].split(", ")
        new_difficulty = calculate_difficulty(new_time, ingredients_to_list)
        update_one_field("difficulty",new_difficulty,recipe_id)

    elif column_to_change == "ingredients":
        new_ingredients = list(input("What is this recipe's new ingredients list? ").split(", "))
        new_ingredients_to_str = ", ".join(new_ingredients)
        update_one_field("ingredients",new_ingredients_to_str,recipe_id)

        new_difficulty = calculate_difficulty(result[3], new_ingredients)
        update_one_field("difficulty",new_difficulty,recipe_id)

    else:
        print("Sorry, that field wasn't recognized.")
        return
    
    print("Recipe successfully updated!")
    conn.commit()
    print()


def update_one_field(field,value,id):
    sql = "UPDATE Recipes SET " + field + " = %s WHERE id = %s"
    val = (value, id)
    cursor.execute(sql, val)

def delete_recipe(conn,cursor):
    cursor.execute("SELECT * FROM Recipes")
    results = cursor.fetchall()

    display_recipes(results)

    recipe_id = int(input("What is the ID of the recipe you want to DELETE? "))

    cursor.execute("DELETE FROM Recipes WHERE id = " + str(recipe_id))

    conn.commit()
    print("Recipe deleted.")


def display_recipes(recipes):
    for i in recipes:
        print("ID: " + str(i[0]))
        print("Name: " + i[1])
        print("Ingredients: " + i[2])
        print("Cooking Time: " + str(i[3]))
        print("Difficulty: " + i[4])
        print()

def calculate_difficulty(cooking_time, ingredients):
    difficulty = ""
    if cooking_time < 10:
        if len(ingredients) < 4:
            difficulty = "Easy"
        else:
            difficulty = "Medium"
    else:
        if len(ingredients) < 4:
            difficulty = "Intermediate"
        else:
            difficulty = "Hard"

    return difficulty

def main_menu(conn,cursor):
    choice = ""
    while(choice != "quit"):
        print("-- RECIPE APP MAIN MENU --")
        print("1. Create a recipe.")
        print("2. Search for a recipe.")
        print("3. Update an existing recipe.")
        print("4. Delete an existing recipe.")

        choice = input("What'll it be? ")
        print()

        if choice == '1':
            create_recipe(conn,cursor)
        elif choice == '2':
            search_recipe(conn,cursor)
        elif choice == '3':
            update_recipe(conn,cursor)
        elif choice == '4':
            delete_recipe(conn,cursor)
        elif choice == "quit":
            print("Exiting app -- Goodbye!")
        else:
            print("Sorry, I didn't quite get that.")

main_menu(conn,cursor)