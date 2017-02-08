import json

def export_cookbook(data):
    with open('cookbook.json', 'w') as outfile:
        json.dump(data, outfile)

def import_cookbook():
    with open('cookbook.json') as infile:
        return json.load(infile)

class Recipe:
    def __init__(self, color_id, color_name, cyan, magenta, yellow, black, white):
        self.color_id = color_id
        self.color_name = color_name
        self.cyan = cyan
        self.magenta = magenta
        self.yellow = yellow
        self.black = black
        self.white = white

class Cookbook:
    def __init__(self, recipes):
        self.recipe_list = recipes

    def get_recipe(self, color_name):
        for recipe in self.recipe_list:
            if recipe.color_name == color_name:
                return recipe
        return None
