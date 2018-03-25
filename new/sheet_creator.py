#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Module docstring."""

import sys

from PyQt5.QtCore import pyqtSignal, pyqtSlot
from PyQt5.QtWidgets import QWidget, QApplication
from ui.sheet_creator_master_ui import Ui_master
from os import path
import webbrowser

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

OUTPUT_DIRECTORY = "./output"
OUTPUT_TEX_FILE_FORMAT = "feuille_{}.tex"
OUTPUT_SUBDIR_FORMAT = "feuille_{}"
RESOURCE_DIRECTORY = "./resources"
HELP_DIRECTORY = path.join(RESOURCE_DIRECTORY, "help")
HELP_FILE = "./aide.pdf"
HELP_PATH = path.join(
    HELP_DIRECTORY, HELP_FILE)
WORD_LIST_DIRECTORY = path.join(RESOURCE_DIRECTORY, "word_lists")
DEFAULT_WORD_LIST_FILE = "liste_mots.txt"
DEFAULT_WORD_LIST_PATH = path.join(
    WORD_LIST_DIRECTORY, DEFAULT_WORD_LIST_FILE)
TEMPLATE_DIRECTORY = path.join(RESOURCE_DIRECTORY, "template")
TEMPLATE_FILE = "template.tex"
TEMPLATE_PATH = path.join(TEMPLATE_DIRECTORY, TEMPLATE_FILE)
TEMPLATE_FIELDS = ["%%%REF_WORD%%%", "%%%CONTENT%%%"]

# Checks that the default word list is avaible
if not path.isfile(DEFAULT_WORD_LIST_PATH):
    print("Default word list is not avaible. The app will shutdown...")
    sys.exit(1)
DEFAULT_WORD_LIST_OK_ENABLED = True

# Checks that the template tex file is avaible
if not path.isfile(TEMPLATE_FILE):
    print("Template TeX file is not avaible. The app will shutdown...")
    sys.exit(2)
with open(TEMPLATE_PATH, "r", encoding=ENC) as template_file:
    for field in TEMPLATE_FIELDS:
        if not field in template_file.read():
            print("Template TeX file is not valid. The app will shutdown...")
            sys.exit(3)

# Only handles ASCII chars at the moment
ASCII_IDS = list(range(0, 127 + 1))
ALLOWED_ASCII_IDS = (
    [45] +
    list(range(65, 90 + 1)) +
    list(range(97, 122 + 1))
)

DEBUG_LEVEL = 2
FANCY_LEVELS = {
    0: "E",
    1: "W",
    2: "I",
    3: "L"
}
DEBUG_CONSOLE = True

def normalize(string):
    """Returns a normalized version of the string."""
    return string.strip()

def normalize_word(word):
    """Returns a normalized version of the word."""
    return word.strip().lower()

def normalize_line(line):
    """Returns a normalized version of the line."""
    return line.strip()

def is_correct_word(word):
    """Checks wether the specified word is a valid "word", that's to say with
    no space, no special symbol..."""
    if len(word) <= 0:
        return False
    for c in word:
        try:
            if ord(c) in ASCII_IDS and ord(c) not in ALLOWED_ASCII_IDS:
                return False
        except:
            pass
    return True

# TODO: Faire le systeme qui empeche de pas cocher de cases !

