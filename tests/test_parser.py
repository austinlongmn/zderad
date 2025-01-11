import zderad
import json

def test_parse_directive():
    assert zderad.parse_directive(
        "  ^[include](file.py)  "
    ) == zderad.ZderadfileDirectiveParameters("include", {"filename": "file.py"})
    assert zderad.parse_directive(
        "^[output_images](path/to/directory)"
    ) == zderad.ZderadfileDirectiveParameters(
        "output_images", {"filename": "path/to/directory"}
    )
    assert zderad.parse_directive(
        "^[include,flag_a,flag_b](file.py)"
    ) == zderad.ZderadfileDirectiveParameters(
        "include", {"filename": "file.py", "flag_a": True, "flag_b": True}
    )
    assert zderad.parse_directive(
        "  ^[include,flag_a,option_a=abc def 1234 bob / 2,flag_b,option_b=1234](file.py)  "
    ) == zderad.ZderadfileDirectiveParameters(
        "include", {"filename": "file.py", "flag_a": True, "flag_b": True, "option_a": "abc def 1234 bob / 2", "option_b": "1234"}
    )
