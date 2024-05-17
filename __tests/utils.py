from __future__ import annotations

import re
from typing import List, Optional, Any, Callable, Union
from playwright.sync_api import expect, Locator, Page

from typing_extensions import Protocol, Self


class IPropsAble(Protocol):
    def props(
        self,
        add: Optional[str] = None,
        *,
        remove: Optional[str] = None,
    ) -> Self:
        ...


def set_test_id(element: IPropsAble, id: str):
    return element.props(f'data-testid="{id}"')


class fn:
    def __init__(self, fn: Optional[Callable] = None) -> None:
        self._fn = fn
        self._called_count = 0

    def mockClear(self):
        self._called_count = 0
        return self

    @property
    def calledTimes(self):
        return self._called_count

    def toHaveBeenCalled(self):
        return self.calledTimes > 0

    def __call__(self, *args: Any, **kwds: Any) -> Any:
        if self._fn is None:
            pass
            self._called_count += 1
            return

        assert self._fn is not None
        result = self._fn(*args, **kwds)
        self._called_count += 1

        return result


def tran_str(value):
    if isinstance(value, str):
        return f"'{value}'"
    return value


class BaseUiUtils:
    def __init__(
        self,
        page: Page,
        target_locator: Union[str, Locator],
    ) -> None:
        if isinstance(target_locator, str):
            target_locator = page.locator(target_locator)

        self.page = page
        self.target_locator = target_locator

    def expect_find_by_class(self, classes: Union[List[str], str]):
        target = self.target_locator.filter(has=self.page.locator(f".{classes}"))
        expect(target).to_be_visible()

    def expect_to_have_class(self, classes: Union[List[str], str]):
        expect(self.target_locator).to_have_class(classes)

    def expect_not_to_have_class(self, classes: Union[List[str], str]):
        expect(self.target_locator).not_to_have_class(classes)

    def expect_to_contain_class(self, *classes: str):
        for cls in classes:
            expect(self.target_locator).to_have_class(re.compile(cls))

    def expect_not_to_contain_class(self, *classes: str):
        for cls in classes:
            expect(self.target_locator).not_to_have_class(re.compile(cls))

    def get_style_attr_value(self) -> str:
        return self.target_locator.evaluate("element => element.getAttribute('style')")

    def get_style(self, name: str):
        return self.target_locator.evaluate(f"node=> node.style.{name}")

    def expect_to_be_visible(self):
        expect(self.target_locator).to_be_visible()

    def expect_to_have_text(self, text: str):
        expect(self.target_locator).to_have_text(text)

    def expect_not_to_have_text(self, text: str):
        expect(self.target_locator).not_to_have_text(text)

    def expect_to_have_value(self, value: str):
        return expect(self.target_locator).to_have_value(value)

    def expect_not_to_have_value(self, value: str):
        return expect(self.target_locator).not_to_have_value(value)

    def get_by_text(self, text: str):
        return self.target_locator.get_by_text(text)

    def expect_to_be_hidden(self):
        expect(self.target_locator).to_be_hidden()

    @property
    def expect(self):
        return expect(self.target_locator)


class SelectUtils(BaseUiUtils):
    def __init__(self, page: Page, target_locator: Union[str, Locator]) -> None:
        super().__init__(page, target_locator)

    def show_popup_click(self):
        self.target_locator.click()
        self.page.wait_for_timeout(600)

    def click(self):
        self.target_locator.click()

    def get_options_values(self):
        return self.page.locator(
            "css= .q-menu.q-position-engine.scroll > .q-virtual-scroll__content > * "
        ).all_inner_texts()

    def click_cancel(self):
        self.page.get_by_role("button", name="cancel").click()

    def click_and_select(self, value: str):
        self.click()
        # self.page.wait_for_timeout(500)
        # self.target_locator.filter(has_text="namearrow_drop_down").locator("i").click()

        self.page.get_by_role("option", name=value).click()

    # def get_input_value(self):
    #     return self.target_locator.input_value()

    # def expect_have_value(self, value: str):
    #     return expect(self.target_locator).to_have_value(value)

    def get_selected_values(self):
        return self.target_locator.locator(".q-chip__content").all_inner_texts()

    def input_and_enter(self, text: str):
        self.target_locator.type(text)
        self.page.wait_for_timeout(500)
        self.target_locator.press("Enter")


class ColorPickerUtils(BaseUiUtils):
    def __init__(self, page: Page, target_locator: Union[str, Locator]) -> None:
        super().__init__(page, target_locator)

    def expect_has_button(self):
        expect(self.page.locator("button")).to_be_visible()

    def click_button(self):
        self.page.locator("button").click()

    def click_color_panel(self):
        self.page.locator(".q-color-picker__spectrum-black").click()


