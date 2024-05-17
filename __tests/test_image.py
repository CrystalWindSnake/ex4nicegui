from ex4nicegui.reactive import rxui
from nicegui import ui
from ex4nicegui import to_ref
from .screen import BrowserManager
from .utils import ImageUtils, set_test_id
from pathlib import Path

image_file = Path(__file__).parent / "files/slide1.jpg"


def test_source(browser: BrowserManager, page_path: str):
    img_bs64 = (
        "data:image/png;base64,"
        "iVBORw0KGgoAAAANSUhEUgAAADAAAAAwCAYAAABXAvmHAAAABmJLR0QA/wD/AP+gvaeTAAAEHElEQVRo"
        "ge2ZXUxbZRjHf6enH3QtBQ7paIFlMO2AMXTGqZE40bCpiRdzF06Nsu3O6G68MH5MnYkk3vhx4cWCJppF"
        "lvgZ74wXbsZdLCYaQMeWUWM30EJZgVM+WtpS2uNFoQzTU3pKu2O0v8v38//Pe57ned8cKFOmTBk9EVR7"
        "vrxsRlJ6gR7AfdMUrWcC6EcWTnK4fSnbAKPqVEl5C3ipRMLypR54GUkBeCXbAEOOyUdKoahAjqp15DKg"
        "12eTDZdaRy4DN43p+1s55HTwVF0Vk/taNM3V3UCDxUStSWQ4HKPDXsFwOK5pvm4GTILADquZbslGPKUA"
        "sNdRwXg8wQ6rOe911NPo2UvKplXmYOcWM957Par9wrnL6xv2786qVbcT8EUTSOdH+Co4T//kLE0Xfgfg"
        "wcFRpPMjea+jm4GkohBaTuKxmhlaiNFoMZFS4Jf5KKHlZN7rqBeyEvPF7kYO11UBsKdyLUuGH2jjNV+Q"
        "t0en8lpHtxN41RfkyUt+APYPjfJNcJ7v5TB7f77KJxOhvNfRzcDVaPpqM51Ick6O4DQbuTC7yMBClMml"
        "5bzX0bUOdNgtXAzHAGi3WRiOaKsBoGMa1cy/LY0Wi7IBvfl/GhCAJ+qq+HbPdgL7Whi8+5YN59zjsOLr"
        "9ODr9PB6s7OQbbOiuRI7jAa+7tjGAcmeaQtukLdNgsBHbfWZW2atSdS6rSqaDAjAp7saOSDZSSoKpwOz"
        "nJmcw7uYO3+/uL2W2+wVm9GpiiYD3ZKNg85KAI57A3w4vnHJv9Vq5o1mJ9FUCqMgYBLUS08haIqBY+4a"
        "AK5E4lyJxDnV4ub0rgaOuasRswgTgL7WeqwGA73XpjIPl2Ki6QQ6q6wAbDUb+fHO5kwZP+qu5qDTwaGL"
        "f64bf8RdTbdkYzgc492xGU40FS94V9F0Ai5L2q9kEunzyxz3BhhYiALwmLOSh24IbKfZyHseFykFnh0J"
        "kFBKczPRZMBqSA//eCLE894Ap/wyDw+NsZhMAWTiA+B9Tx21JpG+cZmf5haLKHk9mgysCp1bTmXaZhJJ"
        "vIvpq3HTSpq83V7BM65qAHrc1chdrchdrdjE9HbPNUjIXa2bV49GA6tC22yWTJsoCLhXPq3ZRHKlbW1O"
        "pWigxihSYxQzMWMxCNQYi1MLNAXxZ9fnuKOygkckO0+7qjgrR3hhWy0uc3qZ72bCAPwWjmd9mPvv28kW"
        "0UDfuMyJP4JFkK/RwAd/zfD4Vgd3OaycaW9c1/dDKMLn1+eAtQf7P1kN41gqe38haPqE4imF7sFR3hmb"
        "ZiyWIKEo+KJL9F6b4tFfx1jeINMMLcQYWIjijyU2JfpG/tMvsokSSSkAYVytJ5eB/hIoKQxBUdWiHsSy"
        "cHLlz0gP6T8lepD+xTQjvKnT/mXKlCmzAX8Dl7JCqRHaepQAAAAASUVORK5CYII="
    )
    img_source = to_ref(image_file)

    @ui.page(page_path)
    def _():
        set_test_id(
            rxui.image(img_source).props("fit=contain").classes("w-[20rem] h-[20rem]"),
            "target",
        )

    page = browser.open(page_path)

    target = ImageUtils(page, "target")

    target.expect_find_by_class("q-img__image")
    target.expect_load_image()

    img_source.value = img_bs64  # type: ignore

    page.wait(1000)
    target.expect_load_image()

    src = target.get_src()
    assert src.startswith("data:image/png;base64,iVB")
