import argparse
import os
import re
import subprocess
from uuid import uuid4

from .utils import check_if_modified, make_target_dir


def main():
    # Configure command line args
    parser = argparse.ArgumentParser(description="coverage XML parser")
    parser.add_argument("-o", required=False)
    args = parser.parse_args()

    # Output file path either default or user override
    output_dir, output_filepath = make_target_dir(
        args.o or "reports/coverage/coverage.xml"
    )

    # Write coverage XML report to tmp location
    tmp_filename = f"coverage_pre_commit-{uuid4()}.xml"
    tmp_filepath = os.path.join(output_dir, tmp_filename)
    subprocess.check_output(["coverage", "xml", "-o", tmp_filepath])

    # Remove timestamp to avoid unnecessary diffs and write to correct location
    output_file = open(output_filepath, mode="w+")
    for line in open(tmp_filepath):
        output_file.write(re.sub(pattern=r"timestamp=\"[0-9]*\"", repl="", string=line))
    output_file.close()
    os.remove(tmp_filepath)

    # Handle git checks
    check_if_modified(output_filepath, "xml")
