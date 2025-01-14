# Zderadfile Format

`zderad` is operated with an input file (by default, `./Zderadfile`). The
Zderadfile is, for the most part, a normal Markdown file. You can find
information on how a markdown file works
[here](https://www.markdownguide.org/getting-started/).

The part where the Zderadfile is different is in its "Zderadfile directives".
They look like this:

```markdown
^[directive](args)
```

As you can see, a Zderadfile directive is simply a Markdown link with a carat
(`^`) prepended before the opening bracket. Zderadfile directives can take
options and args like so:

```markdown
^[directive,flag,option=value](arg 1, arg 2, arg 3)
```

The commas and equals signs can be escaped with a backslash (`\`). However,
Zderadfiles do not yet support escaping the brackets or parentheses. (PRs are
welcome!).

You can find more information on the specific commands in the
[/docs/directives](/docs/directives/) folder.