class RadioUtils(BaseUiUtils):
    def __init__(self, page: Page, target_locator: Union[str, Locator]) -> None:
        super().__init__(page, target_locator)

    def is_checked_by_label(self, label: str):
        return self.target_locator.get_by_label(label).is_checked()

    def check_by_label(self, label: str):
        # self.target_locator.click(f"text={label}")

        self.target_locator.get_by_label(label).click()
        return

    def get_all_labels(self):
        return self.target_locator.locator(".q-radio__label").all_inner_texts()


class EChartsUtils(BaseUiUtils):
    def __init__(self, page: Page, target_locator: Union[str, Locator]) -> None:
        super().__init__(page, target_locator)

    def assert_canvas_exists(self):
        expect(self.target_locator.locator("css=canvas")).to_be_visible(timeout=5000)

    def assert_echarts_attachment(self):
        attr = self.target_locator.get_attribute("_echarts_instance_", timeout=10000)
        assert attr is not None

    def get_options(self):
        opts = self.target_locator.evaluate(
            "node => echarts.getInstanceByDom(node).getOption()"
        )

        return opts

    def click_series(
        self,
        x_value,
        y_value,
        color=None,
        seriesIndex=0,
        x_position_offset=0.0,
        y_position_offset=0.0,
    ):
        x, y = EChartsUtils.cal_series_pos(
            self.target_locator,
            x_value,
            y_value,
            color,
            seriesIndex,
        )

        self.page.mouse.click(
            x + x_position_offset,
            y + y_position_offset,
        )

    def mouse_hover_series(
        self,
        x_value,
        y_value,
        color=None,
        seriesIndex=0,
        x_position_offset=0.0,
        y_position_offset=0.0,
    ):
        x, y = EChartsUtils.cal_series_pos(
            self.target_locator,
            x_value,
            y_value,
            color,
            seriesIndex,
        )

        self.page.mouse.move(
            x + x_position_offset,
            y + y_position_offset,
        )

    @staticmethod
    def cal_series_pos(
        chartIns_box: Locator,
        x_value,
        y_value,
        color=None,
        seriesIndex=0,
    ):
        finder = ""
        if color is None:
            finder = f"{{ seriesIndex: {seriesIndex} }}"
        else:
            finder = f"{{ seriesName: {tran_str(color)} }}"

        pos_x, pos_y = chartIns_box.evaluate(
            f"node => echarts.getInstanceByDom(node).convertToPixel({finder}, [{tran_str(x_value)}, {tran_str(y_value)}])"
        )

        box = chartIns_box.bounding_box()
        assert box
        return (
            box["x"] + pos_x,
            box["y"] + pos_y,
        )


class TableUtils(BaseUiUtils):
    def __init__(self, page: Page, target_locator: Union[str, Locator]) -> None:
        super().__init__(page, target_locator)

    def expect_cell_to_be_visible(self, cell_values: List):
        for cell_value in cell_values:
            expect(
                self.target_locator.get_by_role(
                    "cell",
                    name=cell_value,
                    exact=True,
                )
            ).to_be_visible()

    def expect_cell_not_to_be_visible(self, cell_values: List):
        for cell_value in cell_values:
            expect(
                self.target_locator.get_by_role(
                    "cell",
                    name=cell_value,
                    exact=True,
                )
            ).not_to_be_visible()

    def click_checkbox(self, row_values: List):
        name = " ".join((str(d) for d in row_values))
        self.target_locator.get_by_role("row", name=name).get_by_role(
            "checkbox"
        ).click()

    def get_cell_style(self, cell_value: str):
        return self.target_locator.get_by_role(
            "cell", name=cell_value, exact=True
        ).get_attribute("style")

    def is_sortable(self, column_name: str):
        # sortable
        return self.target_locator.locator("thead th", has_text=column_name).evaluate(
            "node => node.classList.contains('sortable')"
        )


class MermaidUtils(BaseUiUtils):
    def __init__(self, page: Page, target_locator: Union[str, Locator]) -> None:
        super().__init__(page, target_locator)

    def click_node(self, nodeId: str):
        self.target_locator.get_by_text(nodeId, exact=True).click()

    def assert_svg_exists(self):
        expect(self.target_locator.locator("css=svg")).to_be_visible(timeout=5000)


