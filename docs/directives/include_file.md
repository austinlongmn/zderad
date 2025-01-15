# `include` Directive

The `include` directive is perhaps the most basic of the directives. It
allows you to insert the contents of its args in place of the directive.
Observe:

```zderadfile
^[include](file.txt)
```

There can be multiple arguments in this directive, and they can be globs. Here
are the supported options:

| Option or Flag      | Type   | Examples           | Notes                                                                                          |
| ------------------- | ------ | ------------------ | ---------------------------------------------------------------------------------------------- |
| `lang`              | Option | `python`, `md`     | Specifies the language identifier of the file contents.                                        |
| `include_filenames` | Flag   | N/A                | Displays the file name before the contents.                                                    |
| `markdown`          | Flag   | N/A                | Inserts raw markdown, just as if you had typed it into the Zderadfile                          |
| `decrease_headings` | Option | `1`, `2`, `3`, ... | Places the specified number of hash tags at the beginning of any line starting with hash tags. |

## Examples

```zderadfile
^[include](file.txt)
```

```zderadfile
^[include](*.txt)
```

```zderadfile
^[include,lang=python](*.py)
```

```zderadfile
^[include,markdown,decrease_headings=1](README.md)
```
