#!/bin/bash

RAW_UI_DIRECTORY="../_ui"
PY_UI_DIRECTORY="../ui"

pyuic5 -x "$RAW_UI_DIRECTORY/sheet_creator_master.ui" -o "$PY_UI_DIRECTORY/sheet_creator_master_ui.py"
