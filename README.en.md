# ex4nicegui

<div align="center">

English| [简体中文](./README.md)

</div>

- [Install](#-install)
- [Usage](#-usage)
- [Features](#-features)
- [BI Module](#bi-module)

An extension library for [nicegui](https://github.com/zauberzeug/nicegui). It has built-in responsive components and fully implements data-responsive interface programming.

![todo-app](https://github.com/CrystalWindSnake/ex4nicegui-examples/blob/main/asset/todo-app.02.gif)

[more examples](https://github.com/CrystalWindSnake/ex4nicegui-examples)

## 📦 Install

```
pip install ex4nicegui -U
```

## examples
- [basic](./examples/basic/)
- [todo list mvc](./examples/todomvc/)


## 🦄 Usage
![](./asset/sync_input.gif)
```python
from nicegui import ui
from ex4nicegui import rxui, ref_computed, effect, to_ref

# Define responsive data
r_input = to_ref("")

# Pass in the responsive data according to the nicegui usage method.
rxui.input(value=r_input)
rxui.label(r_input)

ui.run()
```

---

![colors](https://github.com/CrystalWindSnake/ex4nicegui-examples/blob/main/asset/colors.01.gif)

```python
from nicegui import ui
from ex4nicegui import rxui, to_ref

ui.radio.default_props("inline")

# Define responsive data
colors = ["red", "green", "blue", "yellow", "purple", "white"]
color = to_ref("blue")
bg_color = to_ref("red")


## Within the function, accessing `ref` or other associated functions will automatically synchronize updates
def bg_text():
    return f"Current background color is {bg_color.value}"


# UI

with ui.row(align_items="center"):
    rxui.radio(colors, value=color)
    ## With lambda
    rxui.label(lambda: f"Font color is {color.value}").bind_style({"color": color})

with ui.row(align_items="center"):
    rxui.radio(colors, value=bg_color)
    ## With function
    rxui.label(bg_text).bind_style({"background-color": bg_color})
```


## ViewModel
In version v0.7.0, the `ViewModel` class has been incorporated to facilitate the management of reactive data sets. Below is an illustrative example utilizing a basic calculator interface:

1. Upon modification of the numerical input fields or selection of arithmetic symbols by the user, the resultant value is instantaneously reflected on the display panel.
2. Should the computed outcome fall below zero, its representation assumes a red hue; conversely, non-negative results are rendered in black.

```python
from ex4nicegui import rxui

class Calculator(rxui.ViewModel):
    num1 = rxui.var(0)
    sign = rxui.var("+")
    num2 = rxui.var(0)

    def result(self):
        # When any of the values of num1, sign, or num2 changes, the result is recalculated accordingly.
        return eval(f"{self.num1.value}{self.sign.value}{self.num2.value}")

# Each object possesses its own independent data.
calc = Calculator()

with ui.row(align_items="center"):
    rxui.number(value=calc.num1, label="Number 1")
    rxui.select(value=calc.sign, options=["+", "-", "*", "/"], label="Sign")
    rxui.number(value=calc.num2, label="Number 2")
    ui.label("=")
    rxui.label(calc.result).bind_color(
        lambda: "red" if calc.result() < 0 else "black"
    )

```

### cached_var

In the preceding example, due to the use of `calc.result` twice, every time any of the values `num1`, `sign`, or `num2` undergoes a change, `result` is executed twice

In reality, the second computation is redundant. We can circumvent this unnecessary calculation by applying the `rxui.cached_var` decorator, which ensures that the result is cached and only recalculated when necessary.

```python
class Calculator(rxui.ViewModel):
    ...

    @rxui.cached_var
    def result(self):
        return eval(f"{self.num1.value}{self.sign.value}{self.num2.value}")

...
```

---

### for list and dict data

When the data is mutable, such as lists or dictionaries, a factory function must be supplied to `rxui.var`.

```python
class Home(rxui.ViewModel):
    persons= rxui.var(lambda: [])

```

In the following example, each person is displayed using a card. The average age of all individuals is shown at the top. When an individual's age exceeds the average age, the card's border turns red.

Age modifications are made through the `number` component, triggering automatic updates across the display.

```python
from typing import List
from ex4nicegui import rxui, Ref
from itertools import count
from nicegui import ui

id_generator = count()

class Person(rxui.ViewModel):
    def __init__(self, name: str, age: int):
        super().__init__()
        self.name = rxui.var(name)
        self.age = rxui.var(age)
        self.id = next(id_generator)



class Home(rxui.ViewModel):
    persons: Ref[List[Person]] = rxui.var(lambda: [])

    def avg_age(self) -> float:
        if len(self.persons.value) == 0:
            return 0

        return sum(p.age.value for p in self.persons.value) / len(self.persons.value)

    def sample_data(self):
        self.persons.value = [
            Person("alice", 25),
            Person("bob", 30),
            Person("charlie", 31),
            Person("dave", 22),
            Person("eve", 26),
            Person("frank", 29),
        ]

home = Home()
home.sample_data()

rxui.label(lambda: f"avg age: {home.avg_age()}")


with ui.row():

    @rxui.vfor(home.persons, key="id")
    def _(store: rxui.VforStore[Person]):
        person = store.get_item()
        with rxui.card().classes("outline").bind_classes(
            {
                "outline-red-500": lambda: person.age.value > home.avg_age(),
            }
        ):
            rxui.input(value=person.name, placeholder="name")
            rxui.number(value=person.age, min=1, max=100, step=1, placeholder="age")

ui.run()
```

If you find the `rxui.vfor` code too complex, you can use the `effect_refreshable` decorator instead.

```python
from ex4nicegui import rxui, Ref, effect_refreshable
...

# Explicitly specifying to monitor changes in `home.persons` can prevent unintended refreshes.
@effect_refreshable.on(home.persons)
def _():
    
    for person in home.persons.value:
        ...
        rxui.number(value=person.age, min=1, max=100, step=1, placeholder="Age")
...
```

Note that whenever the `home.persons` list changes (such as when elements are added or removed), the function decorated with `effect_refreshable` will be re-executed. This means that all elements will be recreated.


For more complex applications, please refer to the [examples](./examples)

---

## 🚀 Features

### echarts components

```python
from nicegui import ui
from ex4nicegui import ref_computed, effect, to_ref
from ex4nicegui.reactive import rxui

r_input = to_ref("")


# ref_computed Creates a read-only reactive variable
# Functions can use any other reactive variables automatically when they are associated
@ref_computed
def cp_echarts_opts():
    return {
        "title": {"text": r_input.value}, #In the dictionary, use any reactive variable. Get the value by .value
        "xAxis": {
            "type": "category",
            "data": ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"],
        },
        "yAxis": {"type": "value"},
        "series": [
            {
                "data": [120, 200, 150, 80, 70, 110, 130],
                "type": "bar",
                "showBackground": True,
                "backgroundStyle": {"color": "rgba(180, 180, 180, 0.2)"},
            }
        ],
    }


input = rxui.input("Enter the content, and the chart title will be synchronized", value=r_input)

# Get the native nicegui component object through the element attribute of the responsive component object
input.element.classes("w-full")

rxui.echarts(cp_echarts_opts).classes('h-[20rem]')

ui.run()
```
![](./asset/asyc_echarts_title.gif)


### echarts mouse events

the `on` function parameters `event_name` and `query` to view the[echarts English Documentation](https://echarts.apache.org/handbook/en/concepts/event/)


The following example binds the mouse click event
```python
from nicegui import ui
from ex4nicegui.reactive import rxui

opts = {
    "xAxis": {"type": "value", "boundaryGap": [0, 0.01]},
    "yAxis": {
        "type": "category",
        "data": ["Brazil", "Indonesia", "USA", "India", "China", "World"],
    },
    "series": [
        {
            "name": "first",
            "type": "bar",
            "data": [18203, 23489, 29034, 104970, 131744, 630230],
        },
        {
            "name": "second",
            "type": "bar",
            "data": [19325, 23438, 31000, 121594, 134141, 681807],
        },
    ],
}

bar = rxui.echarts(opts)

def on_click(e: rxui.echarts.EChartsMouseEventArguments):
    ui.notify(f"on_click:{e.seriesName}:{e.name}:{e.value}")

bar.on("click", on_click)
```


The following example only triggers the mouseover event for a specified series.
```python
from nicegui import ui
from ex4nicegui.reactive import rxui

opts = {
    "xAxis": {"type": "value", "boundaryGap": [0, 0.01]},
    "yAxis": {
        "type": "category",
        "data": ["Brazil", "Indonesia", "USA", "India", "China", "World"],
    },
    "series": [
        {
            "name": "first",
            "type": "bar",
            "data": [18203, 23489, 29034, 104970, 131744, 630230],
        },
        {
            "name": "second",
            "type": "bar",
            "data": [19325, 23438, 31000, 121594, 134141, 681807],
        },
    ],
}

bar = rxui.echarts(opts)

def on_first_series_mouseover(e: rxui.echarts.EChartsMouseEventArguments):
    ui.notify(f"on_first_series_mouseover:{e.seriesName}:{e.name}:{e.value}")


bar.on("mouseover", on_first_series_mouseover, query={"seriesName": "first"})

ui.run()
```
---

## responsive

```python
from ex4nicegui import (
    to_ref,
    ref_computed,
    on,
    effect,
    effect_refreshable,
    batch,
    event_batch,
    deep_ref,
)
```
Commonly used `to_ref`,`deep_ref`,`effect`,`ref_computed`,`on`

### `to_ref`
Defines responsive objects, read and written by `.value`.
```python
a = to_ref(1)
b = to_ref("text")

a.value =2
b.value = 'new text'

print(a.value)
```

When the value is a complex object, responsiveness of nested objects is not maintained by default.

```python
a = to_ref([1,2])

@effect
def _().
    print(len(a.value))

# doesn't trigger the effect
a.value.append(10)

# the whole substitution will be triggered
a.value = [1,2,10]
```

Depth responsiveness is obtained when `is_deep` is set to `True`.

```python
a = to_ref([1,2],is_deep=True)

@effect
def _():
    print('len:',len(a.value))

# print 3
a.value.append(10)

```

> `deep_ref` is equivalent to `to_ref` if `is_deep` is set to `True`.
---

### `deep_ref`
Equivalent to `to_ref` when `is_deep` is set to `True`.

Especially useful when the data source is a list, dictionary or custom class. Objects obtained via `.value` are proxies

```python
data = [1,2,3]
data_ref = deep_ref(data)

assert data_ref.value is not data
```

You can get the raw object with `to_raw`.
```python
from ex4nicegui import to_raw, deep_ref

data = [1, 2, 3]
data_ref = deep_ref(data)

assert data_ref.value is not data
assert to_raw(data_ref.value) is data
```

---

### `effect`
Accepts a function and automatically monitors changes to the responsive objects used in the function to automatically execute the function.

```python
a = to_ref(1)
b = to_ref("text")


@effect
def auto_run_when_ref_value():
    print(f"a:{a.value}")


def change_value():
    a.value = 2
    b.value = "new text"


ui.button("change", on_click=change_value)
```

The first time the effect is executed, the function `auto_run_when_ref_value` will be executed once. After that, clicking on the button changes the value of `a` (via `a.value`) and the function `auto_run_when_ref_value` is executed again.

> Never spread a lot of data processing logic across multiple `on`s or `effects`s, which should be mostly interface manipulation logic rather than responsive data processing logic

---

### `ref_computed`
As with `effect`, `ref_computed` can also return results from functions. Typically used for secondary computation from `to_ref`.

```python
a = to_ref(1)
a_square = ref_computed(lambda: a.value * 2)


@effect
def effect1():
    print(f"a_square:{a_square.value}")


def change_value():
    a.value = 2


ui.button("change", on_click=change_value)
```

When the button is clicked, the value of `a.value` is modified, triggering a recalculation of `a_square`. As the value of `a_square` is read in `effect1`, it triggers `effect1` to execute the

> `ref_computed` is read-only `to_ref`

Starting from version `v0.7.0`, it is not recommended to use `ref_computed` for instance methods. You can use `rxui.ViewModel` and apply the `rxui.cached_var` decorator instead.

```python
class MyState(rxui.ViewModel):
    def __init__(self) -> None:
        self.r_text = to_ref("")

    @rxui.cached_var
    def post_text(self):
        return self.r_text.value + "post"

state = MyState()

rxui.input(value=state.r_text)
rxui.label(state.post_text)
```

---

### `async_computed`
Use `async_computed` when asynchronous functions are required for computed.

```python

# Simulate asynchronous functions that take a long time to execute
async def long_time_query(input: str):
    await asyncio.sleep(2)
    num = random.randint(20, 100)
    return f"query result[{input=}]:{num=}"


search = to_ref("")
evaluating = to_ref(False)

@async_computed(search, evaluating=evaluating, init="")
async def search_result():
    return await long_time_query(search.value)

rxui.lazy_input(value=search)

rxui.label(
    lambda: "Query in progress" if evaluating.value else "Enter content in input box above and return to search"
)
rxui.label(search_result)

```

- The first argument to `async_computed` must explicitly specify the responsive data to be monitored. Multiple responses can be specified using a list.
- Parameter `evaluating` is responsive data of type bool, which is `True` while the asynchronous function is executing, and `False` after the computation is finished.
- Parameter `init` specifies the initial result

---

### `on`
Similar to `effect`, but `on` needs to explicitly specify the responsive object to monitor.

```python

a1 = to_ref(1)
a2 = to_ref(10)
b = to_ref("text")


@on(a1)
def watch_a1_only():
    print(f"watch_a1_only ... a1:{a1.value},a2:{a2.value}")


@on([a1, b], onchanges=True)
def watch_a1_and_b():
    print(f"watch_a1_and_b ... a1:{a1.value},a2:{a2.value},b:{b.value}")


def change_a1():
    a1.value += 1
    ui.notify("change_a1")


ui.button("change a1", on_click=change_a1)


def change_a2():
    a2.value += 1
    ui.notify("change_a2")


ui.button("change a2", on_click=change_a2)


def change_b():
    b.value += "x"
    ui.notify("change_b")


ui.button("change b", on_click=change_b)

```

- If the parameter `onchanges` is True (the default value is False), the specified function will not be executed at binding time.

> Never spread a lot of data processing logic across multiple `on`s or `effects`s, which should be mostly interface manipulation logic rather than responsive data processing logic

---

### `new_scope`

By default, all watch functions are automatically destroyed when the client connection is disconnected. For finer-grained control, the `new_scope` function can be utilized.

```python
from nicegui import ui
from ex4nicegui import rxui, to_ref, effect, new_scope

a = to_ref(0.0)

scope1 = new_scope()

@scope1.run
def _():
    @effect
    def _():
        print(f"scope 1:{a.value}")


rxui.number(value=a)
rxui.button("dispose scope 1", on_click=scope1.dispose)
```

---

## functionality

### vmodel
Create two-way bindings on form input elements or components.

Bidirectional bindings are supported by default for `ref` simple value types
```python
from ex4nicegui import rxui, to_ref, deep_ref

data = to_ref("init")

rxui.label(lambda: f"{data.value=}")
# two-way binding 
rxui.input(value=data)
```
- Simple value types are generally immutable values such as `str`, `int`, etc.

When using complex data structures, `deep_ref` is used to keep nested values responsive.
```python
data = deep_ref({"a": 1, "b": [1, 2, 3, 4]})

rxui.label(lambda: f"{data.value=!s}")

# No binding effect
rxui.input(value=data.value["a"])

# readonly binding
rxui.input(value=lambda: data.value["a"])

# two-way binding
rxui.input(value=rxui.vmodel(data,'a'))

# also two-way binding, but not recommended
rxui.input(value=rxui.vmodel(data.value["a"]))
```

- The first input box will be completely unresponsive because the code is equivalent to `rxui.input(value=1)`
- The second input box will get read responsiveness due to the use of a function.
- The third input box, wrapped in `rxui.vmodel`, can be bi-directionally bound.

> If you use `rxui.ViewModel`, you may find that you don't need to use `vmodel` at all.

see [todo list examples](./examples/todomvc/)

---

### vfor
Render list components based on list responsive data. Each component is updated on demand. Data items support dictionaries or objects of any type

Starting from version `v0.7.0`, it is recommended to use in conjunction with `rxui.ViewModel`. Unlike using the `effect_refreshable` decorator, `vfor` does not recreate all elements but updates existing ones.

Below is an example of card sorting, where cards are always sorted by age. When you modify the age data in a card, the cards adjust their order in real time. However, the cursor focus does not leave the input field.

```python
from typing import List
from nicegui import ui
from ex4nicegui import rxui, deep_ref as ref, Ref


class Person(rxui.ViewModel):
    def __init__(self, name: str, age: int) -> None:
        self.name = name
        self.age = ref(age)


class MyApp(rxui.ViewModel):
    persons: Ref[List[Person]] = rxui.var(lambda: [])
    order = rxui.var("asc")

    def sort_by_age(self):
        return sorted(
            self.persons.value,
            key=lambda p: p.age.value,
            reverse=self.order.value == "desc",
        )

    @staticmethod
    def create():
        persons = [
            Person(name="Alice", age=25),
            Person(name="Bob", age=30),
            Person(name="Charlie", age=20),
            Person(name="Dave", age=35),
            Person(name="Eve", age=28),
        ]
        app = MyApp()
        app.persons.value = persons
        return app


# UI
app = MyApp.create()

with rxui.tabs(app.order):
    rxui.tab("asc", "Ascending")
    rxui.tab("desc", "Descending")


@rxui.vfor(app.sort_by_age, key="name")
def each_person(s: rxui.VforStore[Person]):
    person = s.get_item()

    with ui.card(), ui.row(align_items="center"):
        rxui.label(person.name)
        rxui.number(value=person.age, step=1, min=0, max=100)
```

- The `rxui.vfor` decorator is applied to a custom function.
    - The first argument is the reactive list. Note that there is no need to call `app.sort_by_age`.
    - The second argument `key`: To track each node's identifier and thus reuse and reorder existing elements, you can provide a unique key for each block corresponding to an element. By default, the list element index is used. In the example, it is assumed that each person's name is unique.
- The custom function takes one parameter. You can obtain the current row's object via `store.get_item`. Since `Person` itself inherits from `rxui.ViewModel`, its properties can be directly bound to components.


---


### Bind class names

All component classes provide `bind_classes` for binding `class`, supporting three different data structures.

Bind dictionaries

```python
bg_color = to_ref(False)
has_error = to_ref(False)

rxui.label("test").bind_classes({"bg-blue": bg_color, "text-red": has_error})

rxui.switch("bg_color", value=bg_color)
rxui.switch("has_error", value=has_error)
```

Dictionary key  is the class name, and a dictionary value of  a responsive variable with value `bool`. When the responsive value is `True`, the class name is applied to the component `class`.

---

Bind a responsive variable whose return value is a dictionary.

```python
bg_color = to_ref(False)
has_error = to_ref(False)

class_obj = ref_computed(
    lambda: {"bg-blue": bg_color.value, "text-red": has_error.value}
)

rxui.switch("bg_color", value=bg_color)
rxui.switch("has_error", value=has_error)
rxui.label("bind to ref_computed").bind_classes(class_obj)

# or direct function passing
rxui.label("bind to ref_computed").bind_classes(
    lambda: {"bg-blue": bg_color.value, "text-red": has_error.value}
)
```

---

Bind to list

```python
bg_color = to_ref("red")
bg_color_class = ref_computed(lambda: f"bg-{bg_color.value}")

text_color = to_ref("green")
text_color_class = ref_computed(lambda: f"text-{text_color.value}")

rxui.select(["red", "green", "yellow"], label="bg color", value=bg_color)
rxui.select(["red", "green", "yellow"], label="text color", value=text_color)

rxui.label("binding to arrays").bind_classes([bg_color_class, text_color_class])
rxui.label("binding to single string").bind_classes(bg_color_class)
```

- Each element in the list is a responsive variable that returns the class name

---

### bind-style

```python
from nicegui import ui
from ex4nicegui.reactive import rxui
from ex4nicegui.utils.signals import to_ref


bg_color = to_ref("blue")
text_color = to_ref("red")

rxui.label("test").bind_style(
    {
        "background-color": bg_color,
        "color": text_color,
    }
)

rxui.select(["blue", "green", "yellow"], label="bg color", value=bg_color)
rxui.select(["red", "green", "yellow"], label="text color", value=text_color)
```

`bind_style` passed into dictionary, `key` is style name, `value` is style value, responsive string

---

### bind_prop
Binds a property.

```python
label = to_ref("hello")

rxui.button("").bind_prop("label", label)
# Functions are also permissible
rxui.button("").bind_prop(
    "label", lambda: f"{label.value} world"
)

rxui.input(value=label)
```

---

### rxui.echarts
Charting with echarts

---

#### rxui.echarts.from_javascript
Create echart from javascript code

```python
from pathlib import Path

rxui.echarts.from_javascript(Path("code.js"))
# or
rxui.echarts.from_javascript(
    """
(myChart) => {

    option = {
        xAxis: {
            type: 'category',
            data: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
        },
        yAxis: {
            type: 'value'
        },
        series: [
            {
                data: [120, 200, 150, 80, 70, 110, 130],
                type: 'bar'
            }
        ]
    };

    myChart.setOption(option);
}
"""
)
```

- The first parameter of the function is the echart instance object. You need to configure the chart in the function with `setOption`.

The function also has a second parameter, which is the global echarts object, allowing you to register maps via echarts.registerMap.


```python
rxui.echarts.from_javascript(
"""
(chart,echarts) =>{

    fetch('https://geo.datav.aliyun.com/areas_v3/bound/100000_full.json')
    .then(response => response.json())
    .then(data => {
            echarts.registerMap('test_map', data);

            chart.setOption({
                geo: {
                    map: 'test_map',
                    roam: true,
                },
                tooltip: {},
                legend: {},
                series: [],
            });
    });
}
"""
)
```


---

#### rxui.echarts.register_map
Register a map.

```python
rxui.echarts.register_map(
    "china", "https://geo.datav.aliyun.com/areas_v3/bound/100000_full.json"
)

rxui.echarts(
    {
        "geo": {
            "map": "china",
            "roam": True,
        },
        "tooltip": {},
        "legend": {},
        "series": [], 
    }
)
```

- The parameter `map_name` is a customized map name. Note that `map` must correspond to a registered name in the chart configuration.
- The parameter `src` is a valid network link to the map data.


If it's SVG data, you need to set the parameter `type="svg"`
```python
rxui.echarts.register_map("svg-rect", "/test/svg", type="svg")
```



You can also provide the path to the local json file for the map data.
```python
from pathlib import Path

rxui.echarts.register_map(
    "china", Path("map-data.json")
)
```

---

### gsap

js animation library. [gsap documentation](https://gsap.com/docs/v3/)

```python
from nicegui import ui
from ex4nicegui import gsap
```

#### gsap.from_

Set the start property, the animation will transition from the set property to the original position

```python

ui.label("test from").classes("target")
gsap.from_(".target", {"x": 50,'duration':1})

```

After the screen is loaded, the starting position of the text is shifted to the right by 50px, and then moved to the original position within 1 second.

- Arguments `targets` are css selectors.
- Arguments `vars` are attribute values

---

#### gsap.to

Set the end property, the animation will transition from the original property to the set property.

```python

ui.label("test to").classes("target")
gsap.to(".target", {"x": 50,'duration':1})

```

After loading the screen, the text will be moved back 50px from the original position within 1 second.

- Arguments `targets` are css selectors.
- Arguments `vars` are attribute values

---

#### gsap.run_script

Setting up animations by writing js

```python

gsap.run_script(
            r"""function setGsap(gsap) {
    gsap.to('.target',{"duration": 0.3,y:60})
}
""")
```

- The parameter `script` can be text or a file with a js extension `Path`.
- The name of the defined js function doesn't matter, the first argument is a gsap object.

---

### tab_panels

Compared to `nicegui.ui.tab_panels`, `rxui.tab_panels` lacks a `tabs` parameter. Under the reactive data mechanism, the linkage between `tabs` and `tab_panels` can be achieved solely through the `value` parameter.

```python
from nicegui import ui
from ex4nicegui import rxui, to_ref

names = ["Tab 1", "Tab 2", "Tab 3"]
current_tab = to_ref(names[0])

with rxui.tabs(current_tab):
    for name in names:
        rxui.tab(name)

with rxui.tab_panels(current_tab):
    for name in names:
        with rxui.tab_panel(name):
            ui.label(f"Content of {name}")
```

This is because, in a reactive context, component interactions are facilitated by an intermediary data layer (`to_ref`). Consequently, `tab_panels` can be synchronized with other components (ensuring the use of the same `ref` object).

```python
names = ["Tab 1", "Tab 2", "Tab 3"]
current_tab = to_ref(names[0])

with rxui.tab_panels(current_tab):
    for name in names:
        with rxui.tab_panel(name):
            ui.label(f"Content of {name}")

# The tabs definition does not have to precede the panels
with rxui.tabs(current_tab):
    for name in names:
        rxui.tab(name)

rxui.select(names, value=current_tab)
rxui.radio(names, value=current_tab).props("inline")

rxui.label(lambda: f"Current tab is: {current_tab.value}")
```

---

### lazy_tab_panels

In lazy loading mode, only the currently active tab is rendered.
```python
from ex4nicegui import to_ref, rxui, on, deep_ref

current_tab = to_ref("t1")

with rxui.tabs(current_tab):
    ui.tab("t1")
    ui.tab("t2")

with rxui.lazy_tab_panels(current_tab) as panels:

    @panels.add_tab_panel("t1")
    def _():
        ui.notify("Hello from t1")

    @panels.add_tab_panel("t2")
    def _():
        ui.notify("Hello from t2")

```

Upon page load, "Hello from t1" is displayed immediately. When switching to the "t2" tab, "Hello from t2" is then shown.

---
### scoped_style
The `scoped_style` method allows you to create styles that are scoped within the component.

```python
# All child elements will have a red outline, excluding the component itself
with rxui.row().scoped_style("*", "outline: 1px solid red;") as row:
    ui.label("Hello")
    ui.label("World")


# All child elements will have a red outline, including the component itself
with rxui.row().scoped_style(":self *", "outline: 1px solid red;") as row:
    ui.label("Hello")
    ui.label("World")

# When hovering over the row component, all child elements will have a red outline, excluding the component itself
with rxui.row().scoped_style(":hover *", "outline: 1px solid red;") as row:
    ui.label("Hello")
    ui.label("World")

# When hovering over the row component, all child elements will have a red outline, including the component itself
with rxui.row().scoped_style(":self:hover *", "outline: 1px solid red;") as row:
    ui.label("Hello")
    ui.label("World")
```

---

## BI Module

Create an interactive data visualization report using the minimal API.

![](./asset/bi_examples1.gif)

```python
from nicegui import ui
import pandas as pd
import numpy as np
from ex4nicegui import bi
from ex4nicegui.reactive import rxui
from ex4nicegui import effect, effect_refreshable
from pyecharts.charts import Bar


# data ready
def gen_data():
    np.random.seed(265)
    field1 = ["a1", "a2", "a3", "a4"]
    field2 = [f"name{i}" for i in range(1, 11)]
    df = (
        pd.MultiIndex.from_product([field1, field2], names=["cat", "name"])
        .to_frame()
        .reset_index(drop=True)
    )
    df[["idc1", "idc2"]] = np.random.randint(50, 1000, size=(len(df), 2))
    return df


df = gen_data()

# Create a data source.
ds = bi.data_source(df)

# ui
ui.query(".nicegui-content").classes("items-stretch no-wrap")

with ui.row().classes("justify-evenly"):
    # Create components based on the data source `ds`.
    ds.ui_select("cat").classes("min-w-[10rem]")
    ds.ui_select("name").classes("min-w-[10rem]")


with ui.grid(columns=2):
    # Configure the chart using a dictionary.
    @ds.ui_echarts
    def bar1(data: pd.DataFrame):
        data = data.groupby("name").agg({"idc1": "sum", "idc2": "sum"}).reset_index()

        return {
            "xAxis": {"type": "value"},
            "yAxis": {
                "type": "category",
                "data": data["name"].tolist(),
                "inverse": True,
            },
            "legend": {"textStyle": {"color": "gray"}},
            "series": [
                {"type": "bar", "name": "idc1", "data": data["idc1"].tolist()},
                {"type": "bar", "name": "idc2", "data": data["idc2"].tolist()},
            ],
        }

    bar1.classes("h-[20rem]")

    # Configure the chart using pyecharts.
    @ds.ui_echarts
    def bar2(data: pd.DataFrame):
        data = data.groupby("name").agg({"idc1": "sum", "idc2": "sum"}).reset_index()

        return (
            Bar()
            .add_xaxis(data["name"].tolist())
            .add_yaxis("idc1", data["idc1"].tolist())
            .add_yaxis("idc2", data["idc2"].tolist())
        )

    bar2.classes("h-[20rem]")

    # Bind the click event to achieve navigation.
    @bar2.on_chart_click
    def _(e: rxui.echarts.EChartsMouseEventArguments):
        ui.open(f"/details/{e.name}", new_tab=True)


# with response mechanisms, you can freely combine native nicegui components.
label_a1_total = ui.label("")


# this function will be triggered when ds changed.
@effect
def _():
    # prop `filtered_data` is the filtered DataFrame.
    df = ds.filtered_data
    total = df[df["cat"] == "a1"]["idc1"].sum()
    label_a1_total.text = f"idc1 total(cat==a1):{total}"


# you can also use `effect_refreshable`, but you need to note that the components in the function are rebuilt each time.
@effect_refreshable
def _():
    df = ds.filtered_data
    total = df[df["cat"] == "a2"]["idc1"].sum()
    ui.label(f"idc1 total(cat==a2):{total}")


# the page to be navigated when clicking on the chart series.
@ui.page("/details/{name}")
def details_page(name: str):
    ui.label("This table data will not change")
    ui.aggrid.from_pandas(ds.data.query(f'name=="{name}"'))

    ui.label("This table will change when the homepage data changes. ")

    @bi.data_source
    def new_ds():
        return ds.filtered_data[["name", "idc1", "idc2"]]

    new_ds.ui_aggrid()


ui.run()
```

### Details

#### `bi.data_source`
The data source is the core concept of the BI module, and all data linkage is based on this. In the current version (0.4.3), there are two ways to create a data source.

Receive `pandas`'s `DataFrame`:
```python
from nicegui import ui
from ex4nicegui import bi
import pandas as pd

df = pd.DataFrame(
    {
        "name": list("aabcdf"),
        "cls": ["c1", "c2", "c1", "c1", "c3", None],
        "value": range(6),
    }
)

ds =  bi.data_source(df)
```

Sometimes, we want to create a new data source based on another data source, in which case we can use a decorator to create a linked data source:
```python
df = pd.DataFrame(
    {
        "name": list("aabcdf"),
        "cls": ["c1", "c2", "c1", "c1", "c3", None],
        "value": range(6),
    }
)

ds =  bi.data_source(df)

@bi.data_source
def new_ds():
    # df is pd.DataFrame 
    df = ds.filtered_data
    df=df.copy()
    df['value'] = df['value'] * 100
    return df

ds.ui_select('name')
new_ds.ui_aggrid()
```

Note that since `new_ds` uses `ds.filtered_data`, changes to `ds` will trigger the linkage change of `new_ds`, causing the table component created by `new_ds` to change.

---

Remove all filter states through the `ds.remove_filters` method:
```python
ds = bi.data_source(df)

def on_remove_filters():
    ds.remove_filters()

ui.button("remove all filters", on_click=on_remove_filters)

ds.ui_select("name")
ds.ui_aggrid()
```
---

Reset the data source through the `ds.reload` method:
```python

df = pd.DataFrame(
    {
        "name": list("aabcdf"),
        "cls": ["c1", "c2", "c1", "c1", "c3", None],
        "value": range(6),
    }
)

new_df = pd.DataFrame(
    {
        "name": list("xxyyds"),
        "cls": ["cla1", "cla2", "cla3", "cla3", "cla3", None],
        "value": range(100, 106),
    }
)

ds = bi.data_source(df)

def on_remove_filters():
    ds.reload(new_df)

ui.button("reload data", on_click=on_remove_filters)

ds.ui_select("name")
ds.ui_aggrid()
```

---
#### ui_select

Dropdown Select Box

```python
from nicegui import ui
from ex4nicegui import bi
import pandas as pd

df = pd.DataFrame(
    {
        "name": list("aabcdf"),
        "cls": ["c1", "c2", "c1", "c1", "c3", None],
        "value": range(6),
    }
)

ds = bi.data_source(df)

ds.ui_select("name")
```

The first parameter column specifies the column name of the data source.

---
Set the order of options using the parameter `sort_options`:
```python
ds.ui_select("name", sort_options={"value": "desc", "name": "asc"})
```

---
Set whether to exclude null values using the parameter `exclude_null_value`:
```python
df = pd.DataFrame(
    {
        "cls": ["c1", "c2", "c1", "c1", "c3", None],
    }
)

ds = bi.data_source(df)
ds.ui_select("cls", exclude_null_value=True)
```

---
You can set the parameters of the native nicegui select component through keyword arguments.

Set default values through the value attribute:
```python
ds.ui_select("cls",value=['c1','c2'])
ds.ui_select("cls",multiple=False,value='c1')
```
For multiple selections (the parameter `multiple` is defaulted to True), `value` needs to be specified as a list. For single selections, `value` should be set to non-list.

---


#### ui_table

Table

```python
from nicegui import ui
from ex4nicegui import bi
import pandas as pd

data = pd.DataFrame({"name": ["f", "a", "c", "b"], "age": [1, 2, 3, 1]})
ds = bi.data_source(data)

ds.ui_table(
    columns=[
        {"label": "new colA", "field": "colA", "sortable": True},
    ]
)

```

- The parameter `columns` are consistent with nicegui `ui.table`. The key value `field` corresponds to the column name of the data source, and if it does not exist, this configuration will not take effect
- The `rows` parameter will not take effect. Because the data source of the table is always controlled by the data source.

---

#### ui_aggrid


```python
from nicegui import ui
from ex4nicegui import bi
import pandas as pd

data = pd.DataFrame(
    {
        "colA": list("abcde"),
        "colB": [f"n{idx}" for idx in range(5)],
        "colC": list(range(5)),
    }
)
df = pd.DataFrame(data)

source = bi.data_source(df)

source.ui_aggrid(
    options={
        "columnDefs": [
            {"headerName": "xx", "field": "no exists"},
            {"headerName": "new colA", "field": "colA"},
            {
                "field": "colC",
                "cellClassRules": {
                    "bg-red-300": "x < 3",
                    "bg-green-300": "x >= 3",
                },
            },
        ],
        "rowData": [{"colX": [1, 2, 3, 4, 5]}],
    }
)
```

- The parameter `options` is consistent with nicegui `ui.aggrid`. The key value `field` in columnDefs corresponds to the column name of the data source, and if it does not exist, this configuration will not take effect.
- The `rowData` key value will not take effect. Because the data source of the table is always controlled by the data source.


