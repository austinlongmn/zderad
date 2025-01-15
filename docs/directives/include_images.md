# `include_images` Directive

The `include_images` directive is a simple yet helpful directive. It inserts
Markdown links of the glob you provide.

```zderadfile
^[include_images](*.png)
```

There are no options to this directive as of the current version of `zderad`,
but you can use globs for the filename.

## Examples

```zderadfile
^[include_images](*.png)
```

```zderadfile
^[include_images](*.png,output_images/*.png)
```
