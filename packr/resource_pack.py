from pathlib import Path
from shutil import copy2, make_archive, rmtree, copytree
from hashlib import sha1

from typing import List

from packr.optimize import copy_and_optimize
from packr.hash import hash_file


class Resource_Pack:


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

    def gen(self, cache = False, hash_pack = True):

        temp = self.filename
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

        if not cache:
            rmtree(temp)

        if hash_pack:

            self.hash = hash_file(self.file, sha1)

            with open(self.file.with_suffix(self.file.suffix+'.sha1'), 'w+') as file:
                file.write(self.hash)
