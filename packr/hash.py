from pathlib import Path

from hashlib import sha1
from _hashlib import HASH as Hash


def _update_hash(path: Path, hash_object: Hash):
    with open(path, 'rb') as file:
        for chunk in iter(lambda: file.read(4096), b""):
            hash_object.update(chunk)


def _hash_path(path: Path, hash_object: Hash) -> str:
    if path.is_dir():
        for path in sorted(path.iterdir(), key=lambda p: str(p).lower()):
            _update_hash(path, hash_object)
    else:
        _update_hash(path, hash_object)

    return hash_object.hexdigest()

def hash_file(file: Path, hash_object: Hash) -> str:
    return _hash_path(file, hash_object(usedforsecurity=False))

def hash_directory(directory: Path, hash_object: Hash) -> str:
    return _hash_path(directory, hash_object(usedforsecurity=False))
