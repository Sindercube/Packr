<p align="center">
  <h1 align="center"><b>Resource Packager</b></h1>
  <img alt="GitHub Release" src="https://img.shields.io/github/v/release/Sindercube/Resource-Packager?include_prereleases">
</p>

# About

**Resource Packager** is a Python CLI tool and a GitHub Workflow action used to make Minecraft Resource Packs out of multiple different directories and publish them to different distribution platforms.

Intended to be used by Resource Pack creators who are tired of uploading their content to every platform manually, it simplifies the process to just creating a new Github release, and everything else getting updated.

The supported distribution platforms are:
- [GitHub](https://github.com)
- [Modrinth](https://modrinth.com/)
- [CurseForge](https://curseforge.com/)

# Table of Contents 

- [CLI Usage](#cli-usage)
- [Github Workflow Usage](#github-workflow-usage)
  - [Minimal Example](#minimal-example)
  - [Advanced Example](#advanced-example)
  - [Access Tokens](#access-tokens)
  - [Inputs](#inputs)
- [Known Issues](#known-issues)
- [Credits](#credits)

# CLI Usage

To use resource_packager as a CLI tool, you first have to install it using `pip install git+https://gitlab.com/sindercube/resource_packager`

After it is installed, use `python -m resource_packager -h` to view how to use the tool.

# Github Workflow Usage

<!--
> Click [here](https://github.com/Sorrowfall/RP-Example/generate) to create a new repository with the workflow already set up.
Remember to edit `.github/workflows/build-packs.yml` to set up resource_packager correctly for your pack.
-->

To automatically generate Resource Packs from the contents of your GitHub repository, you first have to make a new workflow YAML file in the `.github/workflows/` directory.

## Minimal Example

This is an example of the simplest possible Resource Packager configuration, which just adds the pack files to your GitHub release.

`publish.yml`
```yaml
on:
  release:
    types: [published]

jobs:
  check-bats-version:
    runs-on: ubuntu-latest
    steps:

      - name: Checkout Repo
        uses: actions/checkout@v2

      - name: Build & Upload Pack (Minimal)
        uses: Sindercube/Resource-Packager@v2.0.0
        with:

          filename: pack_min.zip # The file name of your pack.
          parts: | # The files and folders you want to use in your pack. Separated with new lines.
            test_pack/*
          minecraft-versions: | # What Minecraft versions are supported by your pack? Separated with new lines
            1.18.2

          # You shouldn't change these values unless you know what you're doing
          github-repo: ${{ github.event.repository.name }}
          release-version: ${{ github.event.release.tag_name }}
          github-token: ${{ secrets.GITHUB_TOKEN }}
```

## Advanced Example

A full showcase of what Resource Packager can do.

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

      - name: Checkout Repo
        uses: actions/checkout@v2

      #- name: Get Tag
      #  id: tag
      #  uses: dawidd6/action-get-tag@v1

      - name: Build & Upload Pack
        uses: Sindercube/Resource-Packager@v2.0.0
        with:

          filename: pack.zip
          parts: |
            test_pack/*
          output-directory: build/ 
          optimize-files: true
          minecraft-versions: |
            1.18.2

          github-repo: 'xxx/xxx'
          modrinth-id: 'xxxxxxxx'
          curseforge-id: '000000'

          release-name: ${{ github.event.release.name }}
          release-version: ${{ github.event.release.tag_name }} #${{ steps.tag.outputs.tag }}
          changelog: ${{ github.event.release.body }}

          github-token: ${{ secrets.GITHUB_TOKEN }}
          modrinth-token: ${{ secrets.MODRINTH_TOKEN }} # https://modrinth.com/settings/account
          curseforge-token: ${{ secrets.CURSEFORGE_API_TOKEN }} # https://www.curseforge.com/account/api-tokens
```

> If you want to generate multiple packs, just copy-paste the `Build Pack` step.

## Access Tokens

To publish your pack to Modrinth or Curseforge, you have to make new [`MODRINTH_TOKEN`](https://modrinth.com/settings/account) and [`CURSEFORGE_TOKEN`](https://www.curseforge.com/account/api-tokens) secrets in your repository's settings in **Settings > Secrets & Variables > Actions**, then clicking the **New Repository Secret** button and filling out the data.

> For more information, check out [the GitHub Secrets documentation](https://docs.github.com/en/actions/security-guides/encrypted-secrets#creating-encrypted-secrets-for-a-repository).

## Inputs

| Name | Description | Required |
| - | - | - |
| `filename` | What to name the generated pack | `True` |
| `parts` | A list of files or directories to make the pack out of | `True` |
| `output-directory` | What directory to store the pack in | `False` |
| `optimize-files` | Whether to optimize JSON and texture files (Lossless) | `False` |
|
| `release-version` | The name of the release | `True` |
| `release-name` | The version of the release | `False` |
| `changelog` | The changelog for the release | `False` |
| `minecraft-versions` | What versions of Minecraft are supported with this release | `False` |
|
| `github-repo` | The Github repository to publish the release to | `False` |
| `modrinth-id` | The Modrinth project to publish the release to | `False` |
| `curseforge-id` | The Curseforge project to publish the release to | `False` |
|
| `github-token` | The Github access token used to publish the release | `True` (if `github-repo` is specified) |
| `modrinth-token` | The Modrinth access token used to publish the release | `True` (if `github-repo` is specified) |
| `curseforge-token` | The Curseforge access token used to publish the release | `True` (if `github-repo` is specified) |

# Known Issues

- Currently, updating Modrinth resource packs simply does not work, if you are able to figure it out [(because I really cannot)](https://discord.com/channels/734077874708938864/1079544436964474971), please send a PR!

# Credits

A big Thank You to:
- [**The Modrinth Team**](https://github.com/orgs/modrinth/people) for making [Modrinth](https://modrinth.com/), the (objectively) best Minecraft content distribution platform.
- [**Kayra Uylar**](https://github.com/kuylar) for making [Curserinth](https://curserinth.kuylar.dev/), which saved me from having to use 2 different API tokens for CurseForge.
- [**IntellectualSites**](https://github.com/IntellectualSites) for making the [CurseForge Version Identifier](https://github.com/IntellectualSites/CurseForge-version-identifier) repository, which also saved me from having to use 2 different API tokens for CurseForge.

###### And a huge I Hate You to Curseforge, for requiring 2 different API tokens.