class SheetCreatorUiMaster(Ui_master, QWidget):
    """Main instance of the GUI."""

    def __init__(self):
        """Init method."""
        # Init parent class
        super().__init__()
        # Setup widgets
        self.setupUi(self)

        self.put_default_settings()

    @pyqtSlot(int)
    def on_checkbox_vc_startend3_stateChanged(self, _):
        """When the very close startend3 criteria is enabled/disabled."""
        self.update_very_close_status()
    @pyqtSlot(int)
    def on_checkbox_vc_startend2_stateChanged(self, _):
        """When the very close startend2 criteria is enabled/disabled."""
        self.update_very_close_status()
    @pyqtSlot(int)
    def on_checkbox_vc_following4_stateChanged(self, _):
        """When the very close following4 criteria is enabled/disabled."""
        self.update_very_close_status()
    @pyqtSlot(int)
    def on_checkbox_vc_following3_stateChanged(self, _):
        """When the very close following3 criteria is enabled/disabled."""
        self.update_very_close_status()
    @pyqtSlot(int)
    def on_checkbox_vc_indep3_stateChanged(self, _):
        """When the very close indep3 criteria is enabled/disabled."""
        self.update_very_close_status()

    @pyqtSlot(int)
    def on_checkbox_c_startend2_stateChanged(self, _):
        """When the close startend2 criteria is enabled/disabled."""
        self.update_close_status()
    @pyqtSlot(int)
    def on_checkbox_c_following3_stateChanged(self, _):
        """When the close following3 criteria is enabled/disabled."""
        self.update_close_status()
    @pyqtSlot(int)
    def on_checkbox_c_following2_stateChanged(self, _):
        """When the close following2 criteria is enabled/disabled."""
        self.update_close_status()
    @pyqtSlot(int)
    def on_checkbox_c_indep3_stateChanged(self, _):
        """When the close indep3 criteria is enabled/disabled."""
        self.update_close_status()
    @pyqtSlot(int)
    def on_checkbox_c_indep2_stateChanged(self, _):
        """When the close indep2 criteria is enabled/disabled."""
        self.update_close_status()

    @pyqtSlot(str)
    def on_lineedit_ref_word_textEdited(self, _):
        """When the ref word is changed."""
        self.update_ref_word_status()

    @pyqtSlot(int)
    def on_checkbox_advanced_settings_stateChanged(self, _):
        """When the advanced settings button is clicked."""
        self.set_advanced_settings_state(
            self.checkbox_advanced_settings.isChecked())

    @pyqtSlot()
    def on_pushbutton_default_settings_clicked(self):
        """When the default settings button is clicked."""
        self.put_default_settings()

    @pyqtSlot(str)
    def on_lineedit_word_list_textEdited(self, _):
        """When the word list is changed."""
        self.update_word_list_status()

    @pyqtSlot(float)
    def on_spinbox_ows_very_close_valueChanged(self, _):
        """When very close prob is changed."""
        self.update_probs()

    @pyqtSlot(float)
    def on_spinbox_ows_close_valueChanged(self, _):
        """When close prob is changed."""
        self.update_probs()

    @pyqtSlot()
    def on_pushbutton_help_clicked(self):
        """When the help button is clicked."""
        self.open_help()

    @pyqtSlot()
    def on_pushbutton_quit_clicked(self):
        """When the quit button is clicked."""
        self.quit()

    def put_default_settings(self):
        """Reset the interface with default settings."""
        self.lineedit_ref_word.setText(DEFAULT_REF_WORD)
        self.update_ref_word_status()
        self.checkbox_capital.setChecked(DEFAULT_CAPITAL_ENABLED)
        self.checkbox_script.setChecked(DEFAULT_SCRIPT_ENABLED)
        self.checkbox_cursive.setChecked(DEFAULT_CURSIVE_ENABLED)
        self.spinbox_lines.setValue(DEFAULT_LINES)
        self.spinbox_rws_number.setValue(DEFAULT_REF_WORD_NUMBER)
        self.spinbox_rws_prob.setValue(100 * DEFAULT_REF_WORD_PROB)
        self.spinbox_ows_very_close.setValue(100 * DEFAULT_VERY_CLOSE_PROB)
        self.spinbox_ows_close.setValue(100 * DEFAULT_CLOSE_PROB)
        self.update_probs()

        self.checkbox_vc_startend3.setChecked(
            DEFAULT_VERY_CLOSE_STARTEND3_ENABLED)
        self.checkbox_vc_startend2.setChecked(
            DEFAULT_VERY_CLOSE_STARTEND2_ENABLED)
        self.checkbox_vc_following4.setChecked(
            DEFAULT_VERY_CLOSE_FOLLOWING4_ENABLED)
        self.checkbox_vc_following3.setChecked(
            DEFAULT_VERY_CLOSE_FOLLOWING3_ENABLED)
        self.checkbox_vc_indep3.setChecked(
            DEFAULT_VERY_CLOSE_INDEP3_ENABLED)

        self.checkbox_c_startend2.setChecked(
            DEFAULT_CLOSE_STARTEND2_ENABLED)
        self.checkbox_c_following3.setChecked(
            DEFAULT_CLOSE_FOLLOWING3_ENABLED)
        self.checkbox_c_following2.setChecked(
            DEFAULT_CLOSE_FOLLOWING2_ENABLED)
        self.checkbox_c_indep3.setChecked(
            DEFAULT_CLOSE_INDEP3_ENABLED)
        self.checkbox_c_indep2.setChecked(
            DEFAULT_CLOSE_INDEP2_ENABLED)

        self.lineedit_word_list.setText(DEFAULT_WORD_LIST_FILE)
        self.update_word_list_status()

        self.checkbox_advanced_settings.setChecked(
            DEFAULT_ADVANCED_SETTINGS_ENABLED)
        self.set_advanced_settings_state(DEFAULT_ADVANCED_SETTINGS_ENABLED)

    def update_probs(self):
        remaining = 100
        vc_prob = self.spinbox_ows_very_close.value()
        remaining -= vc_prob
        c_prob = min(remaining, self.spinbox_ows_close.value())
        remaining -= c_prob
        self.spinbox_ows_close.setValue(c_prob)
        other_prob = remaining
        self.spinbox_ows_other.setValue(other_prob)

    def get_word_list_path(self):
        """Returns the path of the specified word list."""
        word_list_file = normalize(self.lineedit_word_list.text())
        self.lineedit_word_list.setText(word_list_file)
        return path.join(WORD_LIST_DIRECTORY, word_list_file)

    def update_word_list_status(self):
        """Updates status of the radiobutton which indicates wether the
        specified word list file is valid or not."""
        word_list_ok = path.isfile(self.get_word_list_path())
        if word_list_ok:
            self.radiobutton_word_list_ok.setChecked(True)
            self.pushbutton_generate.setEnabled(True)
        else:
            self.radiobutton_word_list_ok.setChecked(False)
            self.pushbutton_generate.setEnabled(False)

    def get_raw_ref_word(self):
        """Returns the ref word."""
        raw_ref_word = normalize(self.lineedit_ref_word.text())
        self.lineedit_ref_word.setText(raw_ref_word)
        return raw_ref_word

    def update_ref_word_status(self):
        """Desactivates the generate button if the specified ref word is
        invalid."""
        raw_ref_word = self.get_raw_ref_word()
        if is_correct_word(raw_ref_word):
            self.pushbutton_generate.setEnabled(True)
        else:
            self.pushbutton_generate.setEnabled(False)

    def update_very_close_status(self):
        """Desactivates the generate button if no criteria is checked."""
        if (self.checkbox_vc_startend3.isChecked() or
            self.checkbox_vc_startend2.isChecked() or
            self.checkbox_vc_following4.isChecked() or
            self.checkbox_vc_following3.isChecked() or
            self.checkbox_vc_indep3.isChecked()):
            self.pushbutton_generate.setEnabled(True)
        else:
            self.pushbutton_generate.setEnabled(False)

    def update_close_status(self):
        """Desactivates the generate button if no criteria is checked."""
        if (self.checkbox_c_startend2.isChecked() or
            self.checkbox_c_following3.isChecked() or
            self.checkbox_c_following2.isChecked() or
            self.checkbox_c_indep3.isChecked() or
            self.checkbox_c_indep2.isChecked()):
            self.pushbutton_generate.setEnabled(True)
        else:
            self.pushbutton_generate.setEnabled(False)

    def set_advanced_settings_state(self, state):
        """Activates or desactivates the advanced settings panel."""
        self.frame_enabled_advanced_settings.setEnabled(state)

    def open_help(self):
        """Opens the help file."""
        try:
            webbrowser.open(HELP_PATH)
        except Exception as e:
            self.state_msg(0, "Impossible d'ouvrir l'aide : <{}>".format(e))

    def quit(self):
        """Closes the GUI."""
        self.close()

    def get_params(self):
        """Returns all the params set in the GUI (in a dict)."""
        p = {
            "rrw": self.get_raw_ref_word(),
            "capital": self.checkbox_capital.isChecked(),
            "script": self.checkbox_script.isChecked(),
            "cursive": self.checkbox_cursive.isChecked(),
            "lines": self.spinbox_lines.value(),
            "rw_number": self.spinbox_rws_number.value(),
            "rw_prob": self.spinbox_rws_prob.value() / 100,
            "vc_prob": self.spinbox_ows_very_close.value() / 100,
            "c_prob": self.spinbox_ows_close.value() / 100,
            "other_prob": self.spinbox_ows_other.value() / 100,
            "vc_startend3": self.checkbox_vc_startend3.isChecked(),
            "vc_startend2": self.checkbox_vc_startend2.isChecked(),
            "vc_following4": self.checkbox_vc_following4.isChecked(),
            "vc_following3": self.checkbox_vc_following3.isChecked(),
            "vc_indep3": self.checkbox_vc_indep3.isChecked(),
            "c_startend2": self.checkbox_c_startend2.isChecked(),
            "c_following3": self.checkbox_c_following3.isChecked(),
            "c_following2": self.checkbox_c_following2.isChecked(),
            "c_indep3": self.checkbox_c_indep3.isChecked(),
            "c_indep2": self.checkbox_c_indep2.isChecked(),
            "word_list_path": self.get_word_list_path(),
        }
        return p

    def state_msg(self, level, msg):
        """Prints the specified message in the state text box."""
        if level >= DEBUG_LEVEL:
            fancy_msg = "[{}] {}\n".format(FANCY_LEVELS[level], msg)
            self.textbrowser_state_info.append(fancy_msg)
            if DEBUG_CONSOLE:
                print(fancy_msg)

