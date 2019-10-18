# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import os

from maya import cmds
from maya import mel


def onMayaDroppedPythonFile(*args, **kwargs):
    """for Maya2017.3+"""
    _create_shelf()


def onMayaDroppedMelFile():
    "for old Maya"
    _create_shelf()


def _create_shelf():
    script_path = os.path.dirname(__file__) + "/scripts"

    command = """
# -------------------------
# MayaRecentFilesPlus
# Author: @tm8r
# https://github.com/tm8r/MayaRecentFilesPlus
# -------------------------

import os
import sys

from maya import cmds

def open_recent_files():
    script_path = "{0}"
    if not os.path.exists(script_path):
        cmds.error("RecentFilesPlus install directory is not found. path={0}")
        return
    if script_path not in sys.path:
        sys.path.insert(0, script_path)

    import maya_recent_files_plus.view
    maya_recent_files_plus.view.RecentFilesPlus.open()

open_recent_files()""".format(script_path)

    shelf = mel.eval("$gShelfTopLevel=$gShelfTopLevel")
    parent = cmds.tabLayout(shelf, query=True, selectTab=True)
    cmds.shelfButton(
        command=command,
        image="pythonFamily.png",
        annotation="RecentFiles",
        label="RecentFiles",
        imageOverlayLabel="RecentFiles",
        sourceType="Python",
        parent=parent
    )


if __name__ == "_installShelfTm8rRecentFilesPlus":
    onMayaDroppedMelFile()
