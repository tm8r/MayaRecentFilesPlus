# -*- coding: utf-8 -*-
"""collapse widge"""
from __future__ import absolute_import, division, print_function

from ....vendor.Qt import QtCore
from ....vendor.Qt import QtWidgets


class QCollapseWidget(QtWidgets.QFrame):
    """collapse widget(like maya frameLayout)"""

    def __init__(self, label, parent=None):
        """initialize

        Args:
            label (unicode): ラベル
            parent (Qt.QtWidgets.QWidget): 親
        """
        super(QCollapseWidget, self).__init__(parent=parent)
        root_layout = QtWidgets.QVBoxLayout(self)
        root_layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(root_layout)

        self.heading = QtWidgets.QToolButton()
        self.heading.setObjectName("h1")
        self.heading.setToolButtonStyle(QtCore.Qt.ToolButtonTextBesideIcon)
        self.heading.setText(label)
        self.heading.setArrowType(QtCore.Qt.DownArrow)
        self.heading.setCheckable(True)
        self.heading.setChecked(True)
        self.heading.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        root_layout.addWidget(self.heading)

        self.inner_widget = QtWidgets.QFrame()
        self.inner_layout = QtWidgets.QVBoxLayout(self.inner_widget)
        root_layout.addWidget(self.inner_widget)

        self._connect_signals()

    def _connect_signals(self):
        self.heading.clicked.connect(self._on_heading_clicked)

    def _on_heading_clicked(self):
        self.collapse(self.heading.isChecked())

    def set_collapsible(self, enable):
        self.heading.setEnabled(enable)

    def collapse(self, checked):
        self.heading.setArrowType(QtCore.Qt.DownArrow if checked else QtCore.Qt.RightArrow)
        self.heading.setChecked(checked)
        self.inner_widget.setVisible(checked)

    def addWidget(self, widget):
        self.inner_layout.addWidget(widget)

    def addLayout(self, layout):
        self.inner_layout.addLayout(layout)
