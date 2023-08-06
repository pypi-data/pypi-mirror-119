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
Common models.
Contains a generic File list model and an Item for that model.
Used by the Importer, Gimlet and Tool project items but this may be handy for other project items
as well.

:authors: P. Savolainen (VTT), P. Vennström (VTT), A. Soininen (VTT)
:date:    5.6.2020
"""
from collections import namedtuple
from itertools import combinations, takewhile
import json
from pathlib import Path
from PySide2.QtCore import QAbstractItemModel, QAbstractListModel, QFileInfo, QModelIndex, Qt, Signal, QMimeData
from PySide2.QtWidgets import QFileIconProvider
from PySide2.QtGui import QStandardItemModel, QStandardItem, QPixmap, QPainter, QIcon, QColor
from spine_engine.project_item.project_item_resource import extract_packs
from .utils import CmdLineArg, Database, LabelArg


class FileListModel(QAbstractItemModel):
    """A model for files to be shown in a file tree view."""

    FileItem = namedtuple("FileItem", ["resource"])
    PackItem = namedtuple("PackItem", ["label", "resources"])

    def __init__(self, header_label="", draggable=False):
        """
        Args:
            header_label (str): header label
            draggable (bool): if True, the top level items are drag and droppable
        """
        super().__init__()
        self._header_label = header_label
        self._draggable = draggable
        self._single_resources = list()
        self._pack_resources = list()

    def rowCount(self, parent=QModelIndex()):
        if not parent.isValid():
            return len(self._single_resources) + len(self._pack_resources)
        parent_row = parent.row()
        if parent_row < len(self._single_resources):
            return 0
        return len(self._pack_resources[parent_row - len(self._single_resources)].resources)

    def columnCount(self, parent=QModelIndex()):
        return 1

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        """Returns header information."""
        if role != Qt.DisplayRole or orientation != Qt.Horizontal:
            return None
        return self._header_label

    def data(self, index, role=Qt.DisplayRole):
        """Returns data associated with given role at given index."""
        if not index.isValid():
            return None
        if role == Qt.DisplayRole:
            row = index.row()
            pack_label = index.internalPointer()
            if pack_label is None:
                if row < len(self._single_resources):
                    resource = self._single_resources[row].resource
                    return resource.label
                return self._pack_resources[row - len(self._single_resources)].label
            return self._pack_resources[self._pack_index(pack_label)].resources[row].path
        if role == Qt.DecorationRole:
            row = index.row()
            pack_label = index.internalPointer()
            if pack_label is None:
                if row < len(self._single_resources):
                    resource = self._single_resources[row].resource
                else:
                    return None
            else:
                resource = self._pack_resources[self._pack_index(pack_label)].resources[row]
            if resource.hasfilepath:
                return QFileIconProvider().icon(QFileInfo(resource.path))
        if role == Qt.ToolTipRole:
            row = index.row()
            pack_label = index.internalPointer()
            if pack_label is None:
                if row < len(self._single_resources):
                    resource = self._single_resources[row].resource
                else:
                    return None
            else:
                resource = self._pack_resources[self._pack_index(pack_label)].resources[row]
            if resource.type_ == "database":
                return resource.url
            return (
                resource.path
                if resource.hasfilepath
                else f"This file will be generated by {resource.provider_name} upon execution."
            )
        return None

    def flags(self, index):
        if index.internalPointer() is None:
            if index.row() < len(self._single_resources):
                flags = Qt.ItemIsSelectable | Qt.ItemIsEnabled | Qt.ItemNeverHasChildren
            else:
                flags = Qt.ItemIsSelectable | Qt.ItemIsEnabled
            if self._draggable:
                flags = flags | Qt.ItemIsDragEnabled
            return flags
        return Qt.ItemIsSelectable | Qt.ItemIsEnabled | Qt.ItemNeverHasChildren

    def mimeData(self, indexes):
        data = QMimeData()
        text = json.dumps(("labels", ";;".join([index.data() for index in indexes])))
        data.setText(text)
        return data

    def resource(self, index):
        """Returns the resource at given index.

        Args:
            index (QModelIndex): index

        Returns:
            ProjectItemResource: resource
        """
        pack_label = index.internalPointer()
        if pack_label is None:
            row = index.row()
            if row < len(self._single_resources):
                return self._single_resources[row].resource
            pack_resources = self._pack_resources[row - len(self._single_resources)].resources
            return pack_resources[0] if pack_resources else None
        return self._pack_resources[self._pack_index(pack_label)].resources[index.row()]

    def parent(self, index):
        pack_label = index.internalPointer()
        if pack_label is None:
            return QModelIndex()
        return self.createIndex(len(self._single_resources) + self._pack_index(pack_label), 0)

    def index(self, row, column, parent=QModelIndex()):
        if not parent.isValid():
            return self.createIndex(row, column, None)
        parent_row = parent.row()
        if parent_row < len(self._single_resources):
            return QModelIndex()
        pack_label = self._pack_resources[parent_row - len(self._single_resources)].label
        return self.createIndex(row, column, pack_label)

    def update(self, resources):
        """Updates the model according to given list of resources.

        Args:
            resources (Iterable of ProjectItemResource): resources
        """
        self.beginResetModel()
        single_resources, pack_resources = extract_packs(resources)
        new_singles = [self.FileItem(r) for r in single_resources]
        new_packs = [
            self.PackItem(label, [r for r in r_list if r.hasfilepath]) for label, r_list in pack_resources.items()
        ]
        self._single_resources = new_singles
        self._pack_resources = new_packs
        self.endResetModel()

    def duplicate_paths(self):
        """Checks if resources in the model have duplicate file paths.

        Returns:
            set of str: set of duplicate file paths
        """
        single_paths = [Path(item.resource.path) for item in self._single_resources if item.resource.hasfilepath]
        pack_paths = [Path(r.path) for item in self._pack_resources for r in item.resources if r.hasfilepath]
        paths = single_paths + pack_paths
        duplicates = set()
        for p1, p2 in combinations(paths, 2):
            try:
                if p1.samefile(p2):
                    duplicates.add(str(p2))
            except OSError:
                # Sometimes file access fails e.g. in the middle of replacing
                # resources when a connected DC is being renamed.
                continue
        return duplicates

    def _pack_index(self, pack_label):
        """Finds a pack's index in pack resources list.

        Args:
            pack_label (str): pack label

        Returns:
            int: index to pack resources list
        """
        return len(list(takewhile(lambda item: item.label != pack_label, self._pack_resources)))


class CheckableFileListModel(FileListModel):
    """A model for checkable files to be shown in a file tree view."""

    FileItem = namedtuple("FileItem", ["resource", "checked"])
    PackItem = namedtuple("PackItem", ["label", "resources", "checked"])

    checked_state_changed = Signal(QModelIndex, bool)
    """Emitted when an item's checked state changes."""

    def data(self, index, role=Qt.DisplayRole):
        if role == Qt.CheckStateRole:
            if index.internalPointer() is None:
                row = index.row()
                if row < len(self._single_resources):
                    checked = self._single_resources[row].checked
                else:
                    checked = self._pack_resources[row - len(self._single_resources)].checked
                return Qt.Checked if checked else Qt.Unchecked
            return None
        return super().data(index, role)

    def checked_data(self, index):
        """Returns checked status and label for given top-level index.

        Args:
            index (QModelIndex): top-level index

        Returns:
            tuple: item label and checked flag
        """
        row = index.row()
        if row < len(self._single_resources):
            return self._single_resources[row].resource.label, self._single_resources[row].checked
        pack = self._pack_resources[row - len(self._single_resources)]
        return pack.label, pack.checked

    def is_checked(self, index):
        """Returns True if the item at given index is checked.

        Args:
            index (QModelIndex): index

        Returns:
            bool: True if the item is checked, False otherwise
        """
        pack_label = index.internalPointer()
        if pack_label is None:
            row = index.row()
            if row < len(self._single_resources):
                return self._single_resources[row].checked
            return self._pack_resources[row - len(self._single_resources)].checked
        return self._pack_resources[self._pack_index(pack_label)].checked

    def flags(self, index):
        flags = super().flags(index)
        if index.internalPointer() is None:
            return flags | Qt.ItemIsUserCheckable
        return flags

    def update(self, resources):
        """Updates the model according to given list of resources.

        Args:
            resources (Iterable of ProjectItemResource): resources
        """
        self.beginResetModel()
        unchecked_singles = {item.resource.label for item in self._single_resources if not item.checked}
        unchecked_packs = {item.label for item in self._pack_resources if not item.checked}
        unchecked = unchecked_singles | unchecked_packs
        single_resources, pack_resources = extract_packs(resources)
        new_singles = [self.FileItem(r, r.label not in unchecked) for r in single_resources]
        new_packs = [
            self.PackItem(label, [r for r in r_list if r.hasfilepath], label not in unchecked)
            for label, r_list in pack_resources.items()
        ]
        self._single_resources = new_singles
        self._pack_resources = new_packs
        self.endResetModel()

    def setData(self, index, value, role=Qt.EditRole):
        """Sets data in the model."""
        if role != Qt.CheckStateRole or not index.isValid():
            return False
        checked = value == Qt.Checked
        self.checked_state_changed.emit(index, checked)
        return True

    def set_initial_state(self, selected_items):
        """Fills model with incomplete data; needs a call to :func:`update` to make the model usable.

        Args:
            selected_items (dict): mapping from item label to checked flag
        """
        for label, selected in selected_items.items():
            self._pack_resources.append(self.PackItem(label, [], selected))

    def set_checked(self, index, checked):
        """Checks or unchecks given item.

        Args:
            index (QModelIndex): resource label
            checked (bool): checked flag
        """
        row = index.row()
        if row < len(self._single_resources):
            self._single_resources[row] = self._single_resources[row]._replace(checked=checked)
        else:
            row -= len(self._single_resources)
            self._pack_resources[row] = self._pack_resources[row]._replace(checked=checked)
        self.dataChanged.emit(index, index, [Qt.CheckStateRole])

    def index_with_file_path(self):
        """Tries to find an item that has a valid file path.

        Returns:
            QModelIndex: index to a item with usable file path or an invalid index if none found
        """
        for row, item in enumerate(self._single_resources):
            if item.checked and item.resource.hasfilepath:
                return self.index(row, 0)
        for pack_row, item in enumerate(self._pack_resources):
            if item.checked:
                for row, resource in enumerate(item.resources):
                    if resource.hasfilepath:
                        return self.index(row, 0, self.index(pack_row, 0))
        return QModelIndex()


