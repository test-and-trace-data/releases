from website.filters import formatdatestring


def test_formatdatestring_datetime():
    x = formatdatestring("2020-12-23T10:32:16.054492")
    assert x == "23 December 2020, 10:32"


def test_formatdatestring_date():
    x = formatdatestring("2020-12-23")
    assert x == "23 December 2020"
