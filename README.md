# ex4nicegui
[ENGLISH README](./README.en.md)

- [教程](#教程)
- [安装](#-安装)
- [使用](#-使用)
- [功能](#-功能)
- [BI 模块](#bi-模块)

对 [nicegui](https://github.com/zauberzeug/nicegui) 做的扩展库。内置响应式组件，完全实现数据响应式界面编程。


## 教程
[头条文章-秒杀官方实现，python界面库，去掉90%事件代码的nicegui](https://www.toutiao.com/item/7253786340574265860/)

[微信公众号-秒杀官方实现，python界面库，去掉90%事件代码的nicegui](https://mp.weixin.qq.com/s?__biz=MzUzNDk1MTc5Mw==&mid=2247486796&idx=1&sn=457ed6fb9d6a25145f7704d5197d670d&chksm=fa8daf52cdfa2644bede50ae7f2551162ecaedecafec231ee4ce8f28775a599f8669ecf06af1#rd)


## 📦 安装

```
pip install ex4nicegui -U
```

## 🦄 使用

```python
from nicegui import ui
from ex4nicegui import ref_computed, effect, to_ref
from ex4nicegui.reactive import rxui

# 定义响应式数据
r_input = to_ref("")

# 按照 nicegui 使用方式传入响应式数据即可
rxui.input(value=r_input)
rxui.label(r_input)

ui.run()
```
![](./asset/sync_input.gif)


### 提供 echarts 图表组件

```python
from nicegui import ui
from ex4nicegui import ref_computed, effect, to_ref
from ex4nicegui.reactive import rxui

r_input = to_ref("")

# ref_computed 创建只读响应式变量
# 函数中使用任意其他响应式变量，会自动关联
@ref_computed
def cp_echarts_opts():
    return {
        "title": {"text": r_input.value}, #字典中使用任意响应式变量，通过 .value 获取值
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

input = rxui.input("输入内容，图表标题会同步", value=r_input)
# 通过响应式组件对象的 element 属性，获取原生 nicegui 组件对象
input.element.classes("w-full")

rxui.echarts(cp_echarts_opts)

ui.run()
```
![](./asset/asyc_echarts_title.gif)


### echarts 图表鼠标事件

`on` 函数参数 `event_name` 以及 `query` 使用,查看[echarts 事件中文文档](https://echarts.apache.org/handbook/zh/concepts/event/)


以下例子绑定鼠标单击事件
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


以下例子只针对指定系列触发鼠标划过事件
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


## 响应式

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
常用 `to_ref`,`deep_ref`,`effect`,`ref_computed`,`on`

---

### `to_ref`
定义响应式对象,通过 `.value` 读写
```python
a = to_ref(1)
b = to_ref("text")

a.value =2
b.value = 'new text'

print(a.value)
```

当值为复杂对象时，默认不会保持嵌套对象的响应性。
```python
a = to_ref([1,2])

@effect
def _():
    print('len:',len(a.value))

# 不会触发 effect
a.value.append(10)

# 整个替换则会触发
a.value = [1,2,10]
```

参数 `is_deep` 设置为 `True` 时，能得到深度响应能力

```python
a = to_ref([1,2],is_deep=True)

@effect
def _():
    print('len:',len(a.value))

# print 3
a.value.append(10)

```

>  `deep_ref` 等价于 `is_deep` 设置为 `True` 时的 `to_ref`

---

### `deep_ref`
等价于 `is_deep` 设置为 `True` 时的 `to_ref`。

当数据源为列表、字典或自定义类时，特别有用。通过 `.value` 获取的对象为代理对象
```python
data = [1,2,3]
data_ref = deep_ref(data)

assert data_ref.value is not data
```

通过 `to_raw` 可以获取原始对象
```python
from ex4nicegui import to_raw, deep_ref

data = [1, 2, 3]
data_ref = deep_ref(data)

assert data_ref.value is not data
assert to_raw(data_ref.value) is data
```


---

### `effect`
接受一个函数,自动监控函数中使用到的响应式对象变化,从而自动执行函数

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

首次执行 effect ,函数`auto_run_when_ref_value`将被执行一次.之后点击按钮,改变 `a` 的值(通过 `a.value`),函数`auto_run_when_ref_value`再次执行

> 切忌把大量数据处理逻辑分散在多个 `on` 或 `effect` 中，`on` 或 `effect` 中应该大部分为界面操作逻辑，而非响应式数据处理逻辑

---

### `ref_computed`
与 `effect` 具备一样的功能，`ref_computed` 还能从函数中返回结果。一般用于从 `to_ref` 中进行二次计算

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

点击按钮后，`a.value` 值被修改，从而触发 `a_square` 重新计算.由于 `effect1` 中读取了 `a_square` 的值，从而触发 `effect1` 执行

> `ref_computed` 是只读的 `to_ref`


如果你更喜欢通过类组织代码，`ref_computed` 同样支持作用到实例方法上

```python
class MyState:
    def __init__(self) -> None:
        self.r_text = to_ref("")

    @ref_computed
    def post_text(self):
        return self.r_text.value + "post"

state = MyState()

rxui.input(value=state.r_text)
rxui.label(state.post_text)
```


---

### `on`
类似 `effect` 的功能,但是 `on` 需要明确指定监控的响应式对象

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

- 参数 `onchanges` 为 True 时(默认值为 False),指定的函数不会在绑定时执行 


> 切忌把大量数据处理逻辑分散在多个 `on` 或 `effect` 中，`on` 或 `effect` 中应该大部分为界面操作逻辑，而非响应式数据处理逻辑

---


## 组件功能

### vfor
基于列表响应式数据，渲染列表组件。每项组件按需更新。数据项支持字典或任意类型对象

```python
from nicegui import ui
from ex4nicegui.reactive import rxui
from ex4nicegui import to_ref, ref_computed

# refs
items = to_ref(
    [
        {"id": 1, "message": "foo", "done": False},
        {"id": 2, "message": "bar", "done": True},
    ]
)

# ref_computeds
@ref_computed
def done_count_info():
    return f"done count:{sum(item['done'] for item in items.value)}"

# method
def check():
    for item in items.value:
        item["done"] = not item["done"]
    items.value = items.value


# ui
rxui.label(done_count_info)
ui.button("check", on_click=check)

@rxui.vfor(items, key="id")
def _(store: rxui.VforStore):
    # 函数中构建每一行数据的界面
    msg_ref = store.get("message")  # 通过 store.get 获取对应行的属性响应式对象

    # 输入框输入内容，可以看到单选框的标题同步变化
    with ui.card():
        rxui.input(value=msg_ref)
        rxui.checkbox(text=msg_ref, value=store.get("done"))

```

- `rxui.vfor` 装饰器到自定义函数
    - 第一个参数传入响应式列表。列表中每一项可以是字典或其他对象(`dataclasses` 等等)
    - 第二个参数 `key`: 为了可以跟踪每个节点的标识，从而重用和重新排序现有的元素，你可以为每个元素对应的块提供一个唯一的 key 。默认情况使用列表元素索引。
- 自定义函数带有一个参数。通过 `store.get` 可以获取当前行对应的属性，此为响应式对象

> vfor 渲染的项目，只有在新增数据时，才会创建

上述的例子中，你会发现，当点击 checkbox 时，完成数量的文本(`done_count_info`)并没有同步变化

因为 `vfor` 函数中对响应式数据修改，不会影响数据源列表。这是为了防止写出过于复杂的双向数据流响应逻辑而限制。

我们应该在函数中通过事件，对数据源列表做修改

```python
...

@rxui.vfor(items, key="id")
def _(store: rxui.VforStore):
    msg_ref = store.get("message")

    def on_check_change(e):
        items.value[store.row_index]["done"] = e.value
        items.value = items.value

    with ui.card():
        rxui.input(value=msg_ref)
        rxui.checkbox(text=msg_ref, value=store.get("done"),on_change=on_check_change)

```


---

### 绑定类名

所有的组件类提供 `bind_classes` 用于绑定 `class`，支持三种不同的数据结构。

绑定字典

```python
bg_color = to_ref(False)
has_error = to_ref(False)

rxui.label("test").bind_classes({"bg-blue": bg_color, "text-red": has_error})

rxui.switch("bg_color", value=bg_color)
rxui.switch("has_error", value=has_error)
```

字典键值为类名,对应值为 bool 的响应式变量。当响应式值为 `True`，类名应用到组件 class


---

绑定返回值为字典的响应式变量

```python
bg_color = to_ref(False)
has_error = to_ref(False)

class_obj = ref_computed(
    lambda: {"bg-blue": bg_color.value, "text-red": has_error.value}
)

rxui.switch("bg_color", value=bg_color)
rxui.switch("has_error", value=has_error)
rxui.label("bind to ref_computed").bind_classes(class_obj)
```

---

绑定为列表

```python
bg_color = to_ref("red")
bg_color_class = ref_computed(lambda: f"bg-{bg_color.value}")

text_color = to_ref("green")
text_color_class = ref_computed(lambda: f"text-{text_color.value}")

rxui.select(["red", "green", "yellow"], label="bg color", value=bg_color)
rxui.select(["red", "green", "yellow"], label="text color", value=text_color)

rxui.label("binding to arrays").bind_classes([bg_color_class, text_color_class])

```

列表中每个元素为返回类名的响应式变量

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

`bind_style` 传入字典，`key` 为样式名字，`value` 为样式值，响应式字符串


---

### rxui.echarts
使用 echarts 制作图表

---

#### rxui.echarts.from_javascript
从 javascript 代码创建 echart

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

- 函数第一个参数为 echart 实例对象.你需要在函数中通过 `setOption` 完成图表配置

---

#### rxui.echarts.register_map
注册地图.

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

- 参数 `map_name` 为自定义的地图名字。注意在图表配置中 `map` 必需对应注册的名字
- 参数 `src` 为有效的地图数据网络链接。

你也可以直接提供本地地图数据的json文件路径对象(Path)
```python
from pathlib import Path

rxui.echarts.register_map(
    "china", Path("map-data.json")
)
```

---

### gsap
js 动画库. [gsap文档](https://gsap.com/docs/v3/)

```python
from nicegui import ui
from ex4nicegui import gsap
```

#### gsap.from_

设置起始属性，动画将从设置的属性过渡到原始位置

```python

ui.label("test from").classes("target")
gsap.from_(".target", {"x": 50,'duration':1})

```

画面加载后，文本起始位置在往右偏移 50px 处，在 1秒 内移动到原始位置上

- 参数 `targets` 为 css 选择器
- 参数 `vars` 为属性值，具体参考 gsap 文档

---

#### gsap.to

设置结束属性，动画将从原始属性过渡到设置的属性

```python

ui.label("test to").classes("target")
gsap.to(".target", {"x": 50,'duration':1})

```

画面加载后，文本在 1秒 内，从原始位置往后移动 50px

- 参数 `targets` 为 css 选择器
- 参数 `vars` 为属性值，具体参考 gsap 文档

---
#### gsap.run_script

通过编写 js 设置动画

```python

gsap.run_script(
            r"""function setGsap(gsap) {
    gsap.to('.target',{"duration": 0.3,y:60})
}
""")
```

- 参数 `script` 可以为文本或 js 后缀的文件 `Path`
- 定义的 js 函数名字并不影响运行，第一个参数为 gsap 对象

---

## BI 模块

以最精简的 apis 创建可交互的数据可视化报表

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

# 创建数据源
ds = bi.data_source(df)

# ui
ui.query(".nicegui-content").classes("items-stretch no-wrap")

with ui.row().classes("justify-evenly"):
    # 基于数据源 `ds` 创建界面组件
    ds.ui_select("cat").classes("min-w-[10rem]")
    ds.ui_select("name").classes("min-w-[10rem]")


with ui.grid(columns=2):
    # 使用字典配置图表
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

    # 使用pyecharts配置图表
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

    # 绑定点击事件，即可实现跳转
    @bar2.on_chart_click
    def _(e: rxui.echarts.EChartsMouseEventArguments):
        ui.open(f"/details/{e.name}", new_tab=True)


# 利用响应式机制，你可以随意组合原生 nicegui 组件
label_a1_total = ui.label("")


# 当 ds 有变化，都会触发此函数
@effect
def _():
    # filtered_data 为过滤后的 DataFrame
    df = ds.filtered_data
    total = df[df["cat"] == "a1"]["idc1"].sum()
    label_a1_total.text = f"idc1 total(cat==a1):{total}"


# 你也可以使用 `effect_refreshable`,但需要注意函数中的组件每次都被重建
@effect_refreshable
def _():
    df = ds.filtered_data
    total = df[df["cat"] == "a2"]["idc1"].sum()
    ui.label(f"idc1 total(cat==a2):{total}")


# 当点击图表系列时，跳转的页面
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



### 细节




#### `bi.data_source`
数据源是 BI 模块的核心概念，所有数据的联动基于此展开。当前版本(0.4.3)中，有两种创建数据源的方式

接收 `pandas` 的 `DataFrame`:
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

---
有时候，我们希望基于另一个数据源创建新的数据源，此时可以使用装饰器创建联动数据源:
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

注意，由于 `new_ds` 中使用了 `ds.filtered_data` ，因此 `ds` 的变动会触发 `new_ds` 的联动变化，从而导致 `new_ds` 创建的表格组件产生变化

---
通过 `ds.remove_filters` 方法，移除所有筛选状态:
```python
ds = bi.data_source(df)

def on_remove_filters():
    ds.remove_filters()

ui.button("remove all filters", on_click=on_remove_filters)

ds.ui_select("name")
ds.ui_aggrid()
```
---

通过 `ds.reload` 方法，重设数据源:
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

第一个参数 column 指定数据源的列名

---
通过参数 `sort_options` 设置选项顺序:
```python
ds.ui_select("name", sort_options={"value": "desc", "name": "asc"})

```

---
参数 `exclude_null_value` 设置是否排除空值:
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

你可以通过关键字参数，设置原生 nicegui select 组件的参数.

通过 value 属性，设置默认值:
```python
ds.ui_select("cls",value=['c1','c2'])
ds.ui_select("cls",multiple=False,value='c1')

```

多选时(参数 `multiple` 默认为 True)，`value` 需要指定为 list

单选时，`value` 设置为非 list

---

#### ui_table

表格

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

- columns 与 nicegui `ui.table` 一致。其中 键值 `field` 对应数据源的列名，如果不存在，则该配置不会生效
- rows 参数不会生效。因为表格的数据源始终由 data source 控制

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

- 参数 options 与 nicegui `ui.aggrid` 一致。其中 `columnDefs` 中的键值 `field` 对应数据源的列名，如果不存在，则该配置不会生效
- `rowData` 键值不会生效。因为表格的数据源始终由 data source 控制


