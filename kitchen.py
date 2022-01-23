import uuid
from enum import Enum


class Categories(Enum):
    dessert = 1
    main_dish = 2
    soup = 3
    drink = 4
    bakery = 5
    special = 6


class Ingredient:
    def __init__(self, name: str, quantity: float, measure: str):
        self._name = name
        self._quantity = quantity
        self._measure = measure

    @property
    def name(self):
        return self._name

    @property
    def quantity(self):
        return self._quantity

    @property
    def measure(self):
        return self._measure

    @name.setter
    def name(self, val):
        raise ValueError("Sorry name is not changeable")

    @measure.setter
    def measure(self, val):
        raise ValueError("Sorry measure is not changeable")

    def change_quantity(self, val):
        if self._quantity + val < 0:
            raise ValueError("Not enough quantity")
        else:
            self._quantity += val

    def get_quantity_in_measure(self):
        return self.quantity, self.measure

    def __str__(self):
        return f"{self._name} {self._quantity} {self._measure}"


class Fridge:
    def __init__(self):
        self.shelfs = {}
        self.id = None
        self.secret_phrase = None

    def change_ingredients_on_shelfs(self, imp_list, exp_list):
        for ingredient in imp_list:
            shelf_ingredient = self.shelfs.get(ingredient.name)

            if shelf_ingredient:
                shelf_ingredient.change_quantity(ingredient.quantity)

            else:
                self.shelfs[ingredient.name] = ingredient

        for ingredient in exp_list:
            shelf_ingredient = self.shelfs.get(ingredient.name)

            if shelf_ingredient:
                shelf_ingredient.change_quantity(-1*ingredient.quantity)

            else:
                raise ValueError("Sorry no such ingredient in fridge")

    def show_shelfs(self):
        return [str(ingredient) for name, ingredient in self.shelfs.items()]

    def generate_id(self):
        self.id = uuid.uuid4()
        return str(self.id)

    def generate_secret(self):
        pass


class Recipe:
    def __init__(self):
        self.ingredient_list = []
        self.recipe_url = ""
        self.category = None
        self.description = None
        self.name = ""


class CookBook:
    def __init__(self):
        categories = [e.value for e in Categories]
        self.recipes = dict.fromkeys(categories, {})
        self.id = None
        self.secret_phrase = None

    def add_recipe(self, recipe: Recipe):
        existing_recipe = self.recipes[recipe.category].get(recipe.name)

        if existing_recipe:
            recipe.name = recipe.name + "_v2"
            self.recipes[recipe.category][recipe.name] = recipe

    def show_recipies(self):
        return [(recipe, category) for category, category_recipes in self.recipes.items() for r_name, recipe in category_recipes]

    def show_certain_category(self, category):
        return [(recipe, category) for r_name, recipe in self.recipes[category]]
