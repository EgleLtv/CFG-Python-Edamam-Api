import requests
import os
import sys

# clear text file for ease of debugging each time the program is started
file = open('recipetext.txt', 'r+')
file.truncate(0)

print('Welcome to RecipSearch!\n'
      'We\'ll choose a couple of recipes based on an ingredient of your choice'
      'and your dietary preferences')


# Edamam API open and return data
def search_recipe(ingredient):
    app_id = 'a0c0f07e'
    app_key = '237f8b540429c9107f3ec012672723c0'
    results = requests.get(
        'https://api.edamam.com/search?q={}&app_id={}&app_key={}'.format(ingredient, app_id, app_key))
    data = results.json()
    return data['hits']


# list to hold ingredients
recipe_list = []


# start search by entering ingredient
def run():
    results = search_recipe(input('Please enter an ingredient'))
    # diet labels input
    diet_choice = ''
    diet_label = input('Do you have any dietary preferences? \n'
                       'VG-vegetarian\n'
                       'V-vegan\n'
                       'PC-pescatarian\n'
                       'GF-gluten-free\n'
                       'N-no preferences').lower()
    if diet_label == 'vg':
        diet_choice = 'Vegetarian'
    elif diet_label == 'v':
        diet_choice = 'Vegan'
    elif diet_label == 'pc':
        diet_choice = 'Pescatarian'
    elif diet_label == 'gf':
        diet_choice = 'Gluten-Free'
    else:
        diet_label = 'n'
        print('You did not choose any diet preferences.')

    recipe_num = 1
    # initialise for loop to go through recipes
    for result in results:
        recipe = result['recipe']
        labels = recipe['healthLabels']
        check = False

        # check if diet label is mentioned
        for item in labels:
            if item == diet_choice:
                check = True

        # print recipe if no diet selected or if diet matches
        if check or diet_label == 'n':
            print('The recipe number {}\'s label is {}.\n'
                  'Total calories are {}.\n'
                  'You can access it here: {}'.format(recipe_num, recipe['label'], int(recipe['calories']),
                                                      recipe['url']))
            print('Recipe is suitable for people following these diets: {}'.format(', '.join(labels)))
            # print all ingredients of the recipe and save to a list
            print('The recipe calls for these ingredients:')
            ing_values = recipe['ingredients']
            for ing in ing_values:
                print(ing['text'])
                recipe_list.append(ing['text'])
            recipe_num += 1

            # save recipe to file, including ingredient list
            save_recipes = input('Do you want to save this recipe into a file? Y/N').lower()
            if save_recipes == 'y':
                with open('recipetext.txt', 'a') as recipe_file:
                    recipe_file.write(recipe['label'] + '\n')
                    recipe_file.write('Total calories: ' + str(int(recipe['calories'])) + '\n')
                    recipe_file.write(recipe['url'] + '\n')
                    for element in recipe_list:
                        recipe_file.write(element + '\n')
                    recipe_file.write('\n')

            # ask if continue or not
            do_continue = input('Do you want to see another recipe? Y/N').lower()
            if do_continue == 'n':
                if os.stat('recipetext.txt').st_size == 0:
                    print('Sorry you did not like the recipes.')
                else:
                    print('Saved recipes can be found in a text file named recipetext.txt :)')
                sys.exit('Bye, thank you for using RecipSearch!')

            # clear list to start next recipe
            recipe_list.clear()

    # ask if want to try again
    if os.stat('recipetext.txt').st_size == 0:
        start_over = input('\nNo more recipes to show, sorry you didn\'t see anything you liked.\n'
                           'Would you like to try again with a different ingredient? Y/N').lower()
        if start_over == 'y':
            run()
            print('Bye, thank you for using RecipSearch!')
    else:
        print('\nNo more recipes to show, thank you for using RecipSearch! :)\n'
              'Saved recipes can be found in a text file named recipetext.txt')
        start_over = input('Would you like to try again with a different ingredient? Y/N').lower()
        if start_over == 'y':
            run()
            print('Bye, thank you for using RecipSearch!')


# run program
run()
