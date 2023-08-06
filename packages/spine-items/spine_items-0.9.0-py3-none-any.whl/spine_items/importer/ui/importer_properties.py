# -*- coding: utf-8 -*-
######################################################################################################################
# Copyright (C) 2017-2021 Spine project consortium
# This file is part of Spine Items.
# Spine Items is free software: you can redistribute it and/or modify it under the terms of the GNU Lesser General
# Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option)
# any later version. This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY;
# without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU Lesser General
# Public License for more details. You should have received a copy of the GNU Lesser General Public License along with
# this program. If not, see <http://www.gnu.org/licenses/>.
######################################################################################################################

################################################################################
## Form generated from reading UI file 'importer_properties.ui'
##
## Created by: Qt User Interface Compiler version 5.14.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import (QCoreApplication, QDate, QDateTime, QMetaObject,
    QObject, QPoint, QRect, QSize, QTime, QUrl, Qt)
from PySide2.QtGui import (QBrush, QColor, QConicalGradient, QCursor, QFont,
    QFontDatabase, QIcon, QKeySequence, QLinearGradient, QPalette, QPainter,
    QPixmap, QRadialGradient)
from PySide2.QtWidgets import *

from spine_items import resources_icons_rc

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(294, 370)
        self.verticalLayout = QVBoxLayout(Form)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.label_name = QLabel(Form)
        self.label_name.setObjectName(u"label_name")
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_name.sizePolicy().hasHeightForWidth())
        self.label_name.setSizePolicy(sizePolicy)
        self.label_name.setMinimumSize(QSize(0, 20))
        self.label_name.setMaximumSize(QSize(16777215, 20))
        font = QFont()
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.label_name.setFont(font)
        self.label_name.setStyleSheet(u"background-color: #ecd8c6;")
        self.label_name.setFrameShape(QFrame.Box)
        self.label_name.setFrameShadow(QFrame.Sunken)
        self.label_name.setAlignment(Qt.AlignCenter)
        self.label_name.setWordWrap(True)

        self.verticalLayout.addWidget(self.label_name)

        self.scrollArea_6 = QScrollArea(Form)
        self.scrollArea_6.setObjectName(u"scrollArea_6")
        self.scrollArea_6.setWidgetResizable(True)
        self.scrollAreaWidgetContents_5 = QWidget()
        self.scrollAreaWidgetContents_5.setObjectName(u"scrollAreaWidgetContents_5")
        self.scrollAreaWidgetContents_5.setGeometry(QRect(0, 0, 292, 348))
        self.verticalLayout_21 = QVBoxLayout(self.scrollAreaWidgetContents_5)
        self.verticalLayout_21.setObjectName(u"verticalLayout_21")
        self.horizontalLayout_9 = QHBoxLayout()
        self.horizontalLayout_9.setSpacing(4)
        self.horizontalLayout_9.setObjectName(u"horizontalLayout_9")
        self.label_specification = QLabel(self.scrollAreaWidgetContents_5)
        self.label_specification.setObjectName(u"label_specification")
        sizePolicy1 = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.label_specification.sizePolicy().hasHeightForWidth())
        self.label_specification.setSizePolicy(sizePolicy1)
        self.label_specification.setMaximumSize(QSize(16777215, 16777215))
        font1 = QFont()
        font1.setPointSize(8)
        self.label_specification.setFont(font1)

        self.horizontalLayout_9.addWidget(self.label_specification)

        self.comboBox_specification = QComboBox(self.scrollAreaWidgetContents_5)
        self.comboBox_specification.setObjectName(u"comboBox_specification")
        sizePolicy2 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.comboBox_specification.sizePolicy().hasHeightForWidth())
        self.comboBox_specification.setSizePolicy(sizePolicy2)

        self.horizontalLayout_9.addWidget(self.comboBox_specification)

        self.toolButton_edit_specification = QToolButton(self.scrollAreaWidgetContents_5)
        self.toolButton_edit_specification.setObjectName(u"toolButton_edit_specification")
        self.toolButton_edit_specification.setMinimumSize(QSize(22, 22))
        self.toolButton_edit_specification.setMaximumSize(QSize(22, 22))
        icon = QIcon()
        icon.addFile(u":/icons/wrench.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.toolButton_edit_specification.setIcon(icon)
        self.toolButton_edit_specification.setIconSize(QSize(16, 16))
        self.toolButton_edit_specification.setPopupMode(QToolButton.InstantPopup)

        self.horizontalLayout_9.addWidget(self.toolButton_edit_specification)


        self.verticalLayout_21.addLayout(self.horizontalLayout_9)

        self.treeView_files = QTreeView(self.scrollAreaWidgetContents_5)
        self.treeView_files.setObjectName(u"treeView_files")
        font2 = QFont()
        font2.setPointSize(10)
        self.treeView_files.setFont(font2)
        self.treeView_files.setContextMenuPolicy(Qt.CustomContextMenu)
        self.treeView_files.setTextElideMode(Qt.ElideLeft)
        self.treeView_files.setUniformRowHeights(True)

        self.verticalLayout_21.addWidget(self.treeView_files)

        self.cancel_on_error_checkBox = QCheckBox(self.scrollAreaWidgetContents_5)
        self.cancel_on_error_checkBox.setObjectName(u"cancel_on_error_checkBox")
        self.cancel_on_error_checkBox.setChecked(True)

        self.verticalLayout_21.addWidget(self.cancel_on_error_checkBox)

        self.line_6 = QFrame(self.scrollAreaWidgetContents_5)
        self.line_6.setObjectName(u"line_6")
        self.line_6.setFrameShape(QFrame.HLine)
        self.line_6.setFrameShadow(QFrame.Sunken)

        self.verticalLayout_21.addWidget(self.line_6)

        self.horizontalLayout_13 = QHBoxLayout()
        self.horizontalLayout_13.setObjectName(u"horizontalLayout_13")
        self.horizontalSpacer_17 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_13.addItem(self.horizontalSpacer_17)

        self.toolButton_open_dir = QToolButton(self.scrollAreaWidgetContents_5)
        self.toolButton_open_dir.setObjectName(u"toolButton_open_dir")
        sizePolicy1.setHeightForWidth(self.toolButton_open_dir.sizePolicy().hasHeightForWidth())
        self.toolButton_open_dir.setSizePolicy(sizePolicy1)
        self.toolButton_open_dir.setMinimumSize(QSize(22, 22))
        self.toolButton_open_dir.setMaximumSize(QSize(22, 22))
        icon1 = QIcon()
        icon1.addFile(u":/icons/folder-open-regular.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.toolButton_open_dir.setIcon(icon1)

        self.horizontalLayout_13.addWidget(self.toolButton_open_dir)


        self.verticalLayout_21.addLayout(self.horizontalLayout_13)

        self.scrollArea_6.setWidget(self.scrollAreaWidgetContents_5)

        self.verticalLayout.addWidget(self.scrollArea_6)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.label_name.setText(QCoreApplication.translate("Form", u"Name", None))
        self.label_specification.setText(QCoreApplication.translate("Form", u"Specification", None))
#if QT_CONFIG(tooltip)
        self.comboBox_specification.setToolTip(QCoreApplication.translate("Form", u"<html><head/><body><p>Specification for this Importer</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.toolButton_edit_specification.setToolTip(QCoreApplication.translate("Form", u"<html><head/><body><p>Edit specification.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.cancel_on_error_checkBox.setToolTip(QCoreApplication.translate("Form", u"If there are any errors when trying to import data cancel the whole import.", None))
#endif // QT_CONFIG(tooltip)
        self.cancel_on_error_checkBox.setText(QCoreApplication.translate("Form", u"Cancel import on error", None))
#if QT_CONFIG(tooltip)
        self.toolButton_open_dir.setToolTip(QCoreApplication.translate("Form", u"<html><head/><body><p>Open this Importer's project directory in file browser</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
    # retranslateUi

