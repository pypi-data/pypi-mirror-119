######################################################################################################################
# Copyright (C) 2017-2021 Spine project consortium
# This file is part of Spine Toolbox.
# Spine Toolbox is free software: you can redistribute it and/or modify it under the terms of the GNU Lesser General
# Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option)
# any later version. This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY;
# without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU Lesser General
# Public License for more details. You should have received a copy of the GNU Lesser General Public License along with
# this program. If not, see <http://www.gnu.org/licenses/>.
######################################################################################################################
"""
Contains undo and redo commands for Import editor.

:author: A. Soininen (VTT)
:date:   4.8.2020
"""
from enum import auto, IntEnum, unique
from PySide2.QtCore import Qt
from PySide2.QtWidgets import QUndoCommand


@unique
class _Id(IntEnum):
    SET_OPTION = auto()


class PasteMappings(QUndoCommand):
    """Command to paste copied mappings"""

    def __init__(self, import_editor_window, source_table_name, copied_mappings, previous_mappings):
        """
        Args:
            import_editor_window (ImportEditorWindow): import editor window
            source_table_name (src): name of the target source table
            copied_mappings (Iterable): mappings to paste
            previous_mappings (Iterable): mappings before pasting
        """
        text = "paste mappings"
        super().__init__(text)
        self._import_editor_window = import_editor_window
        self._source_table_name = source_table_name
        self._mappings = copied_mappings
        self._previous_mappings = previous_mappings

    def redo(self):
        """Pastes the copied mappings"""
        self._import_editor_window.paste_mappings(self._source_table_name, self._mappings)

    def undo(self):
        """Restores mappings to their previous state."""
        self._import_editor_window.paste_mappings(self._source_table_name, self._previous_mappings)


class PasteOptions(QUndoCommand):
    """Command to paste copied mapping options."""

    def __init__(self, import_sources, source_table_name, copied_options, previous_options):
        """
        Args:
            import_sources (ImportSources): import editor
            source_table_name (src): name of the target source table
            copied_options (dict): options from the internal clipboard
            previous_options (dict): previous options
        """
        text = "paste options"
        super().__init__(text)
        self._import_sources = import_sources
        self._source_table_name = source_table_name
        self._options = copied_options
        self._previous_options = previous_options

    def redo(self):
        """Pastes the options."""
        self._import_sources.paste_options(self._source_table_name, self._options)

    def undo(self):
        """Restores the options to their previous values."""


class SetTableChecked(QUndoCommand):
    """Command to change a source table's checked state."""

    def __init__(self, table_name, table_list_model, checked, *rows):
        """
        Args:
            table_name (str): source table name
            table_list_model (SourceTableListModel): source table model
            checked (bool): new checked state
            rows (int): table row on the list
        """
        text = ("select" if checked else "deselect") + f" '{table_name}'"
        super().__init__(text)
        self._model = table_list_model
        self._rows = rows
        self._checked = checked

    def redo(self):
        """Changes the checked state."""
        self._model.set_checked(self._checked, *self._rows)

    def undo(self):
        """Restores the previous checked state."""
        self._model.set_checked(not self._checked, *self._rows)


class UpdateTableItem(QUndoCommand):
    """Command to update table name and state in file-less mode."""

    def __init__(self, table_list_model, row, old_item, new_item, is_empty_row):
        """
        Args:
            table_list_model (SourceTableListModel): source table model
            row (int): table row on the list
            old_item (dict): old item dictionary
            new_item (dict): new item dictionary
        """
        text = "rename table" if not is_empty_row else "add table"
        super().__init__(text)
        self._model = table_list_model
        self._row = row
        self._old_item = old_item
        self._new_item = new_item
        self._is_empty_row = is_empty_row

    def redo(self):
        self._model.update_item(self._row, self._new_item, add_empty_row=self._is_empty_row)

    def undo(self):
        self._model.update_item(self._row, self._old_item, remove_empty_row=self._is_empty_row)


