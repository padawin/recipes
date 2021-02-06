#!/bin/env python3

import sys
import errno
from os import listdir, makedirs
from os.path import isdir, join, dirname, exists
from images import process_image
from common import get_recipe_image

# Args[1]: path to src code
# Args[2]: path to recipes
# Args[3]: path to destination

src_dir = sys.argv[1]
recipes_dir = sys.argv[2]
dest_dir = sys.argv[3]


def create_dir(file_path):
    name = dirname(file_path)
    if exists(name):
        return

    try:
        makedirs(name)
    except OSError as exc:  # Guard against race condition
        if exc.errno != errno.EEXIST:
            raise


def generate_thumbnails(path, dest_path):
    for i, im in enumerate(process_image(path), start=1):
        destination = "{directory}/{width}x{height}x{crop}/{path}".format(
            directory=dest_path,
            width=im[0]['width'],
            height=im[0]['height'],
            crop=int(im[0]['crop']),
            path=path
        )
        create_dir(destination)
        im[1].save(destination, "JPEG", quality=95, optimize=True)


def generate_category(category):
    for recipe in listdir(join(recipes_dir, category)):
        if not isdir(join(recipes_dir, category, recipe)):
            continue

        recipe_image = get_recipe_image(recipes_dir, category, recipe)
        if recipe_image is not None:
            generate_thumbnails(recipe_image, join(dest_dir, "images"))


def generate_categories():
    for cat in listdir(recipes_dir):
        if not isdir(join(recipes_dir, cat)):
            continue
        generate_category(cat)


generate_categories()
