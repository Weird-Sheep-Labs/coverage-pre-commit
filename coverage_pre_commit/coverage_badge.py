import argparse
import os
import subprocess
import sys

from .utils import check_if_modified, make_target_dir


def main():
    # Configure command line args
    parser = argparse.ArgumentParser(description="coverage badge parser")
    parser.add_argument("-i", required=False)
    parser.add_argument("-o", required=False)
    args = parser.parse_args()

    # File paths either default or user override
    _, input_filepath = make_target_dir(args.i or "reports/coverage/coverage.xml")
    _, output_filepath = make_target_dir(
        args.o or "reports/coverage/coverage-badge.svg"
    )

    # Check input file location is valid and exit 1 if not
    if not os.path.exists(input_filepath):
        print(f"Could not find coverage report: {input_filepath}.")
        sys.exit(1)

    # Generate coverage badge
    subprocess.check_output(
        ["genbadge", "coverage", "-i", input_filepath, "-o", output_filepath]
    )

    # Handle git checks
    check_if_modified(output_filepath, "badge")