class SetComponentMappingType(QUndoCommand):
    """Sets the type of a component mapping."""

    def __init__(
        self, component_display_name, mapping_specification_model, mapping_type, previous_type, previous_reference
    ):
        """
        Args:
            component_display_name (str): component name on the mapping specification table
            mapping_specification_model (MappingSpecificationModel): specification model
            mapping_type (str): name of the new type
            previous_type (str): name of the original type
            previous_reference (str or int): original mapping's reference
        """
        text = "change source mapping"
        super().__init__(text)
        self._model = mapping_specification_model
        self._component_display_name = component_display_name
        self._new_type = mapping_type
        self._previous_type = previous_type
        self._previous_reference = previous_reference
        if self._new_type == self._previous_type:
            self.setObsolete(True)

    def redo(self):
        """Changes a component mapping's type."""
        self._model.set_type(self._component_display_name, self._new_type)

    def undo(self):
        """Restores component mapping's original type."""
        self._model.set_type(self._component_display_name, self._previous_type)
        self._model.set_reference(self._component_display_name, self._previous_type, self._previous_reference)


class SetComponentMappingReference(QUndoCommand):
    """Sets the reference for a component mapping."""

    def __init__(
        self,
        component_display_name,
        mapping_specification_model,
        new_type,
        new_reference,
        previous_type,
        previous_reference,
    ):
        """
        Args:
            component_display_name (str): component name on the mapping specification table
            mapping_specification_model (MappingSpecificationModel): specification model
            new_type (str): new mapping 'type'
            new_reference (str or int): new value for the reference
            previous_type (str): original mapping 'type'
            previous_reference (str or int): reference's original value
        """
        text = "change source mapping reference"
        super().__init__(text)
        self._model = mapping_specification_model
        self._component_display_name = component_display_name
        self._new_type = new_type
        self._new_reference = new_reference
        self._previous_type = previous_type
        self._previous_reference = previous_reference
        if self._new_reference == self._previous_reference:
            self.setObsolete(True)

    def redo(self):
        """Sets the reference's value."""
        self._model.set_reference(self._component_display_name, self._new_type, self._new_reference)

    def undo(self):
        """Restores the reference's value and, if necessary, mapping type to their original values."""
        if self._previous_type == "None":
            self._model.set_type(self._component_display_name, "None")
        else:
            self._model.set_reference(self._component_display_name, self._previous_type, self._previous_reference)


class SetConnectorOption(QUndoCommand):
    """Command to set a :class:`ConnectorManager` option."""

    def __init__(self, source_table, option_key, options_widget, value, previous_value):
        """
        Args:
            source_table (str): source table name
            option_key (str): option's key
            options_widget (OptionsWidget): connector options widget
            value (str or int or bool): option's new value
            previous_value (str or int or bool): option's previous value
        """
        text = f"change {option_key}"
        super().__init__(text)
        self._source_table = source_table
        self._option_key = option_key
        self._options_widget = options_widget
        self._value = value
        self._previous_value = previous_value

    def id(self):
        """
        This command's id.

        Returns:
            int: id
        """
        return _Id.SET_OPTION

    def mergeWith(self, command):
        """
        Merges command with another :class:`SetConnectorOption`.

        Args:
            command (QUndoCommand): a command to merge with

        Returns:
            bool: True if merge was successful, False otherwise
        """
        if not isinstance(command, SetConnectorOption):
            return False
        return command._option_key == self._option_key and command._value == self._value

    def redo(self):
        """Changes the connector's option."""
        self._options_widget.set_option_without_undo(self._source_table, self._option_key, self._value)

    def undo(self):
        """Restores the option back to its original value."""
        self._options_widget.set_option_without_undo(self._source_table, self._option_key, self._previous_value)


