#!/usr/bin/env python3

import argparse
import os
import tempfile
import re
import typing
import shutil
import glob

from colored import Fore, Style

# This program runs in a directory and creates a Microsoft word document
# containing any pseudocode, python, or other code files in the directory for
# coursework submission.


def get_tmp_file():
    "Creates and returns a temporary directory to store files."
    return tempfile.mktemp()


def cleanup(tmp_filename: str):
    "Removes the temporary directory and all files within it."
    shutil.copy(tmp_filename, "debug/tmp_file.md")
    os.unlink(tmp_filename)


class ZderadfileDirectiveParameters:
    def __init__(
        self, directive: str, args: list[str], options: dict[str, str]
    ):
        self.directive = directive
        self.args = args
        self.options = options

    def get_flag(self, flag_name: str):
        return self.options.get(flag_name, "false").upper() == "TRUE"

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


class ZderadfileDirective:
    def __init__(self, parameters: ZderadfileDirectiveParameters):
        self.parameters = parameters

    def perform(self, tmp_file: typing.TextIO):
        raise NotImplementedError(
            "perform method must be implemented in subclass"
        )


class IncludeFileDirective(ZderadfileDirective):
    def perform(self, tmp_file: typing.TextIO):
        is_markdown = self.parameters.get_flag("markdown")
        decrease_headings = int(
            self.parameters.options.get("decrease_headings", "0")
        )
        language = self.parameters.options.get("lang", "text")
        include_filenames = self.parameters.get_flag("include_filenames")
        for file_glob in self.parameters.args:
            for file in glob.glob(file_glob):
                with open(file, "r") as f:
                    if include_filenames:
                        tmp_file.write(f"`{file}`\n\n")
                    if not is_markdown:
                        tmp_file.write(f"```{language}\n")
                    for line in f:
                        if decrease_headings:
                            line = re.sub(
                                r"^(#+)",
                                ("#" * decrease_headings) + r"\1",
                                line,
                            )
                            line = re.sub(
                                r"#{6,}", "######", line
                            )
                        tmp_file.write(line)
                    if not is_markdown:
                        tmp_file.write("```\n\n")


directives = {"include": IncludeFileDirective}


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
                options[option_name] = "true"
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
        options[option_name] = option_value if option_value != "" else "true"
    return directive, options


def parse_directive_args(args: str):
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


def perform_directive(
    parameters: ZderadfileDirectiveParameters, tmp_file: typing.TextIO
):
    "Perform the directive on the file and write it to the temporary file."
    if parameters.directive in directives:
        directives[parameters.directive](parameters).perform(tmp_file)
    else:
        raise ValueError(f"Unknown directive: {parameters.directive}")


def main_loop(
    tmp_file: typing.TextIO,
    input_file: typing.TextIO,
    output_file: typing.TextIO,
):
    "Main loop to process the input file and create the output file."
    for line in input_file:
        # Match directives that look like this: ^[directive](path/to/file)
        if "^[" in line:
            try:
                directive = parse_directive(line)
                perform_directive(directive, tmp_file)
            except ZderadfileParseError as e:
                print(
                    f"{Fore.RED}Error parsing directive: {e}{Style.RESET_ALL}"
                )
                return 1
            except Exception as err:
                print(
                    f"{Fore.RED}Error performing directive: {err}"
                    + f"{Style.RESET_ALL}"
                )
                return 1
        else:
            # This is a normal line.
            tmp_file.write(line)
    return 0


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
    args = parser.parse_args()

    tmp_filename = get_tmp_file()
    result = 0
    try:
        with open(args.input_file, "r") as input_file, open(
            args.output_file, "w"
        ) as output_file, open(tmp_filename, "w") as tmp_file:
            result = main_loop(tmp_file, input_file, output_file)
    finally:
        cleanup(tmp_filename)
    exit(result)


if __name__ == "__main__":
    main()
