# -*- coding: utf-8 -*-
"""file helper"""
from __future__ import absolute_import, division, print_function

from collections import OrderedDict
import os

from maya_recent_files_plus.vendor.Qt import QtWidgets

from maya_recent_files_plus.libs.maya.namespace import get_namespace_from_path

from maya import cmds
from maya import mel

_SCENE_DIRECTORY = "scenes"


class FileOpenMode(object):
    Open = "Open"
    Import = "Import"
    Reference = "Reference"


def get_recent_files():
    """returns recent file info

    Returns:
        OrderedDict: key: path, val: fileType
    """
    files = cmds.optionVar(q="RecentFilesList")
    file_types = cmds.optionVar(q="RecentFilesTypeList")
    files.reverse()
    file_types.reverse()
    return OrderedDict(zip(files, file_types))


def open_file(file_path, file_type):
    """open file

    Args:
        file_path (unicode):file path
        file_type (unicode): file type
    """
    cmds.file(force=True, new=True)
    mel.eval('openRecentFile("{0}", "{1}");'.format(file_path, file_type))

    parent_dir = os.path.basename(os.path.dirname(file_path))
    if parent_dir != _SCENE_DIRECTORY:
        return
    project_dir = os.path.dirname(os.path.dirname(file_path))
    mel.eval('setProject "' + project_dir + '";')


def open_file_specifying_mode(path, file_type, file_open_mode, parent=None, *args):
    """Open file in specified mode

    Args:
        path (unicode): path
        file_open_mode (str): mode
        file_type(unicode): callback
        parent(Qt.QtWidgets.QWidget): parent widget
    """
    if file_open_mode == FileOpenMode.Open:
        res = QtWidgets.QMessageBox.question(parent,
                                             "Confirm",
                                             u"Open {0}".format(path),
                                             QtWidgets.QMessageBox.Ok,
                                             QtWidgets.QMessageBox.No)
        if res != QtWidgets.QMessageBox.Ok:
            return
        open_file(path, file_type)
    else:
        _include_file_using_namespace(path, file_open_mode, parent)


def _include_file_using_namespace(path, file_open_mode, parent=None):
    """load file with namespace

    Args:
        path (unicode): path
        file_open_mode (FileOpenMode): mode
        parent(Qt.QtWidgets.QWidget): parent widget
    """
    if file_open_mode == FileOpenMode.Open:
        return
    normal_label = file_open_mode
    confirm_text = u"{0} {1}".format(normal_label, path)

    default_namespace_label = u"{0}(Namespace)".format(normal_label)
    specific_namespace_label = u"{0}(Specify Namespace)".format(normal_label)
    apply_labels = [normal_label, default_namespace_label, specific_namespace_label]

    res = cmds.confirmDialog(t="Confirm", m=confirm_text,
                             button=[normal_label, default_namespace_label, specific_namespace_label, "Cancel"],
                             defaultButton=normal_label, cancelButton="Cancel", dismissString="Cancel")

    if res not in apply_labels:
        return

    namespace = ":"
    if res == default_namespace_label:
        namespace = get_namespace_from_path(path)
    elif res == specific_namespace_label:
        specified_namespace, confirmed = QtWidgets.QInputDialog.getText(
            parent,
            "{0} Namespace".format(normal_label),
            "Namespace",
            text=get_namespace_from_path(path)
        )
        if not confirmed:
            return
        if specified_namespace:
            namespace = specified_namespace

    if file_open_mode == FileOpenMode.Import:
        cmds.file(path, i=True, namespace=namespace)
    elif file_open_mode == FileOpenMode.Reference:
        cmds.file(path, r=True, namespace=namespace)
