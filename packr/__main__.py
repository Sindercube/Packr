from pathlib import Path
from argparse import ArgumentParser
from yaml import load, Loader

from packr import Resource_Pack
from packr.file import File
from packr.hosts import GitHub, Modrinth, CurseForge

class ArgumentError(Exception):
    pass
class MissingAuthError(Exception):
    pass

def is_true(value):
    return value.lower() in ('yes', 'true', 't', 'y', '1')

def strip(value):
    return value.strip().rstrip()

def gen_arguments():

    parser = ArgumentParser()

    #parser.add_argument('-f', '--filename', nargs='?', help="What to name the generated pack")
    #parser.add_argument('-p', '--parts', type=strip, nargs='*', help="A list of files or directories to make the pack out of")
    #parser.add_argument('-d', '--output-directory', default='build/', help="What directory to store the pack in")
    #parser.add_argument('-of', '--optimize-files', type=is_true, nargs='?', const=True, default=True, help="Whether to optimize JSON and texture files (Lossless)")
    #parser.add_argument('-gr', '--github-repo', default=None, help="The GitHub repository to publish the release to")
    #parser.add_argument('-mi', '--modrinth-id', default=None, help="The Modrinth project to publish the release to")
    #parser.add_argument('-ci', '--curseforge-id', default=None, help="The CurseForge project to publish the release to")
    #parser.add_argument('-mv', '--minecraft-versions', type=strip, nargs='*', help="What versions of Minecraft are supported with this release")

    parser.add_argument('-f', '--filename', default="packr.yml", help="What config file to generate the pack from")

    parser.add_argument('-rn', '--release-name', default="New Release", help="The name of the release")
    parser.add_argument('-rv', '--release-version', default=None, help="The version of the release")
    parser.add_argument('-ch', '--changelog', default=None, help="The changelog of the release")
    parser.add_argument('-pr', '--prerelease', type=is_true, nargs='?', const=True, default=False, help="Whether the release is an early, preview release")

    parser.add_argument('-gr', '--github-repo', default=None, help="The GitHub repository to publish the release to")
    parser.add_argument('-mi', '--modrinth-id', default=None, help="The Modrinth project to publish the release to")
    parser.add_argument('-ci', '--curseforge-id', default=None, help="The CurseForge project to publish the release to")

    parser.add_argument('-gt', '--github-token', default=None, help="The GitHub access token used to publish the release")
    parser.add_argument('-mt', '--modrinth-token', default=None, help="The Modrinth access token used to publish the release")
    parser.add_argument('-ct', '--curseforge-token', default=None, help="The CurseForge access token used to publish the release")

    return parser.parse_args()

def main():
    args = gen_arguments()
    config = gen_config(args)
    packs, mc_versions = generate(config)
    publish(args, packs, mc_versions)

def gen_config(args):

    with open(args.filename, 'r') as file:
        config = load(file, Loader)

    return config

def generate(config):

    print('Generating Packs...')

    mc_versions = config.get('minecraft-versions', ['1.18.2'])

    output_directory = config.get('output-directory', 'build/')
    optimize_files = config.get('optimize-files', True)
    packs = []
    for file in config['files']:
        if not isinstance(file, dict):

            packs.append(File(
                file,
                Path(output_directory),
                optimize_files
            ))
            continue

        ((file, parts),) = file.items()

        pack = Resource_Pack(
            file,
            Path(output_directory),
            parts,
            optimize_files
        )
        pack.gen(True)
        packs.append(pack)

    print('Done!')
    return packs, mc_versions

def publish(args, packs, mc_versions):

    hosts = []
    if args.github_repo:
        if not args.github_token:
            raise MissingAuthError('A GitHub authorization token is required to upload a release to GitHub.')
        hosts.append(GitHub(packs, args.github_token, args.github_repo))
    if args.modrinth_id:
        if not args.modrinth_token:
            raise MissingAuthError('A Modrinth authorization token is required to upload a release to Modrinth.')
        hosts.append(Modrinth(packs, args.modrinth_token, args.modrinth_id))
    if args.curseforge_id:
        if not args.curseforge_token:
            raise MissingAuthError('A Curseforge authorization token is required to upload a release to Curseforge.')
        hosts.append(CurseForge(packs, args.curseforge_token, args.curseforge_id))

    for host in hosts:
        print(f'Publishing to {host.__class__.__name__}...')
        result = host.publish(args.release_version, args.release_name, args.changelog, mc_versions, args.prerelease)
        if result.status_code in [200, 204]:
            print('Done! Uploaded successfully!\n')
        else:
            print(f'Done! But the upload failed... {result.reason}')
            print(result.json(), '\n')

if __name__ == '__main__':
    main()
