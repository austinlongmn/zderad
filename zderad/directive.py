import typing


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
