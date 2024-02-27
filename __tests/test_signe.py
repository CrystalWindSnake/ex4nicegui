from nicegui import ui
import pytest
from ex4nicegui import to_ref, on, effect, event_batch
from .screen import ScreenPage
from .utils import fn, ButtonUtils, set_test_id


@pytest.mark.skip("todo")
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


def test_batch_event(page: ScreenPage, page_path: str):
    a = to_ref(0)
    b = to_ref(0)

    # test on
    @fn
    def fn_on_times():
        pass

    def fn_on():
        a.value
        b.value
        fn_on_times()

    on([a, b], onchanges=True)(fn_on)

    # test effect
    @fn
    def fn_effect():
        a.value
        b.value

    effect(fn_effect)

    @ui.page(page_path)
    def _():
        @event_batch
        def when_click():
            a.value += 1
            b.value += 1

        ui.button("change all values", on_click=when_click)

    page.open(page_path)

    assert fn_on_times.calledTimes == 0
    assert fn_effect.calledTimes == 1

    page.wait()
    page._page.get_by_role("button", name="change all values").click()

    assert fn_on_times.calledTimes == 1
    assert fn_effect.calledTimes == 2


@pytest.mark.skip("todo")
def test_sync_scheduler(page: ScreenPage, page_path: str):
    # reset_execution_scheduler("sync")

    a = to_ref(0)
    dummy = []

    @ui.page(page_path)
    def _():
        @on(a, onchanges=True)
        def _():
            a.value
            dummy.append("effect")

        def when_click():
            dummy.append("start")
            a.value += 1
            dummy.append("end")

        set_test_id(ui.button("change", on_click=when_click), "target")

    page.open(page_path)

    btn = ButtonUtils(page, "target")
    btn.click()

    page.wait(1500)
    assert dummy == ["start", "effect", "end"]


@pytest.mark.skip("todo")
def test_post_event_scheduler(page: ScreenPage, page_path: str):
    # reset_execution_scheduler("post-event")

    a = to_ref(0)
    dummy = []

    @ui.page(page_path)
    def _():
        @on(a, onchanges=True)
        def _():
            a.value
            dummy.append("effect")

        def when_click():
            dummy.append("start")
            a.value += 1
            dummy.append("end")

        set_test_id(ui.button("change", on_click=when_click), "target")

    page.open(page_path)

    btn = ButtonUtils(page, "target")
    btn.click()

    page.wait(1500)
    assert dummy == ["start", "end", "effect"]

    reset_execution_scheduler("sync")  # noqa: F821
