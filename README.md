<p align="center">
  <h1 align="center"><b>Packr</b></h1>
  <img align="center" alt="GitHub Release" src="https://img.shields.io/github/v/release/Sindercube/Packr?include_prereleases">
</p>

# About

**Packr** is a Python CLI tool and a GitHub Workflow action used to make Minecraft Resource Packs out of multiple different directories and publish them to different distribution platforms.

Intended to be used by Resource Pack creators who are tired of uploading their content to every platform manually, it simplifies the process to just creating a new GitHub release, and everything else getting updated.

The supported distribution platforms are:
- [GitHub](https://github.com)
- [Modrinth](https://modrinth.com/)
- [CurseForge](https://curseforge.com/)

# Table of Contents 

- [CLI Usage](#cli-usage)
- [GitHub Workflow Usage](#github-workflow-usage)
  - [Minimal Example](#minimal-example)
  - [Advanced Example](#advanced-example)
  - [Access Tokens](#access-tokens)
  - [Inputs](#inputs)
- [Credits](#credits)

# Usage

**Packr** generates resource packs using a YAML file.
The default file used by Packr is `packr.yml`.

## Example File

`packr.yml`
```yaml
files:
  - pack.zip:
    - test_pack/*
  - extra.zip

minecraft-versions:
  - 1.18.2
```

The `files` key is used to assign a list of files to generate.

You can automatically compress files into a `.zip` file by adding more keys to a value.
> To add a file too the zip file, simply give its path. (`assets/pack.mcmeta`)

> To add every file from a directory to the zip file, give its path and add a star. (`assets/*`)

## Generating Using CLI

To use **Packr** as a CLI tool, you first have to install it using `pip install git+https://github.com/sindercube/packr`

To generate the resource packs, simply run `python -m packr`

> Run `python -m packr -h` for additional information.

# GitHub Workflow Usage

<!--
> Click [here](https://github.com/Sorrowfall/RP-Example/generate) to create a new repository with the workflow already set up.
Remember to edit `.github/workflows/build-packs.yml` to set up packr correctly for your pack.
-->

To automatically generate Resource Packs from the contents of your GitHub repository, you first have to make a new workflow YAML file in the `.github/workflows/` directory.

## Minimal Example

An example of a Packr configuration, which just adds the generated files to your GitHub release.

`publish.yml`
```yaml
on:
  release:
    types: [published]

jobs:
  check-bats-version:
    runs-on: ubuntu-latest
    steps:

      - name: Build & Upload Packs
        uses: Sindercube/Packr@v2
        with:

          github-repo: ${{ github.event.repository.full_name }}
          release-version: ${{ github.event.release.tag_name }}
          github-token: ${{ secrets.GITHUB_TOKEN }}
```

## Advanced Example

A full showcase of what Packr can do.

`publish.yml`
```yaml
on:
  release:
    types: [published]
  workflow_dispatch:

jobs:
  check-bats-version:
    runs-on: ubuntu-latest
    steps:

      - name: Build & Upload Packs
        uses: Sindercube/Packr@v2
        with:

          filename: packr.yml

          modrinth-id: 'xxxxxxxx'
          curseforge-id: '000000'
          github-repo: ${{ github.event.repository.full_name }}

          release-name: ${{ github.event.release.name }}
          release-version: ${{ github.event.release.tag_name }}
          changelog: ${{ github.event.release.body }}
          prerelease: ${{ github.event.release.prerelease }}

          github-token: ${{ secrets.GITHUB_TOKEN }}
          modrinth-token: ${{ secrets.MODRINTH_TOKEN }} # https://modrinth.com/settings/account
          curseforge-token: ${{ secrets.CURSEFORGE_API_TOKEN }} # https://www.curseforge.com/account/api-tokens
```

## Access Tokens

To publish your pack to Modrinth or CurseForge, you have to make new [`MODRINTH_TOKEN`](https://modrinth.com/settings/account) and [`CURSEFORGE_TOKEN`](https://www.curseforge.com/account/api-tokens) secrets in your repository's settings in **Settings > Secrets & Variables > Actions**, then clicking the **New Repository Secret** button and filling out the data.

> For more information, check out [the GitHub Secrets documentation](https://docs.github.com/en/actions/security-guides/encrypted-secrets#creating-encrypted-secrets-for-a-repository).

## Inputs

| Name | Description | Required |
| - | - | - |
| `filename` | What YAML file to generate the packs from | `True` |
|||
| `release-name` | The name of the release | `False` |
| `release-version` | The version of the release | `True` |
| `changelog` | The changelog for the release | `False` |
| `prerelease` | Whether the release is an early, preview release | `False` |
|||
| `github-repo` | The GitHub repository to publish the release to | `False` |
| `modrinth-id` | The Modrinth project to publish the release to | `False` |
| `curseforge-id` | The CurseForge project to publish the release to | `False` |
|||
| `github-token` | The GitHub access token used to publish the release | `True` (if `github-repo` is specified) |
| `modrinth-token` | The Modrinth access token used to publish the release | `True` (if `modrinth-id` is specified) |
| `curseforge-token` | The CurseForge access token used to publish the release | `True` (if `curseforge-id` is specified) |

# Credits

A big Thank You to:
- [**The Modrinth Team**](https://github.com/orgs/modrinth/people) for making [Modrinth](https://modrinth.com/), the (objectively) best Minecraft content distribution platform.
- [**Kayra Uylar**](https://github.com/kuylar) for making [Curserinth](https://curserinth.kuylar.dev/), which saved me from having to use 2 different API tokens for CurseForge.
- [**IntellectualSites**](https://github.com/IntellectualSites) for making the [CurseForge Version Identifier](https://github.com/IntellectualSites/CurseForge-version-identifier) repository, which also saved me from having to use 2 different API tokens for CurseForge.

###### And a huge I Hate You to CurseForge.