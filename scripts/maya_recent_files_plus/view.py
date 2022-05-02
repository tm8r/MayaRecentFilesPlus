# -*- coding: utf-8 -*-
"""RecentFiles"""
from __future__ import absolute_import, division, print_function

from maya_recent_files_plus.vendor.Qt import QtCompat
from maya_recent_files_plus.vendor.Qt import QtCore
from maya_recent_files_plus.vendor.Qt import QtWidgets

from maya_recent_files_plus import file_helper
from maya_recent_files_plus.libs.qt.stylesheet import StyleSheet
from maya_recent_files_plus.libs.qt.widgets import collapse_widget

from maya import cmds
from maya import OpenMayaUI as omui
from maya.app.general.mayaMixin import MayaQWidgetBaseMixin

try:
    long
except NameError:
    long = int

try:
    MAYA_WINDOW = QtCompat.wrapInstance(long(omui.MQtUtil.mainWindow()), QtWidgets.QWidget)
except:
    MAYA_WINDOW = None

_ID_FORMAT = "{0}.{1}"


class RecentFilesPlus(MayaQWidgetBaseMixin, QtWidgets.QMainWindow):
    """view"""

    def __init__(self, parent=MAYA_WINDOW):
        """initialize"""
        super(RecentFilesPlus, self).__init__(parent)
        self._makeMayaStandaloneWindow()
        self.setWindowTitle("Recent Files Plus")
        self.setWindowFlags(QtCore.Qt.Window)
        self.setObjectName(self.window_name())
        self.setProperty("saveWindowPref", True)
        self.setStyleSheet(StyleSheet().core_css)

    @classmethod
    def window_name(cls):
        return _ID_FORMAT.format(cls.__module__, cls.__name__)

    @classmethod
    def open(cls, *args):
        """open window"""
        if cmds.window(cls.window_name(), q=True, ex=True):
            cmds.deleteUI(cls.window_name())
        win = cls()
        win._create_ui()
        win.show()

    def _create_ui(self):
        self.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Maximum)
        self.root_widget = QtWidgets.QFrame(self)
        self.root_widget.setObjectName("root")
        self.setMinimumSize(QtCore.QSize(600, 200))
        self.setMaximumHeight(390)
        self.setCentralWidget(self.root_widget)

        root_layout = QtWidgets.QGridLayout(self.root_widget)
        root_layout.setObjectName("root_layout")
        root_layout.setContentsMargins(8, 8, 8, 8)

        main_widget = QtWidgets.QFrame()
        main_layout = QtWidgets.QVBoxLayout()
        main_widget.setLayout(main_layout)

        tool_content_wrapper = QtWidgets.QScrollArea()
        tool_content_wrapper.setWidget(main_widget)
        tool_content_wrapper.setFrameShape(QtWidgets.QFrame.NoFrame)
        tool_content_wrapper.setWidgetResizable(True)
        tool_content_wrapper.setContentsMargins(0, 0, 0, 0)

        root_layout.addWidget(tool_content_wrapper, 0, 0, 1, 1)

        wrap_widget = collapse_widget.QCollapseWidget("Recent Files")
        wrap_widget.set_collapsible(False)
        main_layout.addWidget(wrap_widget)

        for file_path, file_type in file_helper.get_recent_files().items():
            element_layout = QtWidgets.QHBoxLayout()
            wrap_widget.addLayout(element_layout)
            element_line = QtWidgets.QLineEdit()
            element_line.setReadOnly(True)
            element_line.setText(file_path)
            element_layout.addWidget(element_line)

            import_button = QtWidgets.QPushButton("Import")
            import_button.setFixedWidth(70)
            import_button.clicked.connect(lambda x=file_path, y=file_type: self._on_import_button_clicked(x, y))
            element_layout.addWidget(import_button)

            reference_button = QtWidgets.QPushButton("Reference")
            reference_button.setFixedWidth(70)
            reference_button.clicked.connect(lambda x=file_path, y=file_type: self._on_reference_button_clicked(x, y))
            element_layout.addWidget(reference_button)

            open_button = QtWidgets.QPushButton("Open")
            open_button.setFixedWidth(70)
            open_button.clicked.connect(lambda x=file_path, y=file_type: self._on_open_button_clicked(x, y))
            element_layout.addWidget(open_button)

    def keyPressEvent(self, event):
        u"""key press event

        Args:
            event (Qt.QtGui.QKeyEvent): key event
        """
        if event.key() == QtCore.Qt.Key_Escape:
            self.close()
            return
        event.accept()

    def _on_open_button_clicked(self, path, file_type):
        file_helper.open_file(path, file_type)
        self.close()

    def _on_import_button_clicked(self, path, file_type):
        file_helper.open_file_specifying_mode(path, file_type, file_helper.FileOpenMode.Import, parent=self)
        self.close()

    def _on_reference_button_clicked(self, path, file_type):
        file_helper.open_file_specifying_mode(path, file_type, file_helper.FileOpenMode.Reference, parent=self)
        self.close()