class CommandLineArgItem(QStandardItem):
    def __init__(self, text="", rank=None, selectable=False, editable=False, drag_enabled=False, drop_enabled=False):
        super().__init__(text)
        self.setEditable(editable)
        self.setDropEnabled(drop_enabled)
        self.setDragEnabled(drag_enabled)
        self.setSelectable(selectable)
        self.set_rank(rank)

    def set_rank(self, rank):
        if rank is not None:
            icon = self._make_icon(rank)
            self.setIcon(icon)

    @staticmethod
    def _make_icon(rank=None):
        pixmap = QPixmap(16, 16)
        pixmap.fill(Qt.white)
        painter = QPainter(pixmap)
        painter.drawText(0, 0, 16, 16, Qt.AlignCenter, f"{rank}:")
        painter.end()
        return QIcon(pixmap)

    def setData(self, value, role=Qt.UserRole + 1):
        if role != Qt.EditRole:
            return super().setData(value, role=role)
        if value != self.data(role=role):
            self.model().replace_arg(self.row(), CmdLineArg(value))
        return False


class NewCommandLineArgItem(CommandLineArgItem):
    def __init__(self):
        super().__init__("Type new arg here...", selectable=True, editable=True)
        gray_color = qApp.palette().text().color()  # pylint: disable=undefined-variable
        gray_color.setAlpha(128)
        self.setForeground(gray_color)

    def setData(self, value, role=Qt.UserRole + 1):
        if role != Qt.EditRole:
            return super().setData(value, role=role)
        if value != self.data(role=role):
            self.model().append_arg(CmdLineArg(value))
        return False


class CommandLineArgsModel(QStandardItemModel):
    args_updated = Signal(list)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setHorizontalHeaderItem(0, QStandardItem("Command line arguments"))
        self._args = []

    def append_arg(self, arg):
        self.args_updated.emit(self._args + [arg])

    def replace_arg(self, row, arg):
        new_args = self._args.copy()
        new_args[row] = arg
        self.args_updated.emit(new_args)

    def mimeData(self, indexes):
        data = QMimeData()
        text = json.dumps(("rows", ";;".join([str(index.row()) for index in indexes])))
        data.setText(text)
        return data

    def dropMimeData(self, data, drop_action, row, column, parent):
        head, contents = json.loads(data.text())
        if head == "rows":
            rows = [int(x) for x in contents.split(";;")]
            head = [arg for k, arg in enumerate(self._args[:row]) if k not in rows]
            body = [self._args[k] for k in rows]
            tail = [arg for k, arg in enumerate(self._args[row:]) if k + row not in rows]
            new_args = head + body + tail
            self.args_updated.emit(new_args)
            return True
        if head == "labels":
            new_args = self._args[:row] + [LabelArg(arg) for arg in contents.split(";;")] + self._args[row:]
            self.args_updated.emit(new_args)
            return True
        return False

    @staticmethod
    def _reset_root(root, args, child_params, has_empty_row=True):
        last_row = root.rowCount()
        if has_empty_row:
            last_row -= 1
        count = len(args) - last_row
        for _ in range(count):
            root.insertRow(last_row, [CommandLineArgItem(**child_params)])
        if count < 0:
            count = -count
            first = last_row - count
            root.removeRows(first, count)
        for k, arg in enumerate(args):
            child = root.child(k)
            child.set_rank(k)
            child.setText(str(arg))
            color = QColor("red") if arg.missing else None
            child.setData(color, role=Qt.ForegroundRole)


class GimletCommandLineArgsModel(CommandLineArgsModel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.invisibleRootItem().appendRow(NewCommandLineArgItem())

    def reset_model(self, args):
        self._args = args
        self._reset_root(
            self.invisibleRootItem(), args, dict(editable=True, selectable=True, drag_enabled=True), has_empty_row=True
        )

    def canDropMimeData(self, data, drop_action, row, column, parent):
        return row >= 0


class ToolCommandLineArgsModel(CommandLineArgsModel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._spec_args_root = CommandLineArgItem("Specification arguments")
        self._tool_args_root = CommandLineArgItem("Tool arguments", drop_enabled=True)
        self.appendRow(self._spec_args_root)
        self.appendRow(self._tool_args_root)
        self._tool_args_root.appendRow(NewCommandLineArgItem())

    def reset_model(self, spec_args, tool_args):
        self._args = tool_args
        self._reset_root(self._spec_args_root, spec_args, dict(), has_empty_row=False)
        self._reset_root(
            self._tool_args_root, tool_args, dict(editable=True, selectable=True, drag_enabled=True), has_empty_row=True
        )

    def canDropMimeData(self, data, drop_action, row, column, parent):
        return parent.data() is not None and row >= 0


class DatabaseListModel(QAbstractListModel):
    """A model for exporter database lists."""

    def __init__(self, databases):
        """
        Args:
            databases (list of Database): databases to list
        """
        super().__init__()
        self._databases = databases

    def add(self, database):
        """
        Appends a database to the list.

        Args:
            database (Database): a database to add
        """
        row = len(self._databases)
        self.beginInsertRows(QModelIndex(), row, row)
        self._databases.append(database)
        self.endInsertRows()

    def data(self, index, role=Qt.DisplayRole):
        if not index.isValid():
            return None
        if role == Qt.DisplayRole:
            return self._databases[index.row()].url
        return None

    def insertRows(self, row, count, parent=QModelIndex()):
        self.beginInsertRows(parent, row, row + count - 1)
        self._databases = self._databases[:row] + [Database() for _ in range(count)] + self._databases[row:]
        self.endInsertRows()

    def item(self, url):
        """
        Returns database item for given URL.

        Args:
            url (str): database URL

        Returns:
            Database: a database
        """
        for db in self._databases:
            if db.url == url:
                return db
        raise RuntimeError(f"Database '{url}' not found.")

    def items(self):
        """
        Returns a list of databases this model contains.

        Returns:
            list of Database: database
        """
        return self._databases

    def remove(self, url):
        """
        Removes database item with given URL.

        Args:
            url (str): database URL

        Returns:
            Database: removed database or None if not found
        """
        for row, db in enumerate(self._databases):
            if db.url == url:
                self.removeRows(row, 1)
                return db
        return None

    def removeRows(self, row, count, parent=QModelIndex()):
        self.beginRemoveRows(parent, row, row + count - 1)
        self._databases = self._databases[:row] + self._databases[row + count :]
        self.endRemoveRows()

    def rowCount(self, parent=QModelIndex()):
        return len(self._databases)

    def update_url(self, old, new):
        """
        Updates a database URL.

        Args:
            old (str): old URL
            new (str): new URL
        """
        for row, db in enumerate(self._databases):
            if old == db.url:
                db.url = new
                index = self.index(row, 0)
                self.dataChanged.emit(index, index, [Qt.DisplayRole])
                return

    def urls(self):
        """
        Returns database URLs.

        Returns:
            set of str: database URLs
        """
        return {db.url for db in self._databases}


class FullUrlListModel(QAbstractListModel):
    def __init__(self, parent=None):
        """
        Args:
            parent (QObject, optional): model's parent
            """
        super().__init__(parent)
        self._urls = list()

    def append(self, url):
        """
        Appends a URL to the model.

        Args:
            url (str): URL to append
        """
        n = len(self._urls)
        self.beginInsertRows(QModelIndex(), n, n)
        self._urls.append(url)
        self.endInsertRows()

    def data(self, index, role=Qt.DisplayRole):
        if not index.isValid():
            return None
        if role == Qt.DisplayRole:
            return self._urls[index.row()]
        return None

    def rowCount(self, parent=QModelIndex()):
        return len(self._urls)

    def set_urls(self, urls):
        """
        Sets model's URLs.

        Args:
            urls (Iterable of str): URLs
        """
        self.beginResetModel()
        self._urls = list(urls)
        self.endResetModel()

    def update_url(self, old, new):
        """
        Updates a database URL.

        Args:
            old (str): old URL
            new (str): new URL
        """
        for row, url in enumerate(self._urls):
            if old == url:
                self._urls[row] = new
                index = self.index(row, 0)
                self.dataChanged.emit(index, index, [Qt.DisplayRole])
                return
