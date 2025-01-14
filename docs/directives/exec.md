# `exec` Directive

The `exec` directive is the most powerful (and dangerous) of the directives. It
allows you to execute a shell command and insert the resulting STDOUT into your
file.

```zderadfile
^[exec](whoami)
```

Here are the supported options:

| Option or Flag    | Type   | Examples       | Notes                                                   |
| ----------------- | ------ | -------------- | ------------------------------------------------------- |
| `lang`            | Option | `python`, `md` | Specifies the language identifier of the file contents. |
| `include_command` | Flag   | N/A            | Displays the command before the results.                |

## Examples

```zderadfile
^[exec](python3 my_program.py)
```

```zderadfile
^[exec](cat file.txt)
```
