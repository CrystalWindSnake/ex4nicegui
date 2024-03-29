from ex4nicegui.reactive import rxui
from nicegui import ui
from ex4nicegui import to_ref
from .screen import ScreenPage


def test_const_data(page: ScreenPage, page_path: str):
    @ui.page(page_path)
    def _():
        page_size = 10
        data = list(range(105))
        pagination_ref = rxui.use_pagination(data, page_size)

        assert pagination_ref.current_source.value == list(range(page_size))

        for i in range(1, 10):
            pagination_ref.next()

            start = i * page_size
            end = start + page_size
            assert pagination_ref.current_source.value == list(range(start, end))

        pagination_ref.next()
        assert pagination_ref.current_source.value == list(range(100, 105))


def test_set_current_page(page: ScreenPage, page_path: str):
    @ui.page(page_path)
    def _():
        page_size = 10
        data = list(range(105))

        r_cur_page = to_ref(2)
        pagination_ref = rxui.use_pagination(data, page_size, r_cur_page)

        assert pagination_ref.current_source.value == list(range(10, 20))

        r_cur_page.value = 1
        assert pagination_ref.current_source.value == list(range(0, 10))

        r_cur_page.value = 10
        assert pagination_ref.current_source.value == list(range(90, 100))

        r_cur_page.value = 11
        assert pagination_ref.current_source.value == list(range(100, 105))


def test_set_current_page_over_max_size(page: ScreenPage, page_path: str):
    @ui.page(page_path)
    def _():
        page_size = 10
        data = list(range(105))

        r_cur_page = to_ref(12)
        pagination_ref = rxui.use_pagination(data, page_size, r_cur_page)

        assert pagination_ref.current_source.value == list(range(100, 105))

        r_cur_page.value = 0
        assert pagination_ref.current_source.value == list(range(0, 10))


def test_first_last_page(page: ScreenPage, page_path: str):
    @ui.page(page_path)
    def _():
        page_size = 10
        data = list(range(105))

        r_cur_page = to_ref(12)
        pagination_ref = rxui.use_pagination(data, page_size, r_cur_page)

        assert pagination_ref.is_last_page.value
        assert not pagination_ref.is_first_page.value

        r_cur_page.value = 0
        assert pagination_ref.is_first_page.value
        assert not pagination_ref.is_last_page.value
