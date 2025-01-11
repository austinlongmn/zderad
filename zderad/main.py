#!/usr/bin/env python3

import argparse
import os
import tempfile
import re

from colored import Fore, Style

# This program runs in a directory and creates a Microsoft word document
# containing any pseudocode, python, or other code files in the directory for
# coursework submission.


def get_tmp_file():
    "Creates and returns a temporary directory to store files."
    return tempfile.mktemp()


def cleanup(tmp_filename):
    "Removes the temporary directory and all files within it."
    os.unlink(tmp_filename)


def include_file(filename, tmp_file):
    print("include file: ", filename)
    pass


def include_output_images(directory_name, tmp_file):
    print("include output images: ", directory_name)
    pass


directives = {"include": include_file, "output_images": include_output_images}


class ZderadfileDirectiveParameters:
    def __init__(self, directive, args, options):
        self.directive = directive
        self.args = args
        self.options = options

    def __str__(self):
        return (
            "ZderadfileDirectiveParameters(\n"
            + f"  {self.directive},\n"
            + f"  {self.args},\n"
            + f"  {self.options}\n"
            + ")"
        )

    def __repr__(self):
        return str(self)

    def __eq__(self, value):
        if not isinstance(value, ZderadfileDirectiveParameters):
            return False
        return (
            self.directive == value.directive
            and self.args == value.args
            and self.options == value.options
        )


class ZderadfileParseError(Exception):
    pass


def default_raise_diagnostic(message, line):
    raise ZderadfileParseError(f"Error parsing directive: {message}: {line}")


def default_raise_diagnostic_no_ln(message):
    raise ZderadfileParseError(f"Error parsing directive: {message}")


def parse_directive(line, raise_diagnostic=default_raise_diagnostic):
    """Parse the directive and return the directive and filename, along with
    directive arguments."""
    regex_match = re.match(r"^\s*\^\[(.+?)\]\((.+?)\)\s*$", line)
    if regex_match:
        options_str = regex_match.group(1)
        args_str = regex_match.group(2)

        def raise_diagnostic_no_ln(message):
            raise_diagnostic(message, line)

        args = parse_directive_args(args_str)

        directive, options = parse_directive_options(
            options_str, raise_diagnostic
        )

        return ZderadfileDirectiveParameters(directive, args, options)
    else:
        raise ZderadfileParseError(f"Error parsing directive: {line}")


def raise_diagnostic(message, file, line, line_number):
    raise ZderadfileParseError(
        f"Error parsing directive: {message} at {file}:{line_number}:\n{line}"
    )


def parse_directive_options(
    options_str, raise_diagnostic=default_raise_diagnostic_no_ln
):
    PARSING_DIRECTIVE = 0
    PARSING_OPTION_NAME = 1
    PARSING_OPTION_VALUE = 2
    parsing_mode = PARSING_DIRECTIVE
    is_escaped = False
    directive = ""
    option_name = ""
    option_value = ""
    options = {}
    for ch in options_str:
        if parsing_mode == PARSING_DIRECTIVE:
            if is_escaped:
                directive += ch
                is_escaped = False
            elif ch == "\\":
                is_escaped = True
            elif ch.isalpha() or ch == "_":
                directive += ch
            elif ch == ",":
                parsing_mode = PARSING_OPTION_NAME
            else:
                raise_diagnostic(
                    "Directive name must contain only letters and '_'",
                )
        elif parsing_mode == PARSING_OPTION_NAME:
            if is_escaped:
                option_name += ch
                is_escaped = False
            elif ch == "\\":
                is_escaped = True
            elif ch.isalpha() or ch == "_":
                option_name += ch
            elif ch == "=":
                parsing_mode = PARSING_OPTION_VALUE
            elif ch == ",":
                options[option_name] = True
                option_name = ""
                parsing_mode = PARSING_OPTION_NAME
            else:
                raise_diagnostic(
                    "Option name must contain only letters and '_'"
                )
        elif parsing_mode == PARSING_OPTION_VALUE:
            if is_escaped:
                option_value += ch
                is_escaped = False
            elif ch == "\\":
                is_escaped = True
            elif ch == ",":
                options[option_name] = option_value
                option_name = ""
                option_value = ""
                parsing_mode = PARSING_OPTION_NAME
            else:
                option_value += ch
    if option_name:
        options[option_name] = option_value if option_value != "" else True
    return directive, options


def parse_directive_args(args):
    if args == "":
        return {}
    result = []
    argument = ""
    is_escaped = False
    for ch in args:
        if is_escaped:
            argument += ch
            is_escaped = False
        elif ch == "\\":
            is_escaped = True
        elif ch == ",":
            result.append(argument)
            argument = ""
        else:
            argument += ch
    if argument:
        result.append(argument)
    return result


def perform_directive(directive, filename, tmp_file):
    "Perform the directive on the file and write it to the temporary file."
    if directive in directives:
        directives[directive](filename, tmp_file)
    else:
        raise ValueError(f"Unknown directive: {directive}")


def main_loop(tmp_file, input_file, output_file):
    "Main loop to process the input file and create the output file."
    for line in input_file:
        # Match directives that look like this: ^[directive](path/to/file)
        regex_match = re.match(r"^\s+\^\[(.+?)\]\((.+?)\)\s+$", line)
        if regex_match:
            # This is a Zderadfile directive.
            directive = regex_match.group(1)
            filename = regex_match.group(2)
            try:
                perform_directive(directive, filename, tmp_file)
            except ZderadfileParseError as e:
                print(
                    f"{Fore.RED}Error parsing directive: {e}{Style.RESET_ALL}"
                )
        else:
            # This is a normal line.
            tmp_file.write(line)


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
