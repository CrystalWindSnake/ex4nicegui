import pytest
from ex4nicegui import to_ref, on


def test_on_priority_level():
    foo = to_ref("org")
    records = []

    @on(foo, onchanges=True, priority_level=2)
    def _():
        records.append("first")

    @on(foo, onchanges=True)
    def _():
        records.append("second")

    foo.value = "new"
    assert records == ["second", "first"]
