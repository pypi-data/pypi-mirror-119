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
Contains Tool specification classes.

:authors: P. Savolainen (VTT), E. Rinne (VTT), M. Marin (KTH)
:date:   24.1.2018
"""

from collections import OrderedDict
import copy
import logging
import os.path
import json
from spine_engine.project_item.project_item_specification import ProjectItemSpecification
from spine_engine.utils.command_line_arguments import split_cmdline_args
from .item_info import ItemInfo
from .tool_instance import GAMSToolInstance, JuliaToolInstance, PythonToolInstance, ExecutableToolInstance


# Tool types
TOOL_TYPES = ["Julia", "Python", "GAMS", "Executable"]

# Required and optional keywords for Tool specification dictionaries
REQUIRED_KEYS = ["name", "tooltype", "includes"]
OPTIONAL_KEYS = [
    "description",
    "short_name",
    "inputfiles",
    "inputfiles_opt",
    "outputfiles",
    "cmdline_args",
    "execute_in_work",
    "execution_settings",
]
LIST_REQUIRED_KEYS = ["includes", "inputfiles", "inputfiles_opt", "outputfiles"]  # These should be lists


def make_specification(definition, app_settings, logger):
    """De-serializes and constructs a tool specification from definition.

    Args:
        definition (dict): a dictionary containing the serialized specification.
        app_settings (QSettings): Toolbox settings
        logger (LoggerInterface): a logger

    Returns:
        ToolSpecification: a tool specification constructed from the given definition,
            or None if there was an error
    """
    definition["includes_main_path"] = path = definition.setdefault("includes_main_path", ".").replace("/", os.path.sep)
    if not os.path.isabs(path):
        definition_file_path = definition["definition_file_path"]
        path = os.path.normpath(os.path.join(os.path.dirname(definition_file_path), path))
    definition["includes"] = [src_file.replace("/", os.path.sep) for src_file in definition["includes"]]
    try:
        _tooltype = definition["tooltype"].lower()
    except KeyError:
        logger.msg_error.emit(
            "No tool type defined in tool definition file. Supported types "
            "are 'python', 'gams', 'julia' and 'executable'"
        )
        return None
    if _tooltype == "julia":
        spec = JuliaTool.load(path, definition, app_settings, logger)
    elif _tooltype == "python":
        spec = PythonTool.load(path, definition, app_settings, logger)
    elif _tooltype == "gams":
        spec = GAMSTool.load(path, definition, app_settings, logger)
    elif _tooltype == "executable":
        spec = ExecutableTool.load(path, definition, app_settings, logger)
    else:
        logger.msg_warning.emit(f"Tool type <b>{_tooltype}</b> not available")
        return None
    return spec


class ToolSpecification(ProjectItemSpecification):
    """Super class for all tool specifications."""

    def __init__(
        self,
        name,
        tooltype,
        path,
        includes,
        settings,
        logger,
        description=None,
        inputfiles=None,
        inputfiles_opt=None,
        outputfiles=None,
        cmdline_args=None,
        execute_in_work=True,
    ):
        """

        Args:
            name (str): Tool specification name
            tooltype (str): Type of Tool (e.g. Python, Julia, ..)
            path (str): Path to Tool specification
            includes (list): List of files belonging to the tool specification (relative to 'path')
            settings (QSettings): Toolbox settings
            logger (LoggerInterface): a logger instance
            description (str): Description of the Tool specification
            inputfiles (list): List of required data files
            inputfiles_opt (list, optional): List of optional data files (wildcards may be used)
            outputfiles (list, optional): List of output files (wildcards may be used)
            cmdline_args (str, optional): Tool command line arguments (read from tool definition file)
            execute_in_work (bool): Execute in work folder
        """
        super().__init__(name, description, item_type=ItemInfo.item_type(), item_category=ItemInfo.item_category())
        self._settings = settings
        self._logger = logger
        self.tooltype = tooltype
        self.path = path
        self.includes = includes
        if cmdline_args is not None:
            if isinstance(cmdline_args, str):
                # Old tool spec files may have the command line arguments as plain strings.
                self.cmdline_args = split_cmdline_args(cmdline_args)
            else:
                self.cmdline_args = cmdline_args
        else:
            self.cmdline_args = []
        self.inputfiles = set(inputfiles) if inputfiles else set()
        self.inputfiles_opt = set(inputfiles_opt) if inputfiles_opt else set()
        self.outputfiles = set(outputfiles) if outputfiles else set()
        self.return_codes = {}
        self.execute_in_work = execute_in_work

    def _includes_main_path_relative(self):
        return os.path.relpath(self.path, os.path.dirname(self.definition_file_path)).replace(os.path.sep, "/")

    def clone(self):
        spec_dict = copy.deepcopy(self.to_dict())
        spec_dict["definition_file_path"] = self.definition_file_path
        return make_specification(spec_dict, self._settings, self._logger)

    def to_dict(self):
        return {
            "name": self.name,
            "tooltype": self.tooltype,
            "includes": [src_file.replace(os.path.sep, "/") for src_file in self.includes],
            "description": self.description,
            "inputfiles": list(self.inputfiles),
            "inputfiles_opt": list(self.inputfiles_opt),
            "outputfiles": list(self.outputfiles),
            "cmdline_args": self.cmdline_args,
            "execute_in_work": self.execute_in_work,
            "includes_main_path": self._includes_main_path_relative(),
        }

    def set_execution_settings(self):
        raise NotImplementedError

    def save(self):
        """See base class."""
        definition = self.to_dict()
        with open(self.definition_file_path, "w") as fp:
            try:
                json.dump(definition, fp, indent=4)
                return True
            except ValueError:
                self._logger.msg_error.emit(
                    "Saving Tool specification file failed. Path:{0}".format(self.definition_file_path)
                )
                return False

    def is_equivalent(self, other):
        """See base class."""
        for k, v in other.__dict__.items():
            if k in LIST_REQUIRED_KEYS:
                if set(self.__dict__[k]) != set(v):
                    return False
            else:
                if self.__dict__[k] != v:
                    return False
        return True

    def set_return_code(self, code, description):
        """Sets a return code and an associated text description for the tool specification.

        Args:
            code (int): Return code
            description (str): Description
        """
        self.return_codes[code] = description

    @staticmethod
    def check_definition(data, logger):
        """Checks that a tool specification contains
        the required keys and that it is in correct format.

        Args:
            data (dict): Tool specification
            logger (LoggerInterface): A logger instance

        Returns:
            Dictionary or None if there was a problem in the tool definition.
        """
        kwargs = dict()
        for p in REQUIRED_KEYS + OPTIONAL_KEYS:
            try:
                kwargs[p] = data[p]
            except KeyError:
                if p in REQUIRED_KEYS:
                    logger.msg_error.emit("Required keyword '{0}' missing".format(p))
                    return None
            # Check that some values are lists
            if p in LIST_REQUIRED_KEYS:
                try:
                    if not isinstance(data[p], list):
                        logger.msg_error.emit("Keyword '{0}' value must be a list".format(p))
                        return None
                except KeyError:
                    pass
        return kwargs

    def create_tool_instance(self, basedir, logger, owner):
        """Returns an instance of this tool specification that is configured to run in the given directory.

        Args:
            basedir (str): the path to the directory where the instance will run
            logger (LoggerInterface)
            owner (ExecutableItemBase): The item that owns the instance
        """
        return self.tool_instance_factory(self, basedir, self._settings, logger, owner)

    @property
    def tool_instance_factory(self):
        raise NotImplementedError


class GAMSTool(ToolSpecification):
    """Class for GAMS tool specifications."""

    def __init__(
        self,
        name,
        tooltype,
        path,
        includes,
        settings,
        logger,
        description=None,
        inputfiles=None,
        inputfiles_opt=None,
        outputfiles=None,
        cmdline_args=None,
        execute_in_work=True,
    ):
        """

        Args:
            name (str): GAMS Tool name
            tooltype (str): Tool specification type
            path (str): Path to model main file
            includes (list): List of files belonging to the tool (relative to 'path').  # TODO: Change to src_files
            settings (QSettings): Toolbox settings
            logger (LoggerInterface): a logger instance
            First file in the list is the main GAMS program.
            description (str): GAMS Tool description
            inputfiles (list): List of required data files
            inputfiles_opt (list, optional): List of optional data files (wildcards may be used)
            outputfiles (list, optional): List of output files (wildcards may be used)
            cmdline_args (str, optional): GAMS tool command line arguments (read from tool definition file)
        """
        super().__init__(
            name,
            tooltype,
            path,
            includes,
            settings,
            logger,
            description,
            inputfiles,
            inputfiles_opt,
            outputfiles,
            cmdline_args,
            execute_in_work,
        )
        main_file = includes[0]
        # Add .lst file to list of output files
        self.lst_file = os.path.splitext(main_file)[0] + ".lst"
        self.outputfiles.add(self.lst_file)
        # Split main_prgm to main_dir and main_prgm
        # because GAMS needs to run in the directory of the main program
        # TODO: This does not work because main_file is always just file name
        self.main_dir, self.main_prgm = os.path.split(main_file)
        self.gams_options = OrderedDict()
        self.return_codes = {
            0: "Normal return",
            1: "Solver is to be called the system should never return this number",  # ??
            2: "There was a compilation error",
            3: "There was an execution error",
            4: "System limits were reached",
            5: "There was a file error",
            6: "There was a parameter error",
            7: "There was a licensing error",
            8: "There was a GAMS system error",
            9: "GAMS could not be started",
            10: "Out of memory",
            11: "Out of disk",
            62097: "Simulation interrupted by user",  # Not official
        }

    def update_gams_options(self, key, value):
        """[OBSOLETE?] Updates GAMS command line options. Only 'cerr' and 'logoption' keywords supported.

        Args:
            key (str): Option name
            value (int, float): Option value
        """
        # Supported GAMS logoption values
        # 3 writes LOG output to standard output
        # 4 writes LOG output to a file and standard output  [Not supported in GAMS v24.0]
        if key in ["logoption", "cerr"]:
            self.gams_options[key] = "{0}={1}".format(key, value)
        else:
            logging.error("Updating GAMS options failed. Unknown key: %s", key)

    @staticmethod
    def load(path, data, settings, logger):
        """Creates a GAMSTool according to a tool specification file.

        Args:
            path (str): Base path to tool files
            data (dict): Dictionary of tool definitions
            settings (QSettings): Toolbox settings
            logger (LoggerInterface): A logger instance

        Returns:
            GAMSTool instance or None if there was a problem in the tool specification file.
        """
        kwargs = GAMSTool.check_definition(data, logger)
        if kwargs is not None:
            # Return an executable model instance
            return GAMSTool(path=path, settings=settings, logger=logger, **kwargs)
        return None

    @property
    def tool_instance_factory(self):
        return GAMSToolInstance


class JuliaTool(ToolSpecification):
    """Class for Julia tool specifications."""

    def __init__(
        self,
        name,
        tooltype,
        path,
        includes,
        settings,
        logger,
        description=None,
        inputfiles=None,
        inputfiles_opt=None,
        outputfiles=None,
        cmdline_args=None,
        execute_in_work=True,
    ):
        """
        Args:
            name (str): Julia Tool name
            tooltype (str): Tool specification type
            path (str): Path to model main file
            includes (list): List of files belonging to the tool (relative to 'path').  # TODO: Change to src_files
            First file in the list is the main Julia program.
            settings (QSettings): Toolbox settings
            logger (LoggerInterface): A logger instance
            description (str): Julia Tool description
            inputfiles (list): List of required data files
            inputfiles_opt (list, optional): List of optional data files (wildcards may be used)
            outputfiles (list, optional): List of output files (wildcards may be used)
            cmdline_args (str, optional): Julia tool command line arguments (read from tool definition file)
        """
        super().__init__(
            name,
            tooltype,
            path,
            includes,
            settings,
            logger,
            description,
            inputfiles,
            inputfiles_opt,
            outputfiles,
            cmdline_args,
            execute_in_work,
        )
        main_file = includes[0]
        self.main_dir, self.main_prgm = os.path.split(main_file)
        self.julia_options = OrderedDict()
        self.return_codes = {0: "Normal return", -1: "Failure"}

    @staticmethod
    def load(path, data, settings, logger):
        """Creates a JuliaTool according to a tool specification file.

        Args:
            path (str): Base path to tool files
            data (dict): Dictionary of tool definitions
            settings (QSetting): Toolbox settings
            logger (LoggerInterface): A logger instance

        Returns:
            JuliaTool instance or None if there was a problem in the tool definition file.
        """
        kwargs = JuliaTool.check_definition(data, logger)
        if kwargs is not None:
            # Return an executable model instance
            return JuliaTool(path=path, settings=settings, logger=logger, **kwargs)
        return None

    @property
    def tool_instance_factory(self):
        return JuliaToolInstance


class PythonTool(ToolSpecification):
    """Class for Python tool specifications."""

    def __init__(
        self,
        name,
        tooltype,
        path,
        includes,
        settings,
        logger,
        description=None,
        inputfiles=None,
        inputfiles_opt=None,
        outputfiles=None,
        cmdline_args=None,
        execute_in_work=True,
        execution_settings=None,
    ):
        """
        Args:

            name (str): Python Tool name
            tooltype (str): Tool specification type
            path (str): Path to model main file
            includes (list): List of files belonging to the tool (relative to 'path').  # TODO: Change to src_files
            settings (QSettings): Toolbox settings
            logger (LoggerInterface): A logger instance
            First file in the list is the main Python program.
            description (str): Python Tool description
            inputfiles (list): List of required data files
            inputfiles_opt (list, optional): List of optional data files (wildcards may be used)
            outputfiles (list, optional): List of output files (wildcards may be used)
            cmdline_args (str, optional): Python tool command line arguments (read from tool definition file)
            execution_settings (dict): Python kernel spec settings
        """
        super().__init__(
            name,
            tooltype,
            path,
            includes,
            settings,
            logger,
            description,
            inputfiles,
            inputfiles_opt,
            outputfiles,
            cmdline_args,
            execute_in_work,
        )
        main_file = includes[0]
        self.main_dir, self.main_prgm = os.path.split(main_file)
        self.python_options = OrderedDict()
        self.execution_settings = execution_settings
        self.return_codes = {0: "Normal return", -1: "Failure"}  # Not official

    def to_dict(self):
        """Adds kernel spec settings dict to Tool spec dict."""
        d = super().to_dict()
        d["execution_settings"] = self.execution_settings
        return d

    def set_execution_settings(self):
        """Sets the execution_setting instance attribute to defaults if this
        Python Tool spec has not been updated yet.

        Returns:
            void
        """
        if not self.execution_settings:
            # Use global (default) execution settings from Settings->Tools
            # This part is for providing support for Python Tool specs that do not have
            # the execution_settings dict yet
            d = dict()
            d["kernel_spec_name"] = self._settings.value("appSettings/pythonKernel", defaultValue="")
            d["env"] = ""
            d["use_jupyter_console"] = bool(
                int(self._settings.value("appSettings/usePythonKernel", defaultValue="0"))
            )  # bool(int(str))
            d["executable"] = self._settings.value("appSettings/pythonPath", defaultValue="")
            self.execution_settings = d
        else:
            # Make sure that required keys are included (for debugging)
            if not isinstance(self.execution_settings, dict):
                logging.error("self.execution_settings is not a dict")
                return
            if "use_jupyter_console" not in self.execution_settings.keys():
                logging.error("self.execution_settings error 1")
            elif "kernel_spec_name" not in self.execution_settings.keys():
                logging.error("self.execution_settings error 2")
            elif "env" not in self.execution_settings.keys():
                logging.error("self.execution_settings error 3")
            elif "executable" not in self.execution_settings.keys():
                logging.error("self.execution_settings error 4")

    @staticmethod
    def load(path, data, settings, logger):
        """Creates a PythonTool according to a tool specification file.

        Args:
            path (str): Base path to tool files
            data (dict): Dictionary of tool definitions
            settings (QSettings): Toolbox settings
            logger (LoggerInterface): A logger instance

        Returns:
            PythonTool instance or None if there was a problem in the tool definition file.
        """
        kwargs = PythonTool.check_definition(data, logger)
        if kwargs is not None:
            # Return an executable model instance
            return PythonTool(path=path, settings=settings, logger=logger, **kwargs)
        return None

    @property
    def tool_instance_factory(self):
        return PythonToolInstance


class ExecutableTool(ToolSpecification):
    """Class for Executable tool specifications."""

    def __init__(
        self,
        name,
        tooltype,
        path,
        includes,
        settings,
        logger,
        description=None,
        inputfiles=None,
        inputfiles_opt=None,
        outputfiles=None,
        cmdline_args=None,
        execute_in_work=True,
    ):
        """
        Args:

            name (str): Tool name
            tooltype (str): Tool specification type
            path (str): Path to main script file
            includes (list): List of files belonging to the tool (relative to 'path').  # TODO: Change to src_files
            First file in the list is the main script file.
            settings (QSettings): Toolbox settings
            logger (LoggerInterface): A logger instance
            description (str): Tool description
            inputfiles (list): List of required data files
            inputfiles_opt (list, optional): List of optional data files (wildcards may be used)
            outputfiles (list, optional): List of output files (wildcards may be used)
            cmdline_args (str, optional): Tool command line arguments (read from tool definition file)
        """
        super().__init__(
            name,
            tooltype,
            path,
            includes,
            settings,
            logger,
            description,
            inputfiles,
            inputfiles_opt,
            outputfiles,
            cmdline_args,
            execute_in_work,
        )
        main_file = includes[0]
        # TODO: This does not do anything because main_file is always just file name
        self.main_dir, self.main_prgm = os.path.split(main_file)
        self.options = OrderedDict()
        self.return_codes = {0: "Normal exit", 1: "Error happened"}

    @staticmethod
    def load(path, data, settings, logger):
        """Creates an ExecutableTool according to a tool specification file.

        Args:
            path (str): Base path to tool files
            data (dict): Tool specification
            settings (QSettings): Toolbox settings
            logger (LoggerInterface): A logger instance

        Returns:
            ExecutableTool instance or None if there was a problem in the tool specification.
        """
        kwargs = ExecutableTool.check_definition(data, logger)
        if kwargs is not None:
            # Return an executable model instance
            return ExecutableTool(path=path, settings=settings, logger=logger, **kwargs)
        return None

    @property
    def tool_instance_factory(self):
        return ExecutableToolInstance
