import requirements_wayback_machine
from packaging.version import Version
import os.path as op
from datetime import date
import json
import tempfile


tests_dir = op.dirname(__file__)

# this is response to GET https://pypi.org/pypi/requests/json as of 2023-03-19
requests_json_path = op.join(tests_dir, "./data/requests.json")


def test_parse_pypi_json_api_response() -> None:
    with open(requests_json_path) as fp:
        project_metadata_dict = json.load(fp)

    assert len(project_metadata_dict['releases']) == 148
    releases = requirements_wayback_machine.ProjectRelease.parse_project_metadata(project_metadata_dict)
    assert len(releases) == 145  # releases with date
    assert max(r.version for r in releases) == Version("2.28.2")
    assert min(r.version for r in releases) == Version("0.2.0")
    assert max(r.upload_date for r in releases) == date(2023, 1, 12)
    assert min(r.upload_date for r in releases) == date(2011, 2, 14)


REQUIREMENTS_SIMPLE = """\
requests
packaging
"""

REQUIREMENTS_SIMPLE_ANNOTATED = """\
# requirements_wayback_machine: reference date 2021-12-03
# requirements_wayback_machine: requests<=2.26.0
requests
# requirements_wayback_machine: packaging<=21.3
packaging
"""

def test_requirements_simple() -> None:
    # note: this test depends on live PyPI JSON API!
    with tempfile.TemporaryDirectory() as temp_dir:
        input_path = op.join(temp_dir, "requirements.txt")
        output_path = op.join(temp_dir, "requirements-annotated.txt")

        with open(input_path, "w") as fp:
            fp.write(REQUIREMENTS_SIMPLE)

        assert requirements_wayback_machine.main([
            "-r", input_path,
            "-d", "2021-12-03",
            "-o", output_path
        ]) == 0

        with open(output_path) as fp:
            output = fp.read()

        assert output.strip() == REQUIREMENTS_SIMPLE_ANNOTATED.strip()


REQUIREMENTS_COMPLEX = """\
torch>=1.4.0
torchvision>=0.2.1
imageio
imageio-ffmpeg
matplotlib
configargparse
tensorboard
tqdm
opencv-python
PyMCubes
trimesh
jupyter
lpips
"""

REQUIREMENTS_COMPLEX_ANNOTATED = """\
# requirements_wayback_machine: reference date 2021-02-15
# requirements_wayback_machine: torch<=1.7.1
torch>=1.4.0
# requirements_wayback_machine: torchvision<=0.8.2
torchvision>=0.2.1
# requirements_wayback_machine: imageio<=2.9.0
imageio
# requirements_wayback_machine: imageio-ffmpeg<=0.4.3
imageio-ffmpeg
# requirements_wayback_machine: matplotlib<=3.3.4
matplotlib
# requirements_wayback_machine: configargparse<=1.3
configargparse
# requirements_wayback_machine: tensorboard<=2.4.1
tensorboard
# requirements_wayback_machine: tqdm<=4.56.2
tqdm
# requirements_wayback_machine: opencv-python<=4.5.1.48 (highest version to date; latest release to date is 3.4.13.47)
opencv-python
# requirements_wayback_machine: PyMCubes<=0.1.2
PyMCubes
# requirements_wayback_machine: trimesh<=3.9.5
trimesh
# requirements_wayback_machine: jupyter<=1.0.0
jupyter
# requirements_wayback_machine: lpips<=0.1.3 (highest version to date; latest release to date is 0.1.2)
lpips
"""

def test_requirements_complex() -> None:
    # note: this test depends on live PyPI JSON API!
    with tempfile.TemporaryDirectory() as temp_dir:
        input_path = op.join(temp_dir, "requirements.txt")
        output_path = op.join(temp_dir, "requirements-annotated.txt")

        with open(input_path, "w") as fp:
            fp.write(REQUIREMENTS_COMPLEX)

        assert requirements_wayback_machine.main([
            "-r", input_path,
            "-d", "2021-02-15",
            "-o", output_path
        ]) == 0

        with open(output_path) as fp:
            output = fp.read()

        assert output.strip() == REQUIREMENTS_COMPLEX_ANNOTATED.strip()