class SheetGenerator(object):
    """Instance of a sheet generator. Handles the logic to generate the pdf
    file."""

    state_msg = pyqtSignal(int, str, name="state_msg")

    def __init__(self, p):
        """Init method."""
        super().__init__()
        # Params received from the GUI instance
        self.p = p
        self.rw = normalize_word(self.p["rrw"])
        self.vc_list = []
        self.c_list = []

    def create_lists(self):
        """Creates lists of very close and close words."""
        # No need to test, the previous logic ensures that the path is correct
        with open(
            self.p["word_list_path"], "r", encoding=ENC) as word_list_file:
            raw_word = normalize_line(word_list_file.readline())
            while raw_word:
                word = normalize_word(raw_word)
                if self.is_very_close(word):
                    self.vc_list.append(raw_word)
                if self.is_close(word):
                    self.c_list.append(raw_word)
                raw_word = normalize_line(word_list_file.readline())

    def is_very_close(self, word):
        """Tests if the specified word is very close according to the definitions."""
        if self.p["vc_startend3"] and self.check_startend(3, self.rw, word):
            return True
        if self.p["vc_startend2"] and self.check_startend(2, self.rw, word):
            return True
        if self.p["vc_following4"] and self.check_following(4, self.rw, word):
            return True
        if self.p["vc_following3"] and self.check_following(3, self.rw, word):
            return True
        if self.p["vc_indep3"] and self.check_indep(3, self.rw, word):
            return True
        return False

    def is_close(self, word):
        """Tests if the specified word is close according to the definitions.
        """
        if self.p["c_startend2"] and self.check_startend(2, self.rw, word):
            return True
        if self.p["c_following3"] and self.check_following(3, self.rw, word):
            return True
        if self.p["c_following2"] and self.check_following(2, self.rw, word):
            return True
        if self.p["c_indep3"] and self.check_indep(3, self.rw, word):
            return True
        if self.p["c_indep2"] and self.check_indep(2, self.rw, word):
            return True
        return False

    def check_indep(self, n, word_1, word_2):
        """Checks if both words have n indep chars in common."""
        word_2 = [c for c in word_2]
        common_count = 0
        for c in word_1:
            if c in word_2:
                common_count += 1
                word_2.remove(c)
        return common_count >= n

    def check_startend(self, n, word_1, word_2):
        """Checks if both words have n start or end chars in common."""
        if len(word_1) < n or len(word_2) < n:
            return False
        else:
            return (
                word_1[:n] == word_2[:n] or
                word_1[-(n + 1):] == word_2[-(n + 1):])

    def check_following(self, n, word_1, word_2):
        """Checks if both words have n following chars in common."""
        if len(word_1) < n or len(word_2) < n:
            return False
        for i in range(len(word_1) - (n - 1)):
            if word_1[i:i + n] in word_2:
                return True
        return False

    def generate(self):
        """Main process of the generation of the sheet."""
        self.create_lists()
        if not self.vc_list or not self.c_list:
            self.state_msg.emit(0, "One of the list is empty! Abort.")
            return
        if len(self.vc_list) < WORD_NB_WARNING_THRESHOLD:
            self.state_msg.emit(
                1, "Very few very close words found: {}"
                .format(len(self.vc_list)))
        if len(self.c_list) < WORD_NB_WARNING_THRESHOLD:
            self.state_msg.emit(
                1, "Very few close words found: {}".format(len(self.c_list)))
        

def main():
    """Launcher."""
    app = QApplication(sys.argv)
    master = SheetCreatorUiMaster()
    master.show()

    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
