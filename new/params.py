#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Params for Sheet Creator X."""

from os import path
import sys

ENC = "utf8"

WORD_NB_WARNING_THRESHOLD = 25

DEFAULT_REF_WORD = "Cochon"
DEFAULT_CAPITAL_ENABLED = False
DEFAULT_SCRIPT_ENABLED = True
DEFAULT_CURSIVE_ENABLED = False
DEFAULT_LINES = 5
DEFAULT_REF_WORD_NUMBER = 1
DEFAULT_REF_WORD_PROB = 0.80
DEFAULT_VERY_CLOSE_PROB = 0.40
DEFAULT_CLOSE_PROB = 0.40
# NO DEFAULT_OTHER_PROB

DEFAULT_ADVANCED_SETTINGS_ENABLED = False
DEFAULT_VERY_CLOSE_STARTEND3_ENABLED = False
DEFAULT_VERY_CLOSE_STARTEND2_ENABLED = False
DEFAULT_VERY_CLOSE_FOLLOWING4_ENABLED = False
DEFAULT_VERY_CLOSE_FOLLOWING3_ENABLED = True
DEFAULT_VERY_CLOSE_INDEP3_ENABLED = False

DEFAULT_CLOSE_STARTEND2_ENABLED = False
DEFAULT_CLOSE_FOLLOWING3_ENABLED = False
DEFAULT_CLOSE_FOLLOWING2_ENABLED = True
DEFAULT_CLOSE_INDEP3_ENABLED = False
DEFAULT_CLOSE_INDEP2_ENABLED = False

OUTPUT_DIRECTORY = path.abspath("./output")
OUTPUT_TEX_FILE_FORMAT = "feuille_{}.tex"
OUTPUT_PDF_FILE_FORMAT = "feuille_{}.pdf"
OUTPUT_SUBDIR_FORMAT = "feuille_{}"
RESOURCE_DIRECTORY = path.abspath("./resources")
HELP_DIRECTORY = path.join(RESOURCE_DIRECTORY, "help")
HELP_FILE = "aide.pdf"
HELP_PATH = path.join(
    HELP_DIRECTORY, HELP_FILE)
WORD_LIST_DIRECTORY = path.join(RESOURCE_DIRECTORY, "word_lists")
DEFAULT_WORD_LIST_FILE = "liste_mots.txt"
DEFAULT_WORD_LIST_PATH = path.join(
    WORD_LIST_DIRECTORY, DEFAULT_WORD_LIST_FILE)
TEMPLATE_DIRECTORY = path.join(RESOURCE_DIRECTORY, "template")
TEMPLATE_MAIN_FILE = "template_main.tex"
TEMPLATE_MAIN_PATH = path.join(TEMPLATE_DIRECTORY, TEMPLATE_MAIN_FILE)
TEMPLATE_CAPITAL_FILE = "template_capital.tex_template"
TEMPLATE_CAPITAL_PATH = path.join(TEMPLATE_DIRECTORY, TEMPLATE_CAPITAL_FILE)
TEMPLATE_SCRIPT_FILE = "template_script.tex_template"
TEMPLATE_SCRIPT_PATH = path.join(TEMPLATE_DIRECTORY, TEMPLATE_SCRIPT_FILE)
TEMPLATE_CURSIVE_FILE = "template_cursive.tex_template"
TEMPLATE_CURSIVE_PATH = path.join(TEMPLATE_DIRECTORY, TEMPLATE_CURSIVE_FILE)
TEMPLATE_FIELDS = ["%%%REF_WORD%%%", "%%%CONTENT%%%"]

TEX_COMPILE_CMD = "latexmk"
TEX_COMPILE_ARGS = [
    "-pdf"
]

# Checks that the default word list is avaible
if not path.isfile(DEFAULT_WORD_LIST_PATH):
    print("Default word list is not avaible. The app will shutdown...")
    sys.exit(1)

# Checks that the template tex file is avaible
if not path.isfile(TEMPLATE_MAIN_PATH):
    print("Main template TeX file is not avaible. The app will shutdown...")
    sys.exit(2)

if not path.isfile(TEMPLATE_CAPITAL_PATH):
    print("Capital template TeX file is not avaible. The app will shutdown...")
    sys.exit(3)

if not path.isfile(TEMPLATE_SCRIPT_PATH):
    print("Script template TeX file is not avaible. The app will shutdown...")
    sys.exit(4)

if not path.isfile(TEMPLATE_CURSIVE_PATH):
    print("Cursive template TeX file is not avaible. The app will shutdown...")
    sys.exit(5)

# Only handles ASCII chars at the moment
ASCII_IDS = list(range(0, 127 + 1))
ALLOWED_ASCII_IDS = (
    [45] +
    list(range(65, 90 + 1)) +
    list(range(97, 122 + 1))
)

DEBUG_LEVEL = 2
FANCY_LEVELS = {
    0: "<font color='red'>[E]</font>",
    1: "<font color='orange'>[W]</font>",
    2: "<font color='green'>[I]</font>",
    3: "<font color='gray'>[L]</font>"
}
DEBUG_CONSOLE = True