class CreateMapping(QUndoCommand):
    """Creates a new mapping."""

    def __init__(self, source_table_name, import_mappings, row):
        """
        Args:
            source_table_name (src): source table name
            import_mappings (ImportMappings): mappings manager
            row (int): row where the new mapping should be created
        """
        text = "new mapping"
        super().__init__(text)
        self._source_table_name = source_table_name
        self._import_mappings = import_mappings
        self._mapping_name = None
        self._row = row
        self._stored_mapping_specification = None

    def redo(self):
        """Creates a new mapping at the given row in mappings list."""
        if self._mapping_name is None:
            self._mapping_name = self._import_mappings.create_mapping()
        else:
            self._import_mappings.insert_mapping(
                self._source_table_name, self._mapping_name, self._row, self._stored_mapping_specification
            )

    def undo(self):
        """Deletes the created mapping."""
        self._stored_mapping_specification = self._import_mappings.delete_mapping(
            self._source_table_name, self._mapping_name
        )


class DuplicateMapping(QUndoCommand):
    """Duplicates an existing mapping."""

    def __init__(self, source_table_name, import_mappings, row):
        """
        Args:
            source_table_name (src): source table name
            import_mappings (ImportMappings): mappings manager
            row (int): row where the new mapping should be created
        """
        text = "duplicate mapping"
        super().__init__(text)
        self._source_table_name = source_table_name
        self._import_mappings = import_mappings
        self._mapping_name = None
        self._row = row
        self._stored_mapping_specification = None

    def redo(self):
        """Creates a new mapping at the given row in mappings list."""
        if self._mapping_name is None:
            self._mapping_name = self._import_mappings.duplicate_mapping(self._source_table_name, self._row)
        else:
            self._import_mappings.insert_mapping(
                self._source_table_name, self._mapping_name, self._row + 1, self._stored_mapping_specification
            )

    def undo(self):
        """Deletes the created mapping."""
        self._stored_mapping_specification = self._import_mappings.delete_mapping(
            self._source_table_name, self._mapping_name
        )


class DeleteMapping(QUndoCommand):
    """Command to delete a mapping."""

    def __init__(self, source_table_name, import_mappings, mapping_name, row):
        """
        Args:
            source_table_name (src): source table name
            import_mappings (ImportMappings): mappings manager
            mapping_name (str): name of the mapping to delete
            row (int): mapping's row in the mapping list
        """
        text = "delete mapping"
        super().__init__(text)
        self._source_table_name = source_table_name
        self._import_mappings = import_mappings
        self._mapping_name = mapping_name
        self._row = row
        self._stored_mapping_specification = None

    def redo(self):
        """Deletes the mapping."""
        self._stored_mapping_specification = self._import_mappings.delete_mapping(
            self._source_table_name, self._mapping_name
        )

    def undo(self):
        """Restores the deleted mapping."""
        self._import_mappings.insert_mapping(
            self._source_table_name, self._mapping_name, self._row, self._stored_mapping_specification
        )


class SetItemMappingType(QUndoCommand):
    """Command to change item mapping's type."""

    def __init__(self, source_table_name, mapping_specification_name, options_widget, new_type, previous_mapping):
        """
        Args:
            source_table_name (src): name of the source table
            mapping_specification_name (str): name of the mapping
            options_widget (ImportMappingOptions): options widget
            new_type (str): name of the new mapping type
            previous_mapping (ItemMappingBase): the previous mapping
        """
        text = "mapping type change"
        super().__init__(text)
        self._source_table_name = source_table_name
        self._mapping_specification_name = mapping_specification_name
        self._options_widget = options_widget
        self._new_type = new_type
        self._previous_mapping = previous_mapping

    def redo(self):
        """Sets the mapping type to its new value."""
        self._options_widget.set_item_mapping_type(
            self._source_table_name, self._mapping_specification_name, self._new_type
        )

    def undo(self):
        """Resets the mapping type to its former value."""
        self._options_widget.set_item_mapping(
            self._source_table_name, self._mapping_specification_name, self._previous_mapping
        )


