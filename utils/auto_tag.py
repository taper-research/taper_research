#! python3
"""
- Ensure git status is clear.
- Read the project.toml,
- Obtain version as `v`.
- tag the git repo with `v`.
- Display the required shell command to:
    - Push the tags
"""
import os
import re
import subprocess
import sys
import textwrap
from pathlib import Path

pwd = Path(os.path.dirname(__file__)).resolve()
project_root = pwd.parent


def error(*args, **kwargs):
    print(*args, **kwargs, file=sys.stderr)


def is_git_clean():
    git_status = subprocess.run(
        ["git", "status", "--porcelain"], stdout=subprocess.PIPE, cwd=project_root
    )
    return not git_status.stdout.decode("utf-8").strip()


def check_tag_exists(tag_name):
    """
    Function to check if a tag exists in a git repository
    :param tag_name: The name of the tag to be checked
    :return: True if tag exists, False otherwise
    """
    output = subprocess.check_output(
        f"git tag --list {tag_name}", shell=True, cwd=project_root
    ).decode("utf-8")
    print(output)
    return tag_name in output


def tag_repository(tag_name):
    """
    Function to tag a git repository with a new tag
    :param tag_name: The name of the tag to be created
    :return: True if tag creation is successful, False otherwise
    """
    try:
        subprocess.check_output(f"git tag {tag_name}", shell=True, cwd=project_root)
        return True
    except subprocess.CalledProcessError:
        return False


def main():
    project_toml = (project_root / "pyproject.toml").read_text()
    version = re.findall(r'version = "([^"]+)".*', project_toml)
    assert len(version) == 1
    version = version[0]
    print(f"Detected {version=}")

    if not is_git_clean():
        error("Git repository not clean.")
        return -1
    if check_tag_exists(version):
        error(f"Tag {version} exists.")
        return -1
    tag_repository(version)

    msg = f"""
    To push this single tag:
        git push origin {version}
    To push all tags:
        git push --tags
    """
    print(textwrap.dedent(msg))
    return 0


if __name__ == "__main__":
    sys.exit(main())
