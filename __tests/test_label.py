import pytest
from ex4nicegui.reactive import rxui
from ex4nicegui import to_ref
from .screen import Screen


def test_const_str(screen: Screen):
    rxui.label("test label")

    screen.open("/")
    screen.should_contain("test label")


def test_ref_str(screen: Screen):
    r_str = to_ref("test label")
    rxui.label(r_str)

    screen.open("/")
    screen.should_contain("test label")


def test_ref_str_change_value(screen: Screen):
    r_str = to_ref("old")
    rxui.label(r_str)

    screen.open("/")
    screen.should_contain("old")

    screen.wait()
    r_str.value = "new"

    screen.wait()
    screen.should_contain("new")


def test_bind_color(screen: Screen):
    r_color = to_ref("red")
    rxui.label("label").bind_color(r_color)

    screen.open("/")

    assert screen.get_ele("label").evaluate("node=> node.style.color=='red'")


def test_bind_color_changed(screen: Screen):
    r_color = to_ref("red")
    rxui.label("label").bind_color(r_color)

    screen.open("/")

    assert screen.get_ele("label").evaluate("node=> node.style.color=='red'")

    screen.wait()
    r_color.value = "green"
    screen.wait()
    assert screen.get_ele("label").evaluate("node=> node.style.color=='green'")
