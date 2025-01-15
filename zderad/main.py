#!/usr/bin/env python3

import argparse
import os
import tempfile
import typing
import shutil
import subprocess
import sys

from colored import Fore, Style

from zderad.parser import parse_directive, ZderadfileParseError
import traceback
from zderad.directive import (
    ZderadfileDirectiveParameters,
    ZderadfileDirectiveExecutionError,
)
import zderad.directives as directives

# This program runs in a directory and creates a Microsoft word document
# containing any pseudocode, python, or other code files in the directory for
# coursework submission.


def perform_directive(parameters: ZderadfileDirectiveParameters, tmp_file: typing.TextIO):
    "Perform the directive on the file and write it to the temporary file."
    if parameters.directive in directives.directives:
        directives.directives[parameters.directive](parameters).perform(tmp_file)
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
            except ZderadfileDirectiveExecutionError as e:
                print(f"{Fore.red}Error performing directive: {e}{Style.reset}")
                return 1
            except Exception as err:
                print(
                    f"{Fore.red}Unexpected error while parsing or performing "
                    f"directive: {err}{Style.reset}"
                )
                traceback.print_exc()
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


def convert_pandoc(tmp_filename, output_filename):
    "Converts the temporary file to a Microsoft Word document."
    try:
        return subprocess.run(
            [
                "pandoc",
                "--from",
                "markdown",
                tmp_filename,
                "-o",
                output_filename,
            ]
        ).returncode
    except Exception as e:
        print(
            f"{Fore.red}Error converting to Word document: {e}{Style.reset}",
            file=sys.stderr,
        )
        return 1


def main():
    parser = argparse.ArgumentParser(
        description="Create a Microsoft Word document containing code files."
    )
    parser.add_argument("-i", "--input-file", default="Zderadfile", help="The file to parse")
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
        help="Display debug information. Also saves the temporary file to zderad_tmp.md.",
    )
    args = parser.parse_args()

    tmp_filename = get_tmp_file()
    result = 0
    try:
        with open(args.input_file, "r") as input_file, open(tmp_filename, "w") as tmp_file:
            result = generate_tmp_file(tmp_file, input_file)

        if args.output_file == "zderad/Program.docx":
            try:
                os.mkdir("zderad")
            except FileExistsError:
                pass
            except OSError as e:
                print(f"{Fore.red}Error creating directory: {e}{Style.reset}")
                result = 1

        if convert_pandoc(tmp_filename, args.output_file):
            print(f"{Fore.red}Error converting to Word document{Style.reset}")
            result = 1
    finally:
        cleanup(tmp_filename, args.debug)
    if result:
        exit(result)


if __name__ == "__main__":
    main()
