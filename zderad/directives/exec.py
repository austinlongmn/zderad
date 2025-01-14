import subprocess

from zderad.directive import ZderadfileDirective


class ExecDirective(ZderadfileDirective):
    def perform(self, tmp_file):
        language = self.parameters.options.get("lang", "text")
        include_command = self.parameters.get_flag("include_command")
        command = self.parameters.args[0]
        process = subprocess.Popen(
            command,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        stdout, _ = process.communicate()
        if include_command:
            tmp_file.write(f"`{command}`\n\n")
        tmp_file.write(f"```{language}\n")
        tmp_file.write(stdout.decode("utf-8"))
        tmp_file.write("```\n\n")
