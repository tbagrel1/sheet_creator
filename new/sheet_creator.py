#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Sheet Creator X."""

from params import *

import sys
import os
import subprocess
from random import randint, random, choice, choices
from PyQt5.QtCore import pyqtSignal, pyqtSlot, QObject
from PyQt5.QtWidgets import QWidget, QApplication
from ui.sheet_creator_master_ui import Ui_master

# TODO: Erreur sur la creation des listes de mots
# TODO: Erreur sur le replace

import webbrowser

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

    @pyqtSlot()
    def on_pushbutton_generate_clicked(self):
        """When the generate button is clicked."""
        self.generate()

    @pyqtSlot(int)
    def on_checkbox_vc_startend3_stateChanged(self, _):
        """When the very close startend3 criteria is enabled/disabled."""
        self.update_status()
    @pyqtSlot(int)
    def on_checkbox_vc_startend2_stateChanged(self, _):
        """When the very close startend2 criteria is enabled/disabled."""
        self.update_status()
    @pyqtSlot(int)
    def on_checkbox_vc_following4_stateChanged(self, _):
        """When the very close following4 criteria is enabled/disabled."""
        self.update_status()
    @pyqtSlot(int)
    def on_checkbox_vc_following3_stateChanged(self, _):
        """When the very close following3 criteria is enabled/disabled."""
        self.update_status()
    @pyqtSlot(int)
    def on_checkbox_vc_indep3_stateChanged(self, _):
        """When the very close indep3 criteria is enabled/disabled."""
        self.update_status()

    @pyqtSlot(int)
    def on_checkbox_c_startend2_stateChanged(self, _):
        """When the close startend2 criteria is enabled/disabled."""
        self.update_status()
    @pyqtSlot(int)
    def on_checkbox_c_following3_stateChanged(self, _):
        """When the close following3 criteria is enabled/disabled."""
        self.update_status()
    @pyqtSlot(int)
    def on_checkbox_c_following2_stateChanged(self, _):
        """When the close following2 criteria is enabled/disabled."""
        self.update_status()
    @pyqtSlot(int)
    def on_checkbox_c_indep3_stateChanged(self, _):
        """When the close indep3 criteria is enabled/disabled."""
        self.update_status()
    @pyqtSlot(int)
    def on_checkbox_c_indep2_stateChanged(self, _):
        """When the close indep2 criteria is enabled/disabled."""
        self.update_status()

    @pyqtSlot(str)
    def on_lineedit_ref_word_textEdited(self, _):
        """When the ref word is changed."""
        self.update_status()

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
        self.update_status()

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
        self.update_status()

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

    def get_word_list_status(self):
        """Is the word list constraint ok?."""
        word_list_ok = path.isfile(self.get_word_list_path())
        self.radiobutton_word_list_ok.setChecked(word_list_ok)
        return word_list_ok

    def get_raw_ref_word(self):
        """Returns the ref word."""
        raw_ref_word = normalize(self.lineedit_ref_word.text())
        self.lineedit_ref_word.setText(raw_ref_word)
        return raw_ref_word

    def get_ref_word_status(self):
        """Is the constraint on the ref word ok?"""
        raw_ref_word = self.get_raw_ref_word()
        return is_correct_word(raw_ref_word)

    def get_very_close_status(self):
        """Is the constraint on the very close parmams ok?."""
        return (
            self.checkbox_vc_startend3.isChecked() or
            self.checkbox_vc_startend2.isChecked() or
            self.checkbox_vc_following4.isChecked() or
            self.checkbox_vc_following3.isChecked() or
            self.checkbox_vc_indep3.isChecked())

    def update_status(self):
        """Desactivates the generate button if at least one constraint is not
        ok."""
        self.pushbutton_generate.setEnabled(
            self.get_word_list_status() and
            self.get_ref_word_status() and
            self.get_very_close_status() and
            self.get_close_status())

    def get_close_status(self):
        """Is the constraint on the close params ok?."""
        return (
            self.checkbox_c_startend2.isChecked() or
            self.checkbox_c_following3.isChecked() or
            self.checkbox_c_following2.isChecked() or
            self.checkbox_c_indep3.isChecked() or
            self.checkbox_c_indep2.isChecked())

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

    @pyqtSlot(int, str)
    def state_msg(self, level, msg):
        """Prints the specified message in the state text box."""
        if level <= DEBUG_LEVEL:
            fancy_msg = "{} {}".format(FANCY_LEVELS[level], msg)
            self.textbrowser_state_info.append(fancy_msg)
            if DEBUG_CONSOLE:
                print(fancy_msg)

    def generate(self):
        """Generates the PDF file and opens it."""
        sheet_generator = SheetGenerator(self.get_params())
        sheet_generator.state_msg.connect(self.state_msg)
        sheet_generator.generate()

