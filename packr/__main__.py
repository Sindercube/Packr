from pathlib import Path
from argparse import ArgumentParser, ArgumentTypeError

from packr import ResourcePack
from packr.hosts import Github, Modrinth, CurseForge

class ArgumentError(Exception):
    pass
class MissingAuthError(Exception):
    pass

def is_true(value):
    return value.lower() in ('yes', 'true', 't', 'y', '1')

def gen_arguments():

    parser = ArgumentParser()

    parser.add_argument('-f', '--filename', help="", nargs='?')
    parser.add_argument('-p', '--parts', help="", nargs='*')
    parser.add_argument('-d', '--output-directory', help="", default='build/')
    parser.add_argument('-of', '--optimize-files', type=is_true, nargs='?', const=True, default=False)

    parser.add_argument('-rn', '--release-name', help="", default="New Release")
    parser.add_argument('-rv', '--release-version', help="", default=None)
    parser.add_argument('-ch', '--changelog', help="", default=None)
    parser.add_argument('-mv', '--minecraft-versions', help="", nargs='*')

    parser.add_argument('-gr', '--github-repo', help="", default=None)
    parser.add_argument('-mi', '--modrinth-id', help="", default=None)
    parser.add_argument('-ci', '--curseforge-id', help="", default=None)

    parser.add_argument('-mt', '--modrinth-token', help="", default=None)
    parser.add_argument('-gt', '--github-token', help="", default=None)
    parser.add_argument('-ct', '--curseforge-token', help="", default=None)
    #parser.add_argument('-cpt', '--curseforge-project-token', help="", default=None)

    return parser.parse_args()

def main():

    args = gen_arguments()

    if not args.filename:
        raise ArgumentError('A filename is required to generate the pack.')
    if not args.parts:
        raise ArgumentError('Parts are required to generate the pack.')
    
    print('Generating Resource Pack...')

    pack = ResourcePack(
        args.filename,
        Path(args.output_directory),
        [Path(p) for p in args.parts],
        args.optimize_files
    )
    pack.gen(True)
    print('Done!\n')

    hosts = []

    if args.github_repo:
        if not args.github_token:
            raise MissingAuthError('A Github authorization token is required to upload a release to Github.')
        hosts.append(Github(pack, args.github_token, args.github_repo))
    if args.modrinth_id:
        if not args.modrinth_token:
            raise MissingAuthError('A Modrinth authorization token is required to upload a release to Modrinth.')
        hosts.append(Modrinth(pack, args.modrinth_token, args.modrinth_id))
    if args.curseforge_id:
        if not args.curseforge_token:
            raise MissingAuthError('A Curseforge authorization token is required to upload a release to Curseforge.')
        hosts.append(CurseForge(pack, args.curseforge_token, args.curseforge_id))

    for host in hosts:
        print(f'Publishing to {host.__class__.__name__}...')
        result = host.publish(args.release_version, args.release_name, args.changelog, args.minecraft_versions)
        if result.status_code in [200, 204]:
            print(f'Done! Uploaded successfully!\n')
        else:
            print(f'Done! But the upload failed... {result.reason}')


if __name__ == '__main__':
    main()
