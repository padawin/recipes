import functools
from PIL import Image

images_config = [
    {"crop": True, "height": 334, "width": 501},
    {"crop": True, "height": 200, "width": 200},
]


def image_transpose_exif(im):
    """
    Applies EXIF transformations to `im` (if present) and returns
    the result as a new image.
    Taken from [here](https://stackoverflow.com/a/30462851/1667018)
    and adapted.
    """
    exif_orientation_tag = 0x0112  # contains an integer, 1 through 8
    exif_transpose_sequences = [  # corresponding to the following
        [],
        [Image.FLIP_LEFT_RIGHT],
        [Image.ROTATE_180],
        [Image.FLIP_TOP_BOTTOM],
        [Image.FLIP_LEFT_RIGHT, Image.ROTATE_90],
        [Image.ROTATE_270],
        [Image.FLIP_TOP_BOTTOM, Image.ROTATE_90],
        [Image.ROTATE_90],
    ]

    try:
        seq = exif_transpose_sequences[im._getexif()[exif_orientation_tag] - 1]
    except Exception:
        return im
    else:
        if seq:
            return functools.reduce(lambda im, op: im.transpose(op), seq, im)
        else:
            return im


def process_image_for_config(fname, config):
    def new_img(size, im_to_paste=None):
        im = Image.new(
            "RGB",
            (min(size[0], im_to_paste.size[0]), min(size[1], im_to_paste.size[1]))
        )
        im.paste(
            im_to_paste,
            (
                min(0, (size[0] - im_to_paste.size[0]) // 2),
                min(0, (size[1] - im_to_paste.size[1]) // 2),
            ),
        )
        return im
    im = image_transpose_exif(Image.open(fname))
    size = (config["width"], config["height"])
    scale_x = size[0] / im.size[0]
    scale_y = size[1] / im.size[1]
    if config["crop"]:
        scale = max(scale_x, scale_y)
    else:
        scale = min(scale_x, scale_y)
    size2 = tuple(int(round(value * scale)) for value in im.size)
    im = im.resize(size2, Image.ANTIALIAS)
    im = new_img(size, im)
    return im


def process_image(fname):
    for config in images_config:
        yield config, process_image_for_config(fname, config)
