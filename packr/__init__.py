from pathlib import Path
from shutil import copy2, make_archive, rmtree, copytree
from hashlib import sha1

from typing import List

from packr.optimizer import copy_and_optimize


class ResourcePack:
    """Generate Minecraft Resource packs from multiple directories.

    Args:
        name (str): What to name the Resource Pack.
        output_dir (Path): What directory to make the Resource Pack in. Defaults to build/
        parts (List[Path]): A list of directories to make the Resource Pack out of. Defaults to an empty list.
        optimize_files (bool): Whether or not to optimize files. Defaults to True.
    """

    file: Path
    hash: str

    _magic_bytes = 65536

    def get_file(self):
        with open(self.file, 'rb') as file:
            return file.read()

    def __init__(self,
        filename: str,
        output_dir: Path = Path('build/'),
        parts: List[Path] = [],
        optimize_files: bool = True,
    ):

        self.parts = parts
        self.output_dir = Path(output_dir)
        if filename.endswith('.zip'):
            filename = filename.rsplit('.zip', 1)[0]
        self.filename = self.output_dir / filename

        if not self.output_dir.exists():
            self.output_dir.mkdir()

        if optimize_files:
            self.copy_function = copy_and_optimize
        else:
            self.copy_function = copy2

    def gen(self, keep_temp = False, hash_pack = True):

        temp = self.output_dir / 'temp/'
        if temp.exists():
            rmtree(temp)
        temp.mkdir()

        for part in self.parts:
            part = Path(part)

            if part.is_dir():
                copytree(part, temp/part.stem, copy_function=self.copy_function, dirs_exist_ok=True)

            elif part.name == '*':
                # copy only directory contents, not directory
                copytree(part.parent, temp, copy_function=self.copy_function, dirs_exist_ok=True)

            elif part.exists():
                self.copy_function(part, temp)

            else:
                print(f"Unknown path '{part}'")

        #file = Path( str(self.filename) + '.zip' )
        #if file.exists():
        #    self.file = file
        #else:
        self.file = Path( make_archive(self.filename, 'zip', temp) )

        if not keep_temp:
            rmtree(temp)

        if hash_pack:

            self.hash = self._gen_hash()

            with open(self.file.with_suffix('.sha1'), 'w+') as file:
                file.write(self.hash)

    def _gen_hash(self):
        hasher = sha1(usedforsecurity=False)
        with open(self.file, 'rb') as file:
            buf = file.read(self._magic_bytes)
            while len(buf) > 0:
                hasher.update(buf)
                buf = file.read(self._magic_bytes)

        return hasher.hexdigest()
