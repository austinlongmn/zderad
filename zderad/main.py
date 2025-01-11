#!/usr/bin/env python3

import argparse
import os
import tempfile
import re

# This program runs in a directory and creates a Microsoft word document
# containing any psudocode, python, or other code files in the directory for
# coursework submission.


def get_tmp_file():
    "Creates and returns a temporary directory to store files."
    return tempfile.mktemp()


def cleanup(tmp_filename):
    "Removes the temporary directory and all files within it."
    os.unlink(tmp_filename)


def main_loop(tmp_file, input_file, output_file):
    "Main loop to process the input file and create the output file."
    for line in input_file:
        # Match directives that look like this: ^[directive](path/to/file)
        regex_match = re.match(r"^\s+\^\[(.+?)\]\((.+?)\)\s+$", line)
        if regex_match:
            # This is a Zderadfile directive.
            directive = regex_match.group(1)
            filename = regex_match.group(2)
            perform_directive(directive, filename, tmp_file)
        else:
            # This is a normal line.
            tmp_file.write(line)


def include_file(filename, tmp_file):
    print("include file: ", filename)
    pass


def include_output_images(directory_name, tmp_file):
    print("include output images: ", directory_name)
    pass


directives = {"include": include_file, "output_images": include_output_images}


class ZderadfileDirectiveParameters:
    def __init__(self, directive, args):
        self.directive = directive
        self.args = args

    def __repr__(self):
        return f"ZderadfileDirectiveParameters({self.directive}, {self.args})"

    def __eq__(self, value):
        if not isinstance(value, ZderadfileDirectiveParameters):
            return False
        return self.directive == value.directive and self.args == value.args


class ZderadfileParseError(Exception):
    pass


def parse_directive(line):
    """Parse the directive and return the directive and filename, along with
    directive arguments."""
    regex_match = re.match(r"^\s*\^\[(.+?)\]\((.+?)\)\s*$", line)
    if regex_match:
        directive_and_args = regex_match.group(1)
        filename = regex_match.group(2)

        PARSING_DIRECTIVE = 0
        PARSING_ARG_NAME = 1
        PARSING_ARG_VALUE = 2
        parsing_mode = PARSING_DIRECTIVE
        directive = ""
        arg_name = ""
        arg_value = ""
        args = {}
        if filename:
            args["filename"] = filename
        for ch in directive_and_args:
            if parsing_mode == PARSING_DIRECTIVE:
                if ch.isalpha() or ch == "_":
                    directive += ch
                elif ch == ",":
                    parsing_mode = PARSING_ARG_NAME
                else:
                    raise ZderadfileParseError(
                        "Error parsing directive: directive must be alphabetic"
                        + f'or "_": {line}'
                    )
            elif parsing_mode == PARSING_ARG_NAME:
                if ch.isalpha() or ch == "_":
                    arg_name += ch
                elif ch == "=":
                    parsing_mode = PARSING_ARG_VALUE
                elif ch == ",":
                    args[arg_name] = True
                    arg_name = ""
                    parsing_mode = PARSING_ARG_NAME
                else:
                    raise ZderadfileParseError(
                        "Error parsing directive: argument name must be"
                        + f'alphabetic or "_": {line}'
                    )
            elif parsing_mode == PARSING_ARG_VALUE:
                if ch == ",":
                    args[arg_name] = arg_value
                    arg_name = ""
                    arg_value = ""
                    parsing_mode = PARSING_ARG_NAME
                else:
                    arg_value += ch
        if arg_name:
            args[arg_name] = arg_value if arg_value != "" else True
        return ZderadfileDirectiveParameters(directive, args)
    else:
        raise ZderadfileParseError(f"Error parsing directive: {line}")


def perform_directive(directive, filename, tmp_file):
    "Perform the directive on the file and write it to the temporary file."
    if directive in directives:
        directives[directive](filename, tmp_file)
    else:
        raise ValueError(f"Unknown directive: {directive}")


def main():
    parser = argparse.ArgumentParser(
        description="Create a Microsoft Word document containing code files."
    )
    parser.add_argument(
        "-i", "--input-file", default="Zderadfile", help="The file to parse"
    )
    parser.add_argument("output", help="The output file.")
    args = parser.parse_args()

    tmp_filename = get_tmp_file()
    try:
        with open(args.input_file, "r") as input_file, open(
            args.output_file, "w"
        ) as output_file, open(tmp_filename, "w") as tmp_file:
            main_loop(tmp_file, input_file, output_file)
    finally:
        cleanup(tmp_filename)


if __name__ == "__main__":
    main()
