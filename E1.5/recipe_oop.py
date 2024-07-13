class Recipe(object):
    all_ingredients = []
    
    def __init__(self, name, cooking_time, ingredients):
        self.name = name
        self.cooking_time = cooking_time
        self.ingredients = ingredients
        self.difficulty = None
    
    def get_ingredients(self):
        return self.ingredients

    def get_difficulty(self):
        if not self.difficulty:
            self.difficulty = self.calculate_difficulty()
        return self.difficulty

    def calculate_difficulty(self):
        difficulty = ""

        if self.cooking_time < 10:
            if len(self.ingredients) < 4:
                difficulty = "Easy"
            else:
                difficulty = "Medium"
        else:
            if len(self.ingredients) < 4:
                difficulty = "Intermediate"
            else:
                difficulty = "Hard"
    
        return difficulty

    def add_ingredients(self, *ingredients):
        for i in ingredients:
            self.ingredients.append(i)
        self.update_all_ingredients()

    def update_all_ingredients(self):
        for ingredient in self.ingredients:
            if not ingredient in all_ingredients:
                all_ingredients.append(ingredient)

    def search_ingredient(self, ingredient):
        return ingredient in self.ingredients

    def __str__(self):
        output = "Recipe: " + self.name + "\nCooking Time (min): " + str(self.cooking_time) + "\nIngredients: "
        for i in self.ingredients:
            output += "\n" + i
        output += "\nDifficulty: " + self.get_difficulty() + "\n"
        return output

def recipe_search(data, search_term):
    print("Looking for recipes with: " + search_term)
    for i in data:
        if i.search_ingredient(search_term):
            print(i)

tea = Recipe("Tea",5,["Tea Leaves","Sugar","Water"])
print(tea)

coffee = Recipe("Coffee",5,["Coffee Powder","Sugar","Water"])
print(coffee)

cake = Recipe("Cake",50,["Sugar","Butter","Eggs","Vanilla Essence","Flour","Baking Powder","Milk"])
print(cake)

banana_smoothie = Recipe("Banana Smoothie",5,["Bananas","Milk","Peanut Butter","Sugar","Ice Cubes"])
print(banana_smoothie)

recipes_list = [tea,coffee,cake,banana_smoothie]

for i in ["Water","Sugar","Bananas"]:
    recipe_search(recipes_list,i)