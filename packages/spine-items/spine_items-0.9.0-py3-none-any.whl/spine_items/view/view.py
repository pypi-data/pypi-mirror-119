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

"""
Module for view class.

:authors: P. Savolainen (VTT), M. Marin (KHT), J. Olauson (KTH)
:date:   14.07.2018
"""

import os
from PySide2.QtCore import Qt, Slot
from PySide2.QtGui import QStandardItem, QStandardItemModel, QIcon, QPixmap
from sqlalchemy.engine.url import URL, make_url
from spinetoolbox.project_item.project_item import ProjectItem
from spinetoolbox.spine_db_editor.widgets.multi_spine_db_editor import MultiSpineDBEditor
from .item_info import ItemInfo
from .executable_item import ExecutableItem


class View(ProjectItem):
    def __init__(self, name, description, x, y, toolbox, project):
        """
        View class.

        Args:
            name (str): Object name
            description (str): Object description
            x (float): Initial X coordinate of item icon
            y (float): Initial Y coordinate of item icon
            project (SpineToolboxProject): the project this item belongs to
        """
        super().__init__(name, description, x, y, project)
        self._toolbox = toolbox
        self._references = dict()
        self.reference_model = QStandardItemModel()  # References to databases
        self._spine_ref_icon = QIcon(QPixmap(":/icons/Spine_db_ref_icon.png"))

    @staticmethod
    def item_type():
        """See base class."""
        return ItemInfo.item_type()

    @staticmethod
    def item_category():
        """See base class."""
        return ItemInfo.item_category()

    @property
    def executable_class(self):
        return ExecutableItem

    @staticmethod
    def from_dict(name, item_dict, toolbox, project):
        """See base class."""
        description, x, y = ProjectItem.parse_item_dict(item_dict)
        return View(name, description, x, y, toolbox, project)

    def make_signal_handler_dict(self):
        """Returns a dictionary of all shared signals and their handlers.
        This is to enable simpler connecting and disconnecting."""
        s = super().make_signal_handler_dict()
        s[self._properties_ui.toolButton_view_open_dir.clicked] = lambda checked=False: self.open_directory()
        s[self._properties_ui.pushButton_view_open_editor.clicked] = self.open_db_editor
        return s

    def restore_selections(self):
        """Restore selections into shared widgets when this project item is selected."""
        self._properties_ui.label_view_name.setText(self.name)
        self._properties_ui.treeView_view.setModel(self.reference_model)

    def save_selections(self):
        """Save selections in shared widgets for this project item into instance variables."""
        self._properties_ui.treeView_view.setModel(None)

    @Slot(bool)
    def open_db_editor(self, checked=False):
        """Opens selected db in the Spine database editor."""
        indexes = self._selected_indexes()
        db_url_codenames = self._db_url_codenames(indexes)
        if not db_url_codenames:
            return
        MultiSpineDBEditor(self._toolbox.db_mngr, db_url_codenames).show()

    def populate_reference_list(self):
        """Populates reference list."""
        self.reference_model.clear()
        self.reference_model.setHorizontalHeaderItem(0, QStandardItem("References"))  # Add header
        for db in sorted(self._references, reverse=True):
            qitem = QStandardItem(db)
            qitem.setFlags(~Qt.ItemIsEditable)
            qitem.setData(self._spine_ref_icon, Qt.DecorationRole)
            self.reference_model.appendRow(qitem)

    def update_name_label(self):
        """Update View tab name label. Used only when renaming project items."""
        self._properties_ui.label_view_name.setText(self.name)

    def upstream_resources_updated(self, resources):
        """See base class."""
        self._references.clear()
        for resource in resources:
            if resource.type_ == "database":
                url = make_url(resource.url)
                self._references[url.database] = (url, resource.provider_name)
            elif resource.type_ == "file":
                filepath = resource.path
                if os.path.splitext(filepath)[1] == ".sqlite":
                    url = URL("sqlite", database=filepath)
                    self._references[url.database] = (url, resource.provider_name)
        self.populate_reference_list()

    def replace_resource_from_upstream(self, old, new):
        """See base class."""
        if old.type_ == "database" and new.type_ == "database":
            old_url = make_url(old.url)
            new_url = make_url(new.url)
        elif old.type_ == "file":
            if os.path.splitext(old.path)[1] == ".sqlite" and os.path.splitext(new.path)[1] == ".sqlite":
                old_url = URL("sqlite", database=old.path)
                new_url = URL("sqlite", database=new.path)
            else:
                return
        else:
            return
        self._references[new_url.database] = self._references.pop(old_url.database)
        self.populate_reference_list()

    def _selected_indexes(self):
        """Returns selected indexes."""
        selection_model = self._properties_ui.treeView_view.selectionModel()
        if not selection_model.hasSelection():
            self._properties_ui.treeView_view.selectAll()
        return self._properties_ui.treeView_view.selectionModel().selectedRows()

    def _db_url_codenames(self, indexes):
        """Returns a dict mapping url to provider's name for given indexes in the reference model."""
        return dict(self._references[index.data(Qt.DisplayRole)] for index in indexes)

    def notify_destination(self, source_item):
        """See base class."""
        if source_item.item_type() == "Tool":
            self._logger.msg.emit(
                "Link established. You can visualize the output from Tool "
                f"<b>{source_item.name}</b> in View <b>{self.name}</b>."
            )
        elif source_item.item_type() == "Data Store":
            self._logger.msg.emit(
                "Link established. You can visualize Data Store "
                f"<b>{source_item.name}</b> in View <b>{self.name}</b>."
            )
        else:
            super().notify_destination(source_item)
