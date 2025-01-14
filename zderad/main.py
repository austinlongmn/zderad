#!/usr/bin/env python3

import argparse
import os
import tempfile
import typing
import shutil
import subprocess

from colored import Fore, Style

from zderad.parser import parse_directive, ZderadfileParseError
from zderad.directive import ZderadfileDirectiveParameters
import zderad.directives as directives

# This program runs in a directory and creates a Microsoft word document
# containing any pseudocode, python, or other code files in the directory for
# coursework submission.


directives = {
    "include": directives.IncludeFileDirective,
    "include_images": directives.IncludeOutputImagesDirective,
}


def perform_directive(
    parameters: ZderadfileDirectiveParameters, tmp_file: typing.TextIO
):
    "Perform the directive on the file and write it to the temporary file."
    if parameters.directive in directives:
        directives[parameters.directive](parameters).perform(tmp_file)
    else:
        raise ValueError(f"Unknown directive: {parameters.directive}")


def generate_tmp_file(
    tmp_file: typing.TextIO,
    input_file: typing.TextIO,
):
    "Main loop to process the input file and create the output file."
    for line in input_file:
        # Match directives that look like this: ^[directive](path/to/file)
        if "^[" in line:
            try:
                directive = parse_directive(line)
                perform_directive(directive, tmp_file)
            except ZderadfileParseError as e:
                print(f"{Fore.red}Error parsing directive: {e}{Style.reset}")
                return 1
            except Exception as err:
                print(
                    f"{Fore.red}Error performing directive: {err}"
                    + f"{Style.reset}"
                )
                return 1
        else:
            # This is a normal line.
            tmp_file.write(line)
    return 0


def pandoc_convert(input_file: str, output_file: str):
    "Converts the input file to a Microsoft Word document."
    return os.system(f"pandoc {input_file} -o {output_file}")


def get_tmp_file():
    "Creates and returns a temporary directory to store files."
    return tempfile.mktemp()


def cleanup(tmp_filename: str, keep_tmp_file=False):
    "Removes the temporary directory and all files within it."
    if keep_tmp_file:
        shutil.copy(tmp_filename, "zderad_tmp.md")
    os.unlink(tmp_filename)


def main():
    parser = argparse.ArgumentParser(
        description="Create a Microsoft Word document containing code files."
    )
    parser.add_argument(
        "-i", "--input-file", default="Zderadfile", help="The file to parse"
    )
    parser.add_argument(
        "-o",
        "--output-file",
        default="zderad/Program.docx",
        help="The output file.",
    )
    parser.add_argument(
        "-D",
        "--debug",
        action="store_true",
        help="Display debug information. Also saves the temporary file to"
        + "zderad_tmp.md.",
    )
    args = parser.parse_args()

    tmp_filename = get_tmp_file()
    result = 0
    try:
        with open(args.input_file, "r") as input_file, open(
            tmp_filename, "w"
        ) as tmp_file:
            result = generate_tmp_file(tmp_file, input_file)
        if (
            subprocess.run(
                [
                    "pandoc",
                    "--from",
                    "markdown",
                    tmp_filename,
                    "-o",
                    args.output_file,
                ]
            ).returncode
            != 0
        ):
            print(f"{Fore.red}Error converting to Word document{Style.reset}")
            result = 1
    finally:
        cleanup(tmp_filename, args.debug)
    exit(result)


if __name__ == "__main__":
    main()
