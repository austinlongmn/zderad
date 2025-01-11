import zderad.main as zderad


def test_parse_directive():
    assert zderad.parse_directive(
        "  ^[include](file.py)  "
    ) == zderad.ZderadfileDirectiveParameters("include", ["file.py"], {})


def test_parse_directive_arg():
    assert zderad.parse_directive(
        "^[output_images](path/to/directory)"
    ) == zderad.ZderadfileDirectiveParameters(
        "output_images", ["path/to/directory"], {}
    )


def test_parse_directive_flags():
    assert zderad.parse_directive(
        "^[include,flag_a,flag_b](file.py)"
    ) == zderad.ZderadfileDirectiveParameters(
        "include", ["file.py"], {"flag_a": True, "flag_b": True}
    )


def test_parse_directive_options():
    assert zderad.parse_directive(
        "  ^[include,flag_a,option_a=abc def 1234 bob / 2,"
        + "flag_b,option_b=1234](file.py)  "
    ) == zderad.ZderadfileDirectiveParameters(
        "include",
        ["file.py"],
        {
            "flag_a": True,
            "flag_b": True,
            "option_a": "abc def 1234 bob / 2",
            "option_b": "1234",
        },
    )


def test_parse_directive_args():
    assert zderad.parse_directive(
        "  ^[include,flag_a,option_a=abc def 1234 bob / 2,"
        + "flag_b,option_b=1234](test/file.py,abc 123 456,another_arg is here)"
    ) == zderad.ZderadfileDirectiveParameters(
        "include",
        ["test/file.py", "abc 123 456", "another_arg is here"],
        {
            "flag_a": True,
            "flag_b": True,
            "option_a": "abc def 1234 bob / 2",
            "option_b": "1234",
        },
    )
