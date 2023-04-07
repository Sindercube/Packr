#from requests import get, post
from json import dumps

from .base import Host


class CurseForge(Host):

    api_url = 'https://api.curseforge.com/v1/mods/'
    auth_header_key = 'X-Api-Key'
    headers = {}

    curseforge_versions = {}

    def __init__(self, *kwargs):
        super().__init__(*kwargs)

        # fetch version data from github because lol, lmao even
        version_url = 'https://raw.githubusercontent.com/IntellectualSites/CurseForge-version-identifier/main/versions.json'
        version_data = self.get(version_url).json()
        for version in version_data:
            version_name = version['name']
            version_id = version['id']
            if not version_name in self.curseforge_versions:
                self.curseforge_versions[version_name] = version_id

    def publish(self, version = None, title = 'New Release', changelog = None, minecraft_versions = None, prerelease = False):

        metadata = {
            'changelogType': "markdown",
            'displayName': version + ' - ' + title,
            'releaseType': "beta" if prerelease else "release",
            'changelog': changelog or '',
        }

        if minecraft_versions:
            metadata['gameVersions'] = []
            for mcv in minecraft_versions:
                if mcv not in self.curseforge_versions:
                    continue
                if not mcv in metadata['gameVersions']:
                    metadata['gameVersions'].append(self.curseforge_versions[mcv])
        else:
            metadata['gameVersions'] = [9550]

        files_url = f'https://curserinth-api.kuylar.dev/v2/project/{self.id}/version'
        file_data = self.get(files_url).json()
        print(file_data)

        files = {}
        for file in file_data:
            release = file['name'].split(' - ', 1)[0]
            file_id = int(file['id'])
            if not release in files:
                files[release] = file_id
        print(files)

        if version in files:
            metadata['fileID'] = files[version]
            method = 'update-file'
        else:
            method = 'upload-file'

        upload_url = f"https://minecraft.curseforge.com/api/projects/{self.id}/{method}?token={self.token}"
        return self.post(upload_url, data={'metadata': dumps(metadata)}, files={'file': (self.rp.file.name, self.rp.get_file())})
