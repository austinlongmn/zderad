import typing
import glob

from zderad.directive import ZderadfileDirective


class IncludeOutputImagesDirective(ZderadfileDirective):
    def perform(self, tmp_file: typing.TextIO):
        for file_glob in self.parameters.args:
            for file in glob.glob(file_glob):
                tmp_file.write(f"![]({file})\n\n")
