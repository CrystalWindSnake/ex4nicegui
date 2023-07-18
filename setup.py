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


with open("README.md", encoding="utf8") as readme_file:
    readme = readme_file.read()

requirements = ["signe>=0.1.8", "nicegui>=1.3.4", "typing_extensions"]

test_requirements = ["pytest>=3"]

setup(
    author="carson_jia",
    author_email="568166495@qq.com",
    python_requires=">=3.7",
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
    description="...",
    entry_points={},
    install_requires=requirements,
    license="MIT license",
    # long_description=readme,
    include_package_data=True,
    keywords=["nicegui", "ex4nicegui", "webui"],
    name="ex4nicegui",
    packages=find_packages(include=["ex4nicegui", "ex4nicegui.*"]),
    data_files=get_data_files("ex4nicegui/reactive"),
    test_suite="__tests",
    tests_require=test_requirements,
    url="",
    version=ex4nicegui.__version__,
    zip_safe=False,
)
