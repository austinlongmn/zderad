import re

from zderad.directive import ZderadfileDirectiveParameters


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
