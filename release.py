#!/usr/bin/env python3

# -*- python-indent-offset: 4; -*-

import subprocess
import sys
from os import system
from os.path import join

import semver
import toml

from timew.__version__ import __version__

PACKAGE = "timew"

# Test for command line arguments
if len(sys.argv) != 2:
    print(
        "This script takes exactly 1 command line argument, giving the release type: [major|minor|patch]",
        file=sys.stderr,
    )
    exit(1)

# Test that we are on master branch... we do not support cutting releases on any other branch
current_branch = (
    subprocess.check_output("git rev-parse --abbrev-ref HEAD", shell=True)
    .decode("utf-8")
    .rstrip()
)
if not current_branch == "master":
    print(
        "You are currently on branch '{}'.\nOnly releases on 'master' is supported.".format(
            current_branch
        ),
        file=sys.stderr,
    )
    exit(1)

# Test that there are no uncommitted changes
workspace_changes = (
    subprocess.check_output("git status --porcelain", shell=True)
    .decode("utf-8")
    .rstrip()
)
if not workspace_changes == "":
    print(
        "There are uncommitted files in your workspace. Please commit these files and try again.".format(
            current_branch
        ),
        file=sys.stderr,
    )
    exit(1)

# Test that git-extras is installed
git_extras_exists = not subprocess.call(["which", "git-extras"])
if not git_extras_exists:
    print(
        "git-extras must be installed, in order to run this script. \
See: https://github.com/tj/git-extras/blob/master/Installation.md",
        file=sys.stderr,
    )
    exit(1)


# Find the new version number
version_type = sys.argv[1]
new_version = ""

if version_type == "major":
    new_version = semver.bump_major(__version__)
elif version_type == "minor":
    new_version = semver.bump_minor(__version__)
elif version_type == "patch":
    new_version = semver.bump_patch(__version__)
else:
    print(
        "The argument must specify a semantic version to be bumped, one of: [major|minor|patch]",
        file=sys.stderr,
    )
    exit(1)

with open(join(PACKAGE, "__version__.py"), "w") as f:
    f.write('__version__ = "{}"\n'.format(new_version))

project_dict = {}
with open("pyproject.toml") as f:
    project_dict = toml.load(f)

project_dict["tool"]["poetry"]["version"] = new_version

with open("pyproject.toml", "w") as f:
    toml.dump(project_dict, f)

system("git add {} {}".format(join(PACKAGE, "__version__.py"), "pyproject.toml"))
system("git release -c --no-empty-commit {}".format(new_version))
