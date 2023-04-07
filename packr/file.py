from pathlib import Path
from shutil import copy2
from hashlib import sha1

from packr.optimize import copy_and_optimize
from packr.hash import hash_file


class File:

    file: Path
    hash: str

    def get_file(self):
        with open(self.file, 'rb') as file:
            return file.read()

    def __init__(self,
        filename: str,
        output_dir: Path = Path('build/'),
        optimize_files: bool = True,
        hash_input: bool = True
    ):
        self.output_dir = Path(output_dir)
        self.file = Path(filename)

        if not self.output_dir.exists():
            self.output_dir.mkdir()

        if optimize_files:
            self.copy_function = copy_and_optimize
        else:
            self.copy_function = copy2

        if self.file.is_dir():
            return

        self.copy_function(self.file, self.output_dir)

        if hash_input:

            self.hash = hash_file(self.file, sha1)

            with open(self.output_dir / self.file.with_suffix(self.file.suffix+'.sha1'), 'w+') as file:
                file.write(self.hash)