class SheetGenerator(QObject):
    """Instance of a sheet generator. Handles the logic to generate the pdf
    file."""

    state_msg = pyqtSignal(int, str)

    def __init__(self, p):
        """Init method."""
        super().__init__()
        # Params received from the GUI instance
        self.p = p
        self.rw = normalize_word(self.p["rrw"])
        self.vc_list = []
        self.c_list = []
        self.other_list = []

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
                if True:
                    self.other_list.append(raw_word)
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
        else:
            self.state_msg.emit(
                2, "Very close words found: {}".format(len(self.vc_list)))
        if len(self.c_list) < WORD_NB_WARNING_THRESHOLD:
            self.state_msg.emit(
                1, "Very few close words found: {}".format(len(self.c_list)))
        else:
            self.state_msg.emit(
                2, "Close words found: {}".format(len(self.c_list)))
        try:
            self.create_tex_file()
        except Exception as e:
            self.state_msg.emit(
                0, "Unable to create the TeX file: <{}>".format(e))
        try:
            self.compile_tex_file()
        except Exception as e:
            self.state_msg.emit(
                0, "Unable to compile the TeX file: <{}>".format(e))
        try:
            self.display_pdf_file()
        except Exception as e:
            self.state_msg.emit(
                1, "Unable to display the PDF file: <{}>".format(e))

    def get_random_word(self):
        """Returns a random word according to the defined probs."""
        r = random()
        if r < self.p["vc_prob"]:
            return choice(self.vc_list)
        elif r < self.p["vc_prob"] + self.p["c_prob"]:
            return choice(self.c_list)
        else:
            return choice(self.other_list)

    def produce_tab(self, template_path):
        """Produces a tab according to the specified template."""
        with open(template_path, "r", encoding=ENC) as template_file:
            template = template_file.read()
        tab_lines = []
        for _ in range(self.p["lines"]):
            words = []
            index_where_ref_word = choices(
                list(range(5)), k=self.p["rw_number"])
            for i in range(5):
                if i in index_where_ref_word and random() < self.p["rw_prob"]:
                    words.append(self.rw)
                else:
                    words.append(self.get_random_word())
            tab_lines.append(" & ".join(words))
        tab_lines.append("")
        content = "\\\\\\hline\n".join(tab_lines)
        template = template.replace(TEMPLATE_FIELDS[0], self.rw)
        template = template.replace(TEMPLATE_FIELDS[1], content)
        return template

    def produce_content(self):
        """Produces tabs according to the settings."""
        tabs = []
        if self.p["capital"]:
            tabs.append(self.produce_tab(TEMPLATE_CAPITAL_PATH))
        if self.p["script"]:
            tabs.append(self.produce_tab(TEMPLATE_SCRIPT_PATH))
        if self.p["cursive"]:
            tabs.append(self.produce_tab(TEMPLATE_CURSIVE_PATH))
        return "\n".join(tabs)

    def create_tex_file(self):
        """Creates the TeX file."""
        output_dir = os.path.join(
            OUTPUT_DIRECTORY,
            OUTPUT_SUBDIR_FORMAT.format(self.rw))
        if not os.path.isdir(output_dir):
            os.mkdir(output_dir)
        self.output_dir = output_dir
        output_tex_file = OUTPUT_TEX_FILE_FORMAT.format(self.rw)
        self.output_tex_file = output_tex_file
        output_tex_path = os.path.join(
            output_dir,
            output_tex_file)
        output_pdf_path = os.path.join(
            output_dir,
            OUTPUT_PDF_FILE_FORMAT.format(self.rw))
        self.output_pdf_path = output_pdf_path
        with open(TEMPLATE_MAIN_PATH, "r", encoding=ENC) as template_file:
            template = template_file.read()
        template = template.replace(TEMPLATE_FIELDS[0], self.rw)
        template = template.replace(TEMPLATE_FIELDS[1], self.produce_content())
        with open(output_tex_path, "w", encoding=ENC) as output_tex_file:
            output_tex_file.write(template)
    
    def compile_tex_file(self):
        """Compiles the TeX file."""
        os.chdir(self.output_dir)
        result = subprocess.run(
            [TEX_COMPILE_CMD] + TEX_COMPILE_ARGS + [self.output_tex_file],
            stderr=subprocess.PIPE)
        if result.returncode != 0:
            raise Exception(result.stderr)

    def display_pdf_file(self):
        """Displays the PDF file."""
        webbrowser.open(self.output_pdf_path)

def main():
    """Launcher."""
    app = QApplication(sys.argv)
    master = SheetCreatorUiMaster()
    master.show()

    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
