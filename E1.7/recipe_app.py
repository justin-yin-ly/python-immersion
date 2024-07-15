from sqlalchemy import create_engine, Column
from sqlalchemy.types import Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Create the engine that will connect to the database
engine = create_engine("mysql://cf-python:password@localhost/task_database")

Base = declarative_base()

# The Recipe Class - Holds the data and functions for the recipes the user will create
class Recipe(Base):
    __tablename__ = "Recipes"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50))
    ingredients = Column(String(255))
    cooking_time = Column(Integer)
    difficulty = Column(String(20))

    # Representation; what we use to quickly show a recipe for debugging purposes
    def __repr__(self):
        return "Recipe ID: " + str(self.id) + " | Name: " + self.name + " | Difficulty: " + self.difficulty + ">"
    
    # String Representation; what we use to show the recipe to the user
    def __str__(self):
        return f"Recipe: {self.name}\n \tID: {self.id}\n \tIngredients: {self.ingredients} \n \tCooking Time: {self.cooking_time} \n \tDifficulty: {self.difficulty} \n"

    # Calculate difficulty based on number of ingredients and cooking time
    def calculate_difficulty(self):
        ingredients_list = self.return_ingredients_as_list()
        if self.cooking_time < 10:
            if len(ingredients_list) < 4:
                self.difficulty = "Easy"
            else:
                self.difficulty = "Medium"
        else:
            if len(ingredients_list) < 4:
                self.difficulty = "Intermediate"
            else:
                self.difficulty = "Hard"
    
    # Since ingredients are inserted as a string, this helps quickly retrieve the ingredients as a list instead
    def return_ingredients_as_list(self):
        if not self.ingredients:
            return []
        else:
            return self.ingredients.split(", ")

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)

session = Session()


def create_recipe():
    while True:
        # User enters the recipe's name - input validation needs to check that it's within the character limit, and that it's only letters
        name = str(input("Enter the recipe's name: "))
        if 0 < len(name) <= 50:
            break
        else:
            print("The name needs to be within 1 to 50 characters.") 
    
    while True:
        # User enters the recipe's cooking time - input validation checks that it's an integer
        cooking_time = input("Enter the recipe's cooking time: ")
        if cooking_time.isnumeric():
            # Cast input to integer when we verify that it's valid
            cooking_time = int(cooking_time)
            break
        else:
            print("The cooking time must be an integer.")
    
    ingredients = []
    while True:
        # User enters the ingredients list - they enter ingredients one at a time in a forloop
        num = str(input("How many ingredients would you like to input? "))
        if num.isnumeric() and int(num) > 0:
            num = int(num)
            break
        else:
            print("Input a number that's greater than 0.")
    
    for i in range(0, num):
        ingredient = input("Enter ingredient: ")
        ingredients.append(ingredient)
    ingredients_to_str = ", ".join(ingredients)
    
    # Create a new recipe entry based on the information the user put in
    recipe_entry = Recipe(name=name,ingredients=ingredients_to_str,cooking_time=cooking_time)
    recipe_entry.calculate_difficulty()

    # Attempt to push the entry to the database
    session.add(recipe_entry)
    session.commit()
    print("\n" + name + " recipe was added to the database!\n")

def view_all_recipes():
    # Get the complete list from the database
    all_recipes = session.query(Recipe).all()
    # Prints out a message if no recipes were found
    if not all_recipes:
        print("Couldn't find any recipes in the database. Start making some!\n")
        return
    # Call the string representation method for any recipes found
    print("Found " + str(len(all_recipes)) + " recipes | Displaying now... \n")
    for i in all_recipes:
        print(i.__str__())
    # Notify the user where the end of the list is
    print("-"*10 + "[End of recipes]" + "-"*10 + "\n")

def search_by_ingredients():
    # If no recipes are found, there's no need to continue with the rest of the code here; break out of the function and return to the main menu
    if not session.query(Recipe).count():
        print("Couldn't find any recipes in the database. Start making some!\n")
        return
    
    results = session.query(Recipe.ingredients).all()

    all_ingredients = []

    for i in results:
        temp_list = i.ingredients.split(", ")
        for o in temp_list:
            if not o in all_ingredients:
                all_ingredients.append(o)
    
    all_ingredients.sort()

    print("Found the following ingredients: \n")
    for count,value in enumerate(all_ingredients):
        print(count, value)
    
    # Get user input and validate it while doing so - entries should be numbers between 0 and the length of the list (-1)
    while True:
        try:
            ingredient_choices = input("Enter the indexes of the ingredients you want to look for, separated by a space: ").split()
            ingredient_indexes_to_int = [int(i) for i in ingredient_choices]
            if all(-1 < index < len(all_ingredients) for index in ingredient_indexes_to_int):
                break
            else:
                print("One or more of your choices was outside of the accepted range. Try again.\n")
        except ValueError:
            print("You entered something that wasn't a number. Try again.\n")
    
    # Get the ingredients to look for as strings
    search_ingredients = []
    for i in ingredient_indexes_to_int:
        search_ingredients.append(all_ingredients[i])

    # Assemble a list of conditions for our database query
    conditions = []
    for i in search_ingredients:
        like_term = "%" + i + "%"
        conditions.append(Recipe.ingredients.like(like_term))

    # Query the database and call the string representation method on all recipes found
    search_results = session.query(Recipe).filter(*conditions).all()
    print("Found the following recipes with the ingredients you requested: \n")
    for i in search_results:
        print(i.__str__())
    print()