class SetImportObjectsFlag(QUndoCommand):
    """Command to set item mapping's import objects flag."""

    def __init__(self, source_table_name, mapping_specification_name, options_widget, import_objects):
        """
        Args:
            source_table_name (str): name of the source table
            mapping_specification_name (str): name of the mapping specification
            options_widget (ImportMappingOptions): options widget
            import_objects (bool): new flag value
        """
        text = "import objects flag change"
        super().__init__(text)
        self._source_table_name = source_table_name
        self._mapping_specification_name = mapping_specification_name
        self._options_widget = options_widget
        self._import_objects = import_objects

    def redo(self):
        """Changes the import objects flag."""
        self._options_widget.set_import_objects_flag(
            self._source_table_name, self._mapping_specification_name, self._import_objects
        )

    def undo(self):
        """Restores the import objects flag."""
        self._options_widget.set_import_objects_flag(
            self._source_table_name, self._mapping_specification_name, not self._import_objects
        )


class SetParameterType(QUndoCommand):
    """Command to change the parameter type of an item mapping."""

    def __init__(
        self, source_table_name, mapping_specification_name, options_widget, new_type, previous_parameter_mapping
    ):
        """
        Args:
            source_table_name (str): name of the source table
            mapping_specification_name (str): name of the mapping specification
            options_widget (ImportMappingOptions): options widget
            new_type (str): name of the new parameter type
            previous_parameter_mapping (ImportMapping): previous parameter mapping
        """
        text = "parameter type change"
        super().__init__(text)
        self._source_table_name = source_table_name
        self._mapping_specification_name = mapping_specification_name
        self._options_widget = options_widget
        self._new_type = new_type
        self._previous_parameter_mapping = previous_parameter_mapping

    def redo(self):
        """Changes a parameter's type."""
        self._options_widget.set_parameter_type(
            self._source_table_name, self._mapping_specification_name, self._new_type
        )

    def undo(self):
        """Restores a parameter to its previous type"""
        self._options_widget.set_parameter_mapping(
            self._source_table_name, self._mapping_specification_name, self._previous_parameter_mapping
        )


class SetValueType(QUndoCommand):
    """Command to change the value type of an item mapping."""

    def __init__(self, source_table_name, mapping_specification_name, options_widget, new_type, old_type):
        """
        Args:
            source_table_name (str): name of the source table
            mapping_specification_name (str): name of the mapping specification
            options_widget (ImportMappingOptions): options widget
            new_type (str): name of the new value type
            old_type (str): name of the old value type
        """
        text = "value type change"
        super().__init__(text)
        self._source_table_name = source_table_name
        self._mapping_specification_name = mapping_specification_name
        self._options_widget = options_widget
        self._new_type = new_type
        self._old_type = old_type

    def redo(self):
        """Changes a parameter's value type."""
        self._options_widget.set_value_type(self._source_table_name, self._mapping_specification_name, self._new_type)

    def undo(self):
        """Restores a parameter to its previous value type"""
        self._options_widget.set_value_type(self._source_table_name, self._mapping_specification_name, self._old_type)


class SetSkipColumns(QUndoCommand):
    """Command to change item mapping's skip columns option."""

    def __init__(self, source_table_name, mapping_spec_name, options_widget, skip_cols, previous_skip_cols):
        """
        Args:
            source_table_name (str): name of the source table
            mapping_spec_name (str): name of the mapping specification
            options_widget (ImportMappingOptions): options widget
            skip_cols (list): new skip columns
            previous_skip_cols (list): previous skip columns
        """
        text = "mapping ignore columns change"
        super().__init__(text)
        self._source_table_name = source_table_name
        self._mapping_spec_name = mapping_spec_name
        self._options_widget = options_widget
        self._skip_cols = skip_cols
        self._previous_skip_cols = previous_skip_cols

    def redo(self):
        """Changes item mapping's skip columns to a new value."""
        self._options_widget.set_skip_columns(self._source_table_name, self._mapping_spec_name, self._skip_cols)

    def undo(self):
        """Restores item mapping's skip columns to its previous value."""
        self._options_widget.set_skip_columns(
            self._source_table_name, self._mapping_spec_name, self._previous_skip_cols
        )


