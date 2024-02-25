import pytest
from ex4nicegui import to_ref, ref_computed, effect


@pytest.mark.noautofixt
def test_when_error():
    dummy = []

    try:
        pass
        s = to_ref(1)

        @ref_computed
        def cp():
            if s.value > 1:
                raise Exception("")

            return s.value + 1

        @effect
        def _():
            dummy.append(cp.value)

        s.value = 2
    except Exception as e:
        s.value = -1

    assert dummy == [2, 0]
