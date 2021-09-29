import os
import requests

# clear text file for ease of debugging each time the program is started
file = open('recipetext.txt', 'r+')
file.truncate(0)

# dictionary to save calories data for review
dict_calories = {}

# lists to check for diet and meal type
meal_list = ['breakfast', 'lunch', 'dinner', 'snack', 'teatime']
diet_list = ['vegetarian', 'vegan', 'gluten-free', 'low-sugar', 'pescatarian', 'paleo', 'none']


# function to ask for user input on diet
def find_meal():
    # ask for input and only continue if typed in correctly
    while True:
        meal = input('Please choose from the following meal types:\n'
                        'Breakfast, Lunch, Snack, Teatime, Dinner:\n').lower()
        if meal in meal_list:
            return meal
        print('Invalid choice.')


# function to ask for user input on dietary preferences
def find_diet():
    # ask for input and only continue if typed in correctly
    while True:
        diet = input('Please enter your dietary choice from the following options:\n'
                     'Vegan, Vegetarian, Pescatarian, Gluten-free, Paleo, Low-sugar, None:\n').lower()
        if diet in diet_list:
            return diet
        print('Invalid choice.')

# Edamam API open and return data
def search_recipe(ingredient, meal, diet):
    # if diet is chosen, add health search parameter
    if diet != 'none':
        health = '&health='+diet
    else:
        health = ''
    app_id = 'a0c0f07e'
    app_key = '237f8b540429c9107f3ec012672723c0'
    results = requests.get(
        'https://api.edamam.com/search?q={}&app_id={}&app_key={}{}&mealType={}'.format(ingredient, app_id, app_key,
                                                                                       health, meal))
    data = results.json()

    return data['hits']


def print_recipe(recipe_num, recipe, labels, recipe_ing):
    print('\nThe recipe number {}\'s label is {}.\n'
          'Total calories are {}.\n'
          'You can access it here: {}'.format(recipe_num, recipe['label'], int(recipe['calories']),
                                              recipe['url']))

    print('Recipe is suitable for people following these diets: {}'.format(', '.join(labels)))

    # print all ingredients of the recipe and save to a list
    print('The recipe calls for these ingredients:')

    ing_values = recipe['ingredients']

    for ing in ing_values:
        print(ing['text'])
        recipe_ing.append(ing['text'])

    return None


def save_recipe(recipe, recipe_ing):
    save_recipes = input('Do you want to save this recipe into a file? Y/N\n').lower()

    if save_recipes == 'y':

        # save recipe info for recipe calories review
        add_dict_value = {recipe['label']: int(recipe['calories'])}
        dict_calories.update(add_dict_value)

        # FOR DEBUGGING PURPOSES ONLY!
        print(add_dict_value)
        print(dict_calories)

        # append text file to add recipe info
        with open('recipetext.txt', 'a') as recipe_file:

            recipe_file.write(recipe['label'] + '\n')
            recipe_file.write(recipe['url'] + '\n')

            for element in recipe_ing:
                recipe_file.write(element + '\n')

            recipe_file.write('\n')

        # open appended text file
        os.startfile("recipetext.txt")

    return None


def recipe_review():
    s = sorted(dict_calories.items(), key=lambda x: x[1], reverse=True)
    print('\nYou have saved the recipes below.\n'
          'The recipes are listed from highest total calories to lowest in a descending order.')
    for k, v in s:
        print('Recipe name: {}, total calories: {}'.format(k, v))

    min_value = min(dict_calories.values())
    min_keys = min(dict_calories, key=dict_calories.get)
    print('The recipe {} has lowest calories. Calories are {}'.format(min_keys, min_value))
    return None


# start search by entering ingredient and diet
def run():
    ingredient_choice = (input('What ingredient do you want a recipe for?\n'))

    # prompt user input for meal type and diet
    meal = find_meal()
    diet = find_diet()
    results = search_recipe(ingredient_choice, meal, diet)

    # list to hold ingredients
    recipe_ing = []

    recipe_num = 0

    for result in results:
        recipe = result['recipe']
        labels = recipe['healthLabels']

        recipe_num += 1

        # print recipe details to terminal
        print_recipe(recipe_num, recipe, labels, recipe_ing)

        # save recipe to a file, including the ingredient list
        save_recipe(recipe, recipe_ing)

        # ask if users want to continue or not
        do_continue = input('Do you want to see another recipe? Y/N \n').lower()

        if do_continue == 'n':
            break

    # ask if want to try again
    if os.stat('recipetext.txt').st_size == 0:

        start_over = input('Sorry you didn\'t see anything you liked!\n'
                           '\nWould you like to find recipes for a different ingredient instead? Y/N\n').lower()

    else:
        start_over = input('No more recipes to show!\n'
                           '\nSaved recipes can be found in a text file named recipetext.txt\n'
                           '\nWould you like to find recipes for another ingredient? Y/N\n').lower()

    if start_over == 'y':
        run()
    # ask if want to review calories data for recipes that have been saved to a file
    else:
        do_review_recipes = input('Would you like to review calorific information of the recipes saved? Y/N\n').lower()
        if do_review_recipes == 'y':
            recipe_review()

    return None


# run program
run()
print('\nBye, thank you for using RecipeSearch!')