class SetReadStartRow(QUndoCommand):
    """Command to change item mapping's read start row option."""

    def __init__(self, source_table_name, mapping_specification_name, options_widget, start_row, previous_start_row):
        """
        Args:
            source_table_name (str): name of the source table
            mapping_specification_name (str): name of the mapping specification
            options_widget (ImportMappingOptions): options widget
            start_row (int): new read start row
            previous_start_row (int): previous read start row value
        """
        text = "mapping read start row change"
        super().__init__(text)
        self._source_table_name = source_table_name
        self._mapping_specification_name = mapping_specification_name
        self._options_widget = options_widget
        self._start_row = start_row
        self._previous_start_row = previous_start_row

    def redo(self):
        """Changes item mapping's read start row to a new value."""
        self._options_widget.set_read_start_row(
            self._source_table_name, self._mapping_specification_name, self._start_row
        )

    def undo(self):
        """Restores item mapping's read start row to its previous value."""
        self._options_widget.set_read_start_row(
            self._source_table_name, self._mapping_specification_name, self._previous_start_row
        )


class SetItemMappingDimensionCount(QUndoCommand):
    """Command to change item mapping's dimension option."""

    def __init__(
        self, source_table_name, mapping_specification_name, options_widget, dimension_count, previous_dimension_count
    ):
        """
        Args:
            source_table_name (str): name of the source table
            mapping_specification_name (str): name of the mapping specification
            options_widget (ImportMappingOptions): options widget
            dimension_count (int): new dimension count
            previous_dimension_count (int): previous dimension count
        """
        text = "mapping dimension count change"
        super().__init__(text)
        self._source_table_name = source_table_name
        self._mapping_specification_name = mapping_specification_name
        self._options_widget = options_widget
        self._dimension_count = dimension_count
        self._previous_dimension_count = previous_dimension_count
        self._cls_mappings = []
        self._obj_mappings = []

    def redo(self):
        """Changes the item mapping's dimension to the new value."""
        self._cls_mappings, self._obj_mappings = self._options_widget.set_dimension_count(
            self._source_table_name, self._mapping_specification_name, self._dimension_count
        )

    def undo(self):
        """Changes the item mapping's dimension to its previous value."""
        if self._cls_mappings or self._obj_mappings:
            self._options_widget.restore_relationship_mappings(
                self._source_table_name, self._mapping_specification_name, self._cls_mappings, self._obj_mappings
            )
        else:
            self._options_widget.set_dimension_count(
                self._source_table_name, self._mapping_specification_name, self._previous_dimension_count
            )


class SetTimeSeriesRepeatFlag(QUndoCommand):
    """Command to change the repeat flag for time series."""

    def __init__(self, source_table_name, mapping_specification_name, options_widget, repeat):
        """
        Args:
            source_table_name (str): name of the source table
            mapping_specification_name (str): name of the mapping specification
            options_widget (ImportMappingOptions): options widget
            repeat (bool): new repeat flag value
        """
        text = "change time series repeat flag"
        super().__init__(text)
        self._source_table_name = source_table_name
        self._mapping_specification_name = mapping_specification_name
        self._options_widget = options_widget
        self._repeat = repeat

    def redo(self):
        """Sets the repeat flag to given value."""
        self._options_widget.set_time_series_repeat_flag(
            self._source_table_name, self._mapping_specification_name, self._repeat
        )

    def undo(self):
        """Restores the repeat flag to its previous value."""
        self._options_widget.set_time_series_repeat_flag(
            self._source_table_name, self._mapping_specification_name, not self._repeat
        )


