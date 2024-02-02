from pathlib import Path
from nicegui import ui
from ex4nicegui import gsap
from .screen import ScreenPage
from .utils import LabelUtils, set_test_id


def test_base(page: ScreenPage, page_path: str):
    @ui.page(page_path)
    def _():
        gsap.set_defaults({"duration": 0.3})

        set_test_id(ui.label("test from").classes("target-from"), "label from")
        set_test_id(ui.label("test to").classes("target-to"), "label to")

        gsap.from_(".target-from", {"x": 50})
        gsap.to(".target-to", {"x": 10})

    page.open(page_path)
    target_from = LabelUtils(page, "label from")
    target_to = LabelUtils(page, "label to")
    page.wait(1500)

    assert target_from.get_style("transform") == "translate(0px, 0px)"
    assert target_to.get_style("transform") == "translate(10px, 0px)"


def test_run_script(page: ScreenPage, page_path: str):
    @ui.page(page_path)
    def _():
        gsap.set_defaults({"duration": 0.3})
        set_test_id(ui.label("test").classes("target"), "label")

        gsap.run_script(
            r"""function setGsap(gsap) {
    gsap.to('.target',{"duration": 0.3,y:60})
}
"""
        )

    page.open(page_path)
    target = LabelUtils(page, "label")
    page.wait(1500)
    assert target.get_style("transform") == "translate(0px, 60px)"


def test_run_script_with_file(page: ScreenPage, page_path: str):
    @ui.page(page_path)
    def _():
        set_test_id(ui.label("test").classes("target"), "label")
        gsap.run_script(Path(__file__).parent / "files/gsap_script.js")

    page.open(page_path)
    target = LabelUtils(page, "label")

    page.wait(1500)
    assert target.get_style("transform") == "translate(0px, 20px)"
