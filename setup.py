#!/usr/bin/env python
"""The setup script."""

from pathlib import Path
from setuptools import setup, find_packages
import ex4nicegui


def get_data_files(base):
    base = Path(base)

    all_js_files = base.rglob("*.js")

    all_infos = ({"dir": js.parent.name, "js": str(js)} for js in all_js_files)

    all_infos = ((info["dir"], [info["js"]]) for info in all_infos)

    return list(all_infos)


readme = Path("README.en.md").read_text("utf8")


requirements = ["signe>=0.4.14", "nicegui>=1.4.0", "typing_extensions", "executing"]

test_requirements = ["pytest>=3", "playwright", "pandas", "executing"]

setup(
    author="carson_jia",
    author_email="568166495@qq.com",
    python_requires=">=3.8",
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Programming Language :: Python :: 3.8",
    ],
    description="Extension library based on nicegui, providing data responsive,BI functionality modules",
    entry_points={},
    install_requires=requirements,
    license="MIT license",
    long_description=readme,
    long_description_content_type="text/markdown",
    include_package_data=True,
    keywords=["nicegui", "ex4nicegui", "webui"],
    name="ex4nicegui",
    packages=find_packages(include=["ex4nicegui", "ex4nicegui.*"]),
    package_data={"": ["*.js"]},
    test_suite="__tests",
    tests_require=test_requirements,
    url="",
    version=ex4nicegui.__version__,
    zip_safe=False,
)
