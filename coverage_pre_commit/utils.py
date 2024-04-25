import os
import re
from typing import Literal

from git.cmd import Git


def make_target_dir(filepath: str):
    """
    Normalises the filepath string and creates the target directory if required.

    :param filepath: Raw target filepath string
    :return: Tuple of directory and file paths
    """
    directory, filename = os.path.split(os.path.normpath(filepath))
    if directory and not os.path.isdir(directory):
        os.makedirs(directory)
    return directory, os.path.join(directory, filename)


def check_if_modified(output_filepath: str, entity: Literal["xml", "badge"]):
    """
    Exits non-zero if generated file has unstaged changes or is untracked (initial creation)

    :param output_filepath: File path to generated file
    :param entity: Generated entity
    """
    error_msg_value = {"xml": "coverage XML report", "badge": "coverage badge"}
    g = Git()
    for line in g.status("-s").split("\n"):
        if re.match(r"[AM ]M ", line):
            if output_filepath in line:
                print(f"Modified {error_msg_value[entity]} at {output_filepath}.")
                exit(1)

    for line in g.ls_files("--others", "--exclude-standard").split("\n"):
        if output_filepath in line:
            print(f"Created {error_msg_value[entity]} at {output_filepath}.")
            exit(1)
