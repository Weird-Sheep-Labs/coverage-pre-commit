import argparse
import os
import re
import subprocess
from uuid import uuid4

from git.cmd import Git


def main():
    # Configure command line args
    parser = argparse.ArgumentParser(description="coverage XML parser")
    parser.add_argument("-o", required=False)
    args = parser.parse_args()

    # Output file path either default or user override
    output_filepath = args.o or "reports/coverage/coverage.xml"

    # Write coverage XML report to tmp location
    tmp_filepath = f"coverage_pre_commit-{uuid4()}.xml"
    subprocess.check_output(["coverage", "xml", "-o", tmp_filepath])

    # Remove timestamp to avoid unnecessary diffs and write to correct location
    output_file = open(output_filepath, mode="r+")
    for line in open(tmp_filepath):
        output_file.write(re.sub(pattern=r"timestamp=\"[0-9]*\"", repl="", string=line))
    os.remove(tmp_filepath)

    # Exits non-zero if generated file has unstaged changes or is
    # untracked (initial creation)
    g = Git()
    for line in g.status("-s").split("\n"):
        print(line)
        if re.match(r"[AM ]M ", line):
            if output_filepath in line:
                print(f"Modified XML report at {output_filepath}.")
                exit(1)

    for line in g.ls_files("--others", "--exclude-standard").split("\n"):
        if output_filepath in line:
            print(f"Created XML report at {output_filepath}.")
            exit(1)
