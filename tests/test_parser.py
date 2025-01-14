import zderad.parser as parser


def test_parse_directive():
    assert parser.parse_directive(
        "  ^[include](file.py)  "
    ) == parser.ZderadfileDirectiveParameters("include", ["file.py"], {})


def test_parse_directive_arg():
    assert parser.parse_directive(
        "^[output_images](path/to/directory)"
    ) == parser.ZderadfileDirectiveParameters(
        "output_images", ["path/to/directory"], {}
    )


def test_parse_directive_flags():
    assert parser.parse_directive(
        "^[include,flag_a,flag_b](file.py)"
    ) == parser.ZderadfileDirectiveParameters(
        "include", ["file.py"], {"flag_a": "true", "flag_b": "true"}
    )


def test_parse_directive_options():
    assert parser.parse_directive(
        "  ^[include,flag_a,option_a=abc def 1234 bob / 2,"
        + "flag_b,option_b=1234](file.py)  "
    ) == parser.ZderadfileDirectiveParameters(
        "include",
        ["file.py"],
        {
            "flag_a": "true",
            "flag_b": "true",
            "option_a": "abc def 1234 bob / 2",
            "option_b": "1234",
        },
    )


def test_parse_directive_args():
    assert parser.parse_directive(
        "  ^[include,flag_a,option_a=abc def 1234 bob / 2,"
        + "flag_b,option_b=1234](test/file.py,abc 123 456,another_arg is here)"
    ) == parser.ZderadfileDirectiveParameters(
        "include",
        ["test/file.py", "abc 123 456", "another_arg is here"],
        {
            "flag_a": "true",
            "flag_b": "true",
            "option_a": "abc def 1234 bob / 2",
            "option_b": "1234",
        },
    )


def test_parse_directive_args_no_options():
    assert parser.parse_directive(
        "  ^[include](test/file.py,abc 123 456,another_arg is here)"
    ) == parser.ZderadfileDirectiveParameters(
        "include", ["test/file.py", "abc 123 456", "another_arg is here"], {}
    )


def test_parse_directive_option_escapes():
    assert parser.parse_directive(
        "^[include,flag_a=abc\\,def\\,1234\\,bob\\,\\/\\,2](file.py)"
    ) == parser.ZderadfileDirectiveParameters(
        "include", ["file.py"], {"flag_a": "abc,def,1234,bob,/,2"}
    )


def test_parse_directive_args_escapes():
    assert parser.parse_directive(
        "^[include](test/file.py,abc\\,123\\,456,another_arg\\\\is\\\\here)"
    ) == parser.ZderadfileDirectiveParameters(
        "include", ["test/file.py", "abc,123,456", "another_arg\\is\\here"], {}
    )
