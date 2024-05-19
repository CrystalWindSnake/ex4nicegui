from ex4nicegui.reactive import rxui
from nicegui import ui
from ex4nicegui import to_ref, effect, new_scope, on
from .screen import BrowserManager
from .utils import set_test_id, ButtonUtils, InputUtils, LabelUtils


def test_can_dispose_temporarily(browser: BrowserManager, page_path: str):
    @ui.page(page_path)
    def _():
        a = to_ref("0")
        scope1_text = to_ref("")
        scope2_text = to_ref("")

        scope1 = new_scope()

        @scope1.run
        def _():
            @on(a)
            def _():
                scope1_text.value = f"scope 1:{a.value}"

        scope2 = new_scope()

        @scope2.run
        def _():
            @effect
            def _():
                scope2_text.value = f"scope 2:{a.value}"

        rxui.input(value=a).classes("input")
        rxui.label(scope1_text).classes("scope1_text")
        rxui.label(scope2_text).classes("scope2_text")
        rxui.button("dispose scope 1", on_click=scope1.dispose).classes(
            "dispose-scope1"
        )
        rxui.button("dispose scope 2", on_click=scope2.dispose).classes(
            "dispose-scope2"
        )

    page = browser.open(page_path)
    page.wait(600)

    input = page.Input(".input")
    scope1_text = page.Label(".scope1_text")
    scope2_text = page.Label(".scope2_text")
    dispose_scope1 = page.Button(".dispose-scope1")
    dispose_scope2 = page.Button(".dispose-scope2")

    # page.pause()

    scope1_text.expect_contain_text("scope 1:0")
    scope2_text.expect_contain_text("scope 2:0")

    input.fill_text("1")
    # page.pause()
    scope1_text.expect_contain_text("scope 1:1")
    scope2_text.expect_contain_text("scope 2:1")

    dispose_scope1.click()

    input.fill_text("2")
    scope1_text.expect_contain_text("scope 1:1")
    scope2_text.expect_contain_text("scope 2:2")

    dispose_scope2.click()

    input.fill_text("3")
    scope1_text.expect_contain_text("scope 1:1")
    scope2_text.expect_contain_text("scope 2:2")
