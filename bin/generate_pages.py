#!/bin/env python3

import sys
from os import listdir, makedirs
from os.path import isdir, join
import markdown

# Args[1]: path to src code
# Args[2]: path to recipes
# Args[3]: path to destination

src_dir = sys.argv[1]
recipes_dir = sys.argv[2]
dest_dir = sys.argv[3]


def generate_common(content):
    header = join(src_dir, "_header.html")
    footer = join(src_dir, "_footer.html")
    with open(header) as f:
        header_content = "".join(f.readlines())
        content = content.replace("%%HEADER%%", header_content)

    with open(footer) as f:
        footer_content = "".join(f.readlines())
        content = content.replace("%%FOOTER%%", footer_content)
    return content


def _read_content(filename):
    src_file = join(src_dir, filename)

    with open(src_file) as f:
        content = "".join(f.readlines())

    return content


def _prepare_page(filename):
    content = _read_content(filename)
    content = generate_common(content)
    return content


def generate_recipe(category, recipe):
    content = _prepare_page("recipe_page.html")
    recipe_file = join(recipes_dir, category, recipe, "recipe.md")
    with open(recipe_file) as f:
        recipe_content = markdown.markdown("".join(f.readlines()))
    content = content.replace("%%RECIPE%%", recipe_content)

    makedirs(join(dest_dir, category, recipe))
    with open(join(dest_dir, category, recipe, "index.html"), "w") as f:
        f.write(content)


def generate_category(category):
    content = _prepare_page("category_page.html")

    name = category.capitalize()
    content = content.replace("%%NAME%%", name)

    recipe_template = _read_content("_recipe_list_item.html")

    recipes_html = []
    for recipe in listdir(join(recipes_dir, category)):
        if not isdir(join(recipes_dir, category, recipe)):
            continue

        generate_recipe(category, recipe)

        url = join(category, recipe)
        name = recipe.capitalize()
        recipe_html = recipe_template.replace("%%URL%%", url)
        recipe_html = recipe_html.replace("%%NAME%%", name)
        recipes_html.append(recipe_html)

    content = content.replace("%%RECIPES%%", "".join(recipes_html))

    with open(join(dest_dir, category, "index.html"), "w") as f:
        f.write(content)


def generate_categories():
    content = _prepare_page("categories_page.html")
    category_template = _read_content("_category.html")

    categories_html = []
    for cat in listdir(recipes_dir):
        if not isdir(join(recipes_dir, cat)):
            continue

        makedirs(join(dest_dir, cat))

        generate_category(cat)

        name = cat.capitalize()
        category_html = category_template.replace("%%URL%%", cat)
        category_html = category_html.replace("%%NAME%%", name)
        categories_html.append(category_html)

    content = content.replace("%%CATEGORIES%%", "".join(categories_html))

    with open(join(dest_dir, "index.html"), "w") as f:
        f.write(content)


generate_categories()
