from json import dumps

from .base import Host

class Modrinth(Host):

    api_url = 'https://api.modrinth.com/v2'
    auth_header_key = 'Authorization'

    headers = {
    }

    def publish(self, version = None, title = 'New Release', changelog = None, minecraft_versions = None, prerelease = False):

        # generate release data

        data = {
            'loaders': ['minecraft'],
            'dependencies': [],
            'game_versions': minecraft_versions,
            'version_type': "beta" if prerelease else "release",
            'featured': False,
            'status': 'draft',

            'name': title,
            'version_number': version,
            'project_id': self.id,

            'file_parts': ['file'],
            'primary_file': 'file',
        }

        if changelog:
            data['changelog'] = changelog

        post_data = {
            'data': dumps(data),
            'file': (self.rp.file.name, self.rp.get_file(), 'application/zip'),
        }

        # check if release already exists

        assets_url = f'{self.api_url}/project/{self.id}/version'
        assets = self.get(assets_url).json()
        assets = {a['version_number']: str(a['id']) for a in assets}

        if version in assets:
        # if it does, modify it
            patch_url = f'{self.api_url}/version/{assets[version]}'

            # modify release
            del data['file_parts']
            del data['primary_file']
            patch = self.patch(patch_url, json=data)

            version_data = self.get(patch_url)
            file_hash = version_data.json()['files'][0]['hashes']['sha1']

            # upload new file
            post_data['data'] = dumps({'file_parts': ['file'], 'primary_file': 'file'})
            self.post(patch_url + '/file', files=post_data)

            # delete old file
            version_data = self.get(patch_url)
            file_hash = version_data.json()['files'][0]['hashes']['sha1']
            self.delete(f"https://api.modrinth.com/v2/version_file/{file_hash}")

            return patch
        else:
        # if not, create a new one
            post_url = f'{self.api_url}/version'
            return self.post(post_url, files=post_data)