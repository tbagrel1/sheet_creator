#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Setup tool for Sheet Creator X."""

from cx_Freeze import setup, Executable
import sys
import os

path = sys.path

base = None
if sys.platform == "win32":
    base = "Win32GUI"

bin_path_includes = []
# if sys.platform == "linux":
#     bin_path_includes += ["/usr/lib"]

includes = []
include_files = [
    "resources",
    "output",
]
packages = ["ui", "atexit"]
excludes = ["tkinter"]

options = {
    "path": path,
    "includes": includes,
    "packages": packages,
    "excludes": excludes,
    "include_files": include_files,
    "zip_include_packages": "*",
    "zip_exclude_packages": [],
    "bin_path_includes": bin_path_includes,
}

if sys.platform == "win32":
    options["include_msvcr"] = True

setup(
    name="sheet_creator",
    version="2.1.0",
    description="Sheet Creator X",
    executables=[
        Executable("sheet_creator.py", base=base),
    ],
    options= {
        "build_exe": options
    },
)
