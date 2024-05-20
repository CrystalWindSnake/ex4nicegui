from pathlib import Path
from nicegui import ui
from ex4nicegui import gsap
from .screen import BrowserManager


def test_base(browser: BrowserManager, page_path: str):
    @ui.page(page_path)
    def _():
        gsap.set_defaults({"duration": 0.3})

        ui.label("test from").classes("target-from")
        ui.label("test to").classes("target-to")

        gsap.from_(".target-from", {"x": 50})
        gsap.to(".target-to", {"x": 10})

    page = browser.open(page_path)
    target_from = page.Label(".target-from")
    target_to = page.Label(".target-to")

    target_from.expect_to_have_style("transform", "matrix(1, 0, 0, 1, 0, 0)")
    target_to.expect_to_have_style("transform", "matrix(1, 0, 0, 1, 10, 0)")


def test_run_script(browser: BrowserManager, page_path: str):
    @ui.page(page_path)
    def _():
        gsap.set_defaults({"duration": 0.3})
        ui.label("test").classes("target")

        gsap.run_script(
            r"""
            function setGsap(gsap) {
    gsap.to('.target',{"duration": 0.3,y:60})
}
"""
        )

    page = browser.open(page_path)
    target = page.Label(".target")

    target.expect_to_have_style("transform", "matrix(1, 0, 0, 1, 0, 60)")


def test_run_script_with_file(browser: BrowserManager, page_path: str):
    @ui.page(page_path)
    def _():
        ui.label("test").classes("target")
        gsap.run_script(Path(__file__).parent / "files/gsap_script.js")

    page = browser.open(page_path)
    target = page.Label(".target")

    target.expect_to_have_style("transform", "matrix(1, 0, 0, 1, 0, 20)")
