from json import dumps

from .base import Host

class GitHub(Host):

    api_url = 'https://api.github.com/repos/'
    auth_header_key = 'Authorization'
    auth_header_prefix = 'token '

    headers = {
        "Content-Type": 'application/zip',
        "Accept": 'application/vnd.github+json',
        "X-GitHub-Api-Version": '2022-11-28'
    }

    def publish(self, version = None, title = 'New Release', changelog = '', minecraft_versions = None, prerelease = False):
        
        self.api_url += self.id + '/'

        # get releases
        
        release_url = self.api_url + 'releases'
        releases = self.get(release_url).json()
        releases = {r['tag_name']: str(r['url']) for r in releases}
    
        data = {
            'name': title,
            'body': changelog,
            'prerelease': prerelease
        }
    
        # if it exists
        if version in releases:
            result = self.patch(releases[version], data=dumps(data))
        else:
            data['tag_name'] = version
            result = self.post(release_url, data=dumps(data))
        request_data = result.json()

        # check if release already has file

        if 'assets_url' not in request_data:
            assets = {}
        else:
            assets_url = request_data['assets_url']
            assets = self.get(assets_url).json()
            assets = {a['name']: str(a['id']) for a in assets}

        # if yes, delete it

        if self.rp.file.name in assets:
            delete_url = assets_url.rsplit('/', 1)
            delete_url = delete_url[0].rsplit('/', 1)[0] + '/' + delete_url[1]
            delete_url += '/' + assets[self.rp.file.name]
            self.delete(delete_url)

        # upload file to release

        files = {self.rp.file.name: self.rp.get_file()}
        post_url = request_data['upload_url'].split('{?name,label}')[0] + '?name=' + self.rp.file.name
        self.post(post_url, files=files)

        return result
