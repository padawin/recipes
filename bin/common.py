from os.path import isfile, join


def get_recipe_image(recipes_dir, category, recipe):
    image_url = join(category, recipe, "cover.jpg")
    recipe_image = join(recipes_dir, image_url)
    if not isfile(recipe_image):
        return None
    return recipe_image
