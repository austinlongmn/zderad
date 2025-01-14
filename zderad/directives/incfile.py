import re
import typing
import glob

from zderad.directive import ZderadfileDirective


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
                            line = re.sub(r"#{6,}", "######", line)
                        tmp_file.write(line)
                    if not is_markdown:
                        tmp_file.write("```\n\n")