def edit_recipe():
    # If there are no recipes to edit, exit the function
    if not session.query(Recipe).count():
        print("Couldn't find any recipes in the database. Start making some!\n")
        return
    
    # Get the complete list from the database
    all_recipes = session.query(Recipe).all()
    print("-"*10 + "Recipes in the database" + "-"*10)
    for i in all_recipes:
        print("ID: " + str(i.id) + " | Name: " + i.name)

    while True:
        try:
            edit_id = int(input("Enter the id of the recipe you want to edit: "))
            recipe_to_edit = session.query(Recipe).get(edit_id)
            if recipe_to_edit:
                break
            else:
                print("Couldn't find recipe with index of " + str(edit_id))
        except ValueError:
            print("You need to enter a number.")
    print("1 Name: " + recipe_to_edit.name + "\n2 Ingredients: " + recipe_to_edit.ingredients + "\n3 Cooking Time: " + str(recipe_to_edit.cooking_time))
    while True:
        try:
            attribute = int(input("Which attribute will you edit? (Pick a number) "))
            if 0 < attribute < 4:
                break
            else:
                print("You need to pick from 1, 2, or 3")
        except ValueError:
            print("You need to enter a number")
    
    if attribute == 1:
        while True:
            new_name = str(input("Enter the recipe's new name: "))
            if 0 < len(new_name) <= 50:
                recipe_to_edit.name = new_name
                print("Name updated!\n")
                break
            else:
                print("The name needs to be within 1 to 50 characters.") 
    elif attribute == 2:
        new_ingredients = []
        while True:
            # User enters the ingredients list - they enter ingredients one at a time in a forloop
            num = input("How many ingredients would you like to input?")
            if num.isnumeric() and int(num) > 0:
                num = int(num)
                break
            else:
                print("Input a number that's greater than 0.")
        
        for i in range(0, num):
            ingredient = input("Enter ingredient: ")
            new_ingredients.append(ingredient)
        new_ingredients_to_str = ", ".join(new_ingredients)
        recipe_to_edit.ingredients = new_ingredients_to_str
        recipe_to_edit.calculate_difficulty()
        print("Ingredients list updated!\n")
        
    elif attribute == 3:
        while True:
            # User enters the recipe's cooking time - input validation checks that it's an integer
            new_cooking_time = input("Enter the recipe's cooking time: ")
            if new_cooking_time.isnumeric():
                # Cast input to integer when we verify that it's valid
                recipe_to_edit.cooking_time = int(new_cooking_time)
                recipe_to_edit.calculate_difficulty()
                print("Cooking time  updated!\n")
                break
            else:
                print("The cooking time must be an integer.")
    
    session.commit()

def delete_recipe():
    # If there are no recipes to edit, exit the function
    if not session.query(Recipe).count():
        print("Couldn't find any recipes in the database. Start making some!\n")
        return
    
    # Get the complete list from the database
    all_recipes = session.query(Recipe).all()
    print("-"*10 + "Recipes in the database" + "-"*10)
    for i in all_recipes:
        print("ID: " + str(i.id) + " | Name: " + i.name)    

    # Get ID of the recipe to delete from the user
    while True:
        try:
            delete_id = int(input("Enter the id of the recipe you want to DELETE: "))
            recipe_to_delete = session.query(Recipe).get(delete_id)
            if recipe_to_delete:
                break
            else:
                print("Couldn't find recipe with index of " + str(delete_id))
        except ValueError:
            print("You need to enter a number.")
    
    # Display the recipe and then ask the user for confirmation of deletion
    print("Found the following recipe:")
    print(recipe_to_delete.__str__())
    print("\nAre you SURE you want to permanently DELETE this recipe? \n\t 1. Yes \n\t 2. No")
    while True:
        try:
            choice = int(input("(Type 1 for Yes and 2 for No) "))
            if 0 < choice < 3:
                break
            else:
                print("You need to pick from 1 or 2")
        except ValueError:
            print("You need to enter a number")
    
    if choice == 1:
        session.delete(recipe_to_delete)
        session.commit()
        print("Recipe deleted.\n")
    elif choice == 2:
        print("Deletion cancelled. Returning to main menu...\n")

# Main Menu logic
def main_menu():
    choice = ""
    while(choice != "quit"):
        print("--- [RECIPE APP MAIN MENU] ---")
        print("1. Create a recipe.")
        print("2. View all recipes.")
        print("3. Search for a recipe.")
        print("4. Edit an existing recipe.")
        print("5. Delete an existing recipe.\n")
        print("(Type quit to quit the app)\n")

        choice = input("What'll it be? ")
        print()

        if choice == '1':
            create_recipe()
        elif choice == '2':
            view_all_recipes()
        elif choice == '3':
            search_by_ingredients()
        elif choice == '4':
            edit_recipe()
        elif choice == '5':
            delete_recipe()
        elif choice == "quit":
            # Close the database session when the app is done
            print("Exiting app -- Goodbye!")
            session.close()
            engine.dispose()
        else:
            print("Sorry, I didn't quite get that.")

main_menu()