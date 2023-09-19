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



## BI 模块

以最精简的 apis 创建可交互的数据可视化报表

![](./asset/bi_examples1.gif)

```python
from nicegui import ui
import pandas as pd
import numpy as np
from ex4nicegui import bi
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
    def _(e):
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

