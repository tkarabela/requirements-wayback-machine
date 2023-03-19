#!/usr/bin/env python3

# Copyright (c) 2023 Tomas Karabela
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

"""
Requirements Wayback Machine
============================

This script adds comments to pip `requirements.txt` file describing
how it would resolve at given date in the past. This is useful if you're
trying to fix underspecified dependencies that no longer build.

It's implemented in terms of `packaging` Python API and PyPI JSON API.
Parsing and resolution of requirement lines is simplified; it only considers
specifiers (lines like `requests` or `requests<=2.26,>1.0` will be interpreted
correctly, while more complex forms may be misinterpreted or skipped).

Example use:

    $ cat requirements.txt
    requests
    packaging

    $ requirements_wayback_machine.py -r requirements.txt -d 2021-12-03
    # requirements_wayback_machine: reference date 2021-12-03
    # requirements_wayback_machine: requests<=2.26.0
    requests
    # requirements_wayback_machine: packaging<=21.3
    packaging

"""

import argparse
import sys
from dataclasses import dataclass
from datetime import date
import traceback
import re
from typing import TypedDict, Any, Optional
from packaging.requirements import Requirement
import packaging.version
import os.path as op
import requests


__version__ = "0.1.1"


class ProjectReleaseDict(TypedDict):
    """
    Entry in the `releases` dict in `ProjectMetadataDict`
    """
    upload_time: str
    upload_time_iso_8681: str
    yanked: bool
    requires_python: Optional[str]


class ProjectMetadataDict(TypedDict):
    """
    Response from GET /pypi/<project_name>/json

    Reference:
        https://warehouse.pypa.io/api-reference/json.html#get--pypi--project_name--json

    """
    info: dict[str, Any]
    releases: dict[str, list[ProjectReleaseDict]]
    urls: list[Any]
    vulnerabilities: list[Any]


def get_release_date(d: ProjectReleaseDict) -> date:
    return date.fromisoformat(d['upload_time'][:10])


@dataclass
class ProjectRelease:
    """
    A project release on PyPI

    Only releases with some uploaded artifacts are considered.

    Attributes:
        version: eg. packaging.version.Version("1.0")
        upload_date: earliest `upload_time` of an artifact for this version (Python `date`)

    """
    version: packaging.version.Version
    upload_date: date

    @classmethod
    def parse_project_metadata(cls, d: ProjectMetadataDict) -> list['ProjectRelease']:
        output = []
        for version_name, release_list in d['releases'].items():
            version = packaging.version.parse(version_name)
            version_upload_date = min(map(get_release_date, release_list), default=None)
            if version_upload_date is None:
                continue

            output.append(cls(
                version=version,
                upload_date=version_upload_date
            ))

        return output


def query_project_releases(project_name: str) -> list[ProjectRelease]:
    """Ask PyPI JSON API for information about project releases"""
    response = requests.get(f"https://pypi.org/pypi/{project_name}/json")
    project_metadata_dict: ProjectMetadataDict = response.json()
    releases = ProjectRelease.parse_project_metadata(project_metadata_dict)
    return releases


def process_requirements_file(requirements_file_path: str, reference_date: date) -> str:
    """Return annotated requirements.txt file"""
    requirements_filename = op.basename(requirements_file_path)
    output_lines = [
        f"# requirements_wayback_machine: reference date {reference_date.isoformat()}",
    ]
    with open(requirements_file_path) as fp:
        input_lines = list(fp)

    for lineno, input_line in enumerate(input_lines, 1):
        input_line = input_line.rstrip()

        if re.fullmatch(r"\s*(#.*)?", input_line):
            # empty or comment line
            output_lines.append(input_line)
            continue

        try:
            req = Requirement(input_line)
            releases = query_project_releases(req.name)
            releases_to_date = [r for r in releases if r.upload_date <= reference_date]
            matching_versions = list(req.specifier.filter([r.version for r in releases_to_date]))
            matching_releases = [r for r in releases_to_date if r.version in matching_versions]

            if not matching_versions:
                output_lines.append(f"# requirements_wayback_machine: warning - no matching version found for {req.name}{req.specifier}")
                output_lines.append(input_line)
                continue

            highest_version = max(matching_versions)
            latest_version = max(matching_releases, key=lambda r: r.upload_date).version

            if highest_version != latest_version:
                output_lines.append(f"# requirements_wayback_machine: {req.name}<={highest_version} (highest version to date; latest release to date is {latest_version})")
            else:
                output_lines.append(f"# requirements_wayback_machine: {req.name}<={highest_version}")
            output_lines.append(input_line)

        except Exception as e:
            print(f"{requirements_filename}:{lineno} - error:", e, file=sys.stderr)
            output_lines.append(input_line)

    return "\n".join(output_lines)


def main(argv: Optional[list[str]] = None) -> int:
    if argv is None:
        argv = sys.argv[1:]

    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument(
        "-r", "--requirement",
        dest="requirements_file_path",
        required=True,
        metavar='requirements.txt',
        help="path to requirements.txt file"
    )
    parser.add_argument(
        "-d", "--date",
        dest="reference_date",
        type=date.fromisoformat,
        default=date.today(),
        metavar='YYYY-MM-DD',
        help="reference date (default: today)"
    )
    parser.add_argument(
        "-o", "--output",
        dest="output_path",
        metavar='requirements-annotated.txt',
        help="write annotated output to file (default: print to stdout)"
    )
    args = parser.parse_args(argv)
    requirements_file_path: str = args.requirements_file_path
    reference_date: date = args.reference_date
    output_path: Optional[str] = args.output_path

    try:
        new_requirements_file = process_requirements_file(requirements_file_path, reference_date)

        if output_path is None:
            print(new_requirements_file)
        else:
            with open(output_path, "w", encoding="utf-8") as fp:
                print(new_requirements_file, file=fp)
    except Exception:
        traceback.print_exc()
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
