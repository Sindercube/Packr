from pathlib import Path
from shutil import copy2
from json import load, dump, JSONDecodeError

from PIL import Image


def copy(src, dest):
    copy2(str(src), str(dest))


def copy_and_optimize(src, dest):
    src, dest = Path(src), Path(dest)
    dest = dest #/ Path(''.join(src.parts[1:]))

    if src.suffix == '.png':
        return optimize_image(src, dest)

    if src.suffix in ('.json', '.mcmeta'):
        return optimize_json(src, dest)

    copy(src, dest)


def optimize_image(src, dest):

    image = Image.open(src)
    if image.mode == 'P':
        return copy(src, dest)
    # palette = image.convert('P').getpalette()
    # palette = palette[0:palette.index(0, 4)]
    # pixels = int(len(palette)/3)
    # new_image = image.quantize(pixels)
    # new_image.save(dest, palette=Image.Palette.WEB)
    image.convert("P", palette=Image.Palette.ADAPTIVE)
    image.save(dest)


def optimize_json(src, dest):

    with open(src, 'r') as new:
        try:
            json = load(new)
        except JSONDecodeError:
            print(f"Wrongly formatted JSON file '{src}'")
            return 

    if dest.exists():
        with open(dest, 'r') as original:
            try:
                original = load(original)
                json = {**original, **json}
            except JSONDecodeError:
                print(f"Wrongly formatted JSON file '{dest}'")
                copy(src, dest)
                return

    with open(dest, 'w') as original:
        dump(json, original, separators=(',', ':'))
