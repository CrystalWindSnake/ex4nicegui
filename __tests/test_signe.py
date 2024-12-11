from nicegui import ui
from ex4nicegui import to_ref, on, effect, event_batch
from .screen import BrowserManager


def test_batch_event(browser: BrowserManager, page_path: str):
    @ui.page(page_path)
    def _():
        a = to_ref(0)
        b = to_ref(0)
        lbl_fn_on_times = ui.label("0").classes("label-fn-on-times")
        lbl_fn_effect_times = ui.label("0").classes("label-fn-effect-times")

        @on([a, b], onchanges=True)
        def fn_on():
            a.value
            b.value
            lbl_fn_on_times.set_text(str(int(lbl_fn_on_times.text) + 1))

        @effect
        def fn_effect():
            a.value
            b.value
            lbl_fn_effect_times.set_text(str(int(lbl_fn_effect_times.text) + 1))

        @event_batch
        def when_click():
            a.value += 1
            b.value += 1

        ui.button("change all values", on_click=when_click).classes("btn")

    page = browser.open(page_path)

    btn = page.Button(".btn")
    label_fn_on_times = page.Label(".label-fn-on-times")
    label_fn_effect_times = page.Label(".label-fn-effect-times")

    label_fn_on_times.expect_contain_text("0")
    label_fn_effect_times.expect_contain_text("1")

    btn.click()

    label_fn_on_times.expect_contain_text("1")
    label_fn_effect_times.expect_contain_text("2")