class SetMapDimensionCount(QUndoCommand):
    """Command to change the dimension_count of a Map parameter value type."""

    def __init__(
        self, source_table_name, mapping_specification_name, options_widget, dimension_count, previous_dimension_count
    ):
        """
        Args:
            source_table_name (str): name of the source table
            mapping_specification_name (str): name of the mapping specification
            options_widget (ImportMappingOptions): options widget
            dimension_count (int): new dimension_count
            previous_dimension_count (int): previous dimension_count
        """
        text = "map dimension count change"
        super().__init__(text)
        self._source_table_name = source_table_name
        self._mapping_specification_name = mapping_specification_name
        self._options_widget = options_widget
        self._dimension_count = dimension_count
        self._previous_dimension_count = previous_dimension_count
        self._removed_mappings = []

    def redo(self):
        """Sets the Map dimension_count to the new value."""
        self._removed_mappings = self._options_widget.set_map_dimension_count(
            self._source_table_name, self._mapping_specification_name, self._dimension_count
        )

    def undo(self):
        """Restores the previous Map dimension_count value."""
        if self._removed_mappings:
            self._options_widget.restore_index_mappings(
                self._source_table_name, self._mapping_specification_name, self._removed_mappings
            )
        else:
            self._options_widget.set_map_dimension_count(
                self._source_table_name, self._mapping_specification_name, self._previous_dimension_count
            )


class SetMapCompressFlag(QUndoCommand):
    """Command to change the Map compress flag."""

    def __init__(self, source_table_name, mapping_specification_name, options_widget, compress):
        """
        Args:
            source_table_name (str): name of the source table
            mapping_specification_name (str): name of the mapping specification
            options_widget (ImportMappingOptions): options widget
            compress (bool): compress flag value
        """
        text = ("enable" if compress else "disable") + " Map compression"
        super().__init__(text)
        self._source_table_name = source_table_name
        self._mapping_specification_name = mapping_specification_name
        self._options_widget = options_widget
        self._compress = compress

    def redo(self):
        """Sets the compress flag."""
        self._options_widget.set_map_compress(self._source_table_name, self._mapping_specification_name, self._compress)

    def undo(self):
        """Resets the compress flag to previous value."""
        self._options_widget.set_map_compress(
            self._source_table_name, self._mapping_specification_name, not self._compress
        )


class SetColumnOrRowType(QUndoCommand):
    """Command to change the type of columns or rows."""

    def __init__(self, source_table_name, header_widget, sections, new_type, previous_type):
        """
        Args:
            source_table_name (src): name of the source table
            header_widget (HeaderWithButton): widget of origin
            sections (Iterable of int): row or column indexes
            new_type (ConvertSpec): conversion specification for the rows/columns
            previous_type (ConvertSpec): previous conversion specification for the rows/columns
        """
        text = ("row" if header_widget.orientation() == Qt.Vertical else "column") + " type change"
        super().__init__(text)
        self._source_table_name = source_table_name
        self._header_widget = header_widget
        self._sections = sections
        self._new_type = new_type
        self._previous_type = previous_type

    def redo(self):
        """Sets column/row type."""
        self._header_widget.set_data_types(self._source_table_name, self._sections, self._new_type)

    def undo(self):
        """Restores column/row type to its previous value."""
        self._header_widget.set_data_types(self._source_table_name, self._sections, self._previous_type)


class RestoreMappingsFromDict(QUndoCommand):
    """Restores mappings from a dict."""

    def __init__(self, import_sources, mapping_dict):
        """
        Args:
            import_sources (ImportSources): import editor
            mapping_dict (dict): mappings to
        """
        super().__init__("import mappings")
        self._import_sources = import_sources
        self._mapping_dict = mapping_dict
        self._previous_mapping_dict = import_sources.get_mapping_dict()

    def redo(self):
        """Restores the mappings."""
        self._import_sources.import_mappings(self._mapping_dict)

    def undo(self):
        """Reverts back to previous mappings."""
        self._import_sources.import_mappings(self._previous_mapping_dict)