class AggridUtils(BaseUiUtils):
    def __init__(self, page: Page, target_locator: Union[str, Locator]) -> None:
        super().__init__(page, target_locator)

    def expect_cell_to_be_visible(self, cell_values: List):
        for cell_value in cell_values:
            expect(
                self.target_locator.get_by_role(
                    "gridcell",
                    name=cell_value,
                    exact=True,
                )
            ).to_be_visible()

    def expect_selection_cell_to_be_visible(self, cell_values: List):
        for cell_value in cell_values:
            expect(
                self.target_locator.get_by_role("gridcell")
                .locator("div")
                .filter(has_text="a")
            ).to_be_visible()

    def expect_cell_not_to_be_visible(self, cell_values: List):
        for cell_value in cell_values:
            expect(
                self.target_locator.get_by_role(
                    "gridcell",
                    name=cell_value,
                    exact=True,
                )
            ).not_to_be_visible()

    def get_rows(
        self,
    ):
        return self.target_locator.locator(".ag-body-viewport").get_by_role("row").all()

    def get_data(self):
        return [
            row.get_by_role("gridcell").all_inner_texts() for row in self.get_rows()
        ]

    def get_cells(self):
        rows = self.get_rows()
        return [r.get_by_role("gridcell").all() for r in rows]


class ButtonUtils(BaseUiUtils):
    def __init__(self, page: Page, target_locator: Union[str, Locator]) -> None:
        super().__init__(page, target_locator)

    def click(self):
        self.target_locator.wait_for(state="attached")
        self.target_locator.click()

    def expect_enabled(self):
        expect(self.target_locator).to_be_enabled()


class LabelUtils(BaseUiUtils):
    def __init__(self, page: Page, target_locator: Union[str, Locator]) -> None:
        super().__init__(page, target_locator)

    def get_text(self):
        return self.target_locator.inner_text()

    def expect_contain_text(self, expected):
        return expect(self.target_locator).to_contain_text(expected)


class InputUtils(BaseUiUtils):
    def __init__(self, page: Page, target_locator: Union[str, Locator]) -> None:
        super().__init__(page, target_locator)

        # self.target_box = target_box or self.page.locator("css=label.q-input").filter(
        #     has=self.page.get_by_test_id(test_id)
        # )

    def expect_to_have_text(self, text: str):
        return expect(self.target_locator).to_have_value(text)

    def click(self):
        self.target_locator.click(position={"x": 5, "y": 5})

    def dbclick(self):
        self.target_locator.dblclick(position={"x": 5, "y": 5})

    def click_cancel_icon(self):
        self.target_locator.get_by_role("button").click()
        return self

    def keyboard_down(self, key: str):
        self.page.keyboard.down(key)
        return self

    def get_input_value(self):
        return self.target_locator.input_value()

    def input_text(self, text: str):
        self.target_locator.type(text)
        return self

    def fill_text(self, text: str):
        self.target_locator.fill(text)
        return self

    def enter(self):
        self.target_locator.press("Enter")
        return self

    def input_and_enter(self, text: str):
        self.input_text(text)
        self.page.wait_for_timeout(500)
        self.enter()
        return self


class InputNumberUtils(InputUtils):
    def __init__(self, page: Page, target_locator: Union[str, Locator]) -> None:
        super().__init__(page, target_locator)


class TextareaUtils(InputUtils):
    # def __init__(self, screen_page: BrowserManager, test_id: str) -> None:
    #     page = screen_page._page
    #     target_box = page.locator("css=label.q-textarea").filter(
    #         has=page.get_by_test_id(test_id)
    #     )
    #     super().__init__(screen_page, test_id, target_box)

    def __init__(self, page: Page, target_locator: Union[str, Locator]) -> None:
        super().__init__(page, target_locator)


class SwitchUtils(BaseUiUtils):
    def __init__(self, page: Page, target_locator: Union[str, Locator]) -> None:
        super().__init__(page, target_locator)

    def click(self):
        self.target_locator.locator("div").first.click()


class ImageUtils(BaseUiUtils):
    # def __init__(self, screen_page: BrowserManager, test_id: str) -> None:
    #     super().__init__(screen_page, test_id)
    #     self.__img_target = self.target_locator.locator("img")

    def __init__(self, page: Page, target_locator: Union[str, Locator]) -> None:
        super().__init__(page, target_locator)
        self.__img_target = self.target_locator.locator("img")

    def get_image(self):
        return self.__img_target

    def get_src(
        self,
    ):
        res = self.get_image().get_attribute("src")
        assert res
        return res

    def expect_load_image(self):
        expect(self.get_image()).to_be_visible()


class CheckboxUtils(BaseUiUtils):
    def __init__(self, page: Page, target_locator: Union[str, Locator]) -> None:
        super().__init__(page, target_locator)

    def is_checked(self):
        return self.target_locator.is_checked()

    def click(self):
        return self.target_locator.click()
