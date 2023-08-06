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
Contains ToolInstance class.

:authors: P. Savolainen (VTT), E. Rinne (VTT)
:date:   1.2.2018
"""

import os
import sys
import shutil
from spine_engine.utils.helpers import (
    resolve_python_interpreter,
    resolve_julia_executable,
    resolve_gams_executable,
    resolve_conda_executable,
)
from spine_engine.execution_managers.kernel_execution_manager import KernelExecutionManager
from spine_engine.execution_managers.process_execution_manager import ProcessExecutionManager
from spine_engine.execution_managers.persistent_execution_manager import (
    JuliaPersistentExecutionManager,
    PythonPersistentExecutionManager,
)


class ToolInstance:
    """Tool instance base class."""

    def __init__(self, tool_specification, basedir, settings, logger, owner):
        """

        Args:
            tool_specification (ToolSpecification): the tool specification for this instance
            basedir (str): the path to the directory where this instance should run
            settings (QSettings): Toolbox settings
            logger (LoggerInterface): a logger instance
            owner (ExecutableItemBase): The item that owns the instance
        """
        self.tool_specification = tool_specification
        self.basedir = basedir
        self._settings = settings
        self._logger = logger
        self._owner = owner
        self.exec_mngr = None
        self.program = None  # Program to start in the subprocess
        self.args = list()  # List of command line arguments for the program

    @property
    def owner(self):
        return self._owner

    def is_running(self):
        return self.exec_mngr is not None

    def terminate_instance(self):
        """Terminates Tool instance execution."""
        if not self.exec_mngr:
            return
        self.exec_mngr.stop_execution()
        self.exec_mngr = None

    def remove(self):
        """[Obsolete] Removes Tool instance files from work directory."""
        shutil.rmtree(self.basedir, ignore_errors=True)

    def prepare(self, args):
        """Prepares this instance for execution.

        Implement in subclasses to perform specific initialization.

        Args:
            args (list): Tool cmd line args
            k_spec_dict (dict): Kernel spec name and related settings
        """
        raise NotImplementedError()

    def execute(self):
        """Executes a prepared instance. Implement in subclasses."""
        raise NotImplementedError()

    def append_cmdline_args(self, tool_args):
        """
        Appends Tool specification command line args into instance args list.

        Args:
            tool_args (list): List of Tool cmd line args
        """
        self.args += self.tool_specification.cmdline_args
        if tool_args:
            self.args += tool_args


class GAMSToolInstance(ToolInstance):
    """Class for GAMS Tool instances."""

    def prepare(self, args):
        """See base class."""
        gams_path = self._settings.value("appSettings/gamsPath", defaultValue="")
        self.program = resolve_gams_executable(gams_path)
        self.args.append(self.tool_specification.main_prgm)
        self.args.append("curDir=")
        self.args.append(self.basedir)
        self.args.append("logoption=3")  # TODO: This should be an option in Settings
        self.append_cmdline_args(args)
        # TODO: Check if the below sets the curDir argument. Is the curDir arg now useless?
        self.exec_mngr = ProcessExecutionManager(self._logger, self.program, *self.args, workdir=self.basedir)

    def execute(self):
        """Executes a prepared instance."""
        ret = self.exec_mngr.run_until_complete()
        if ret != 0:
            try:
                return_msg = self.tool_specification.return_codes[ret]
                self._logger.msg_error.emit(f"\t<b>{return_msg}</b> [exit code:{ret}]")
            except KeyError:
                self._logger.msg_error.emit(f"\tUnknown return code ({ret})")
        self.exec_mngr = None
        return ret


class JuliaToolInstance(ToolInstance):
    """Class for Julia Tool instances."""

    def prepare(self, args):
        """See base class."""
        sysimage = self._owner.options.get("julia_sysimage", "")
        use_julia_kernel = self._settings.value("appSettings/useJuliaKernel", defaultValue="2")
        # Prepare args
        mod_work_dir = repr(self.basedir).strip("'")
        self.args = [f'cd("{mod_work_dir}");']
        cmdline_args = self.tool_specification.cmdline_args + args
        if cmdline_args:
            fmt_cmdline_args = '["' + repr('", "'.join(cmdline_args)).strip("'") + '"]'
            self.args += [f"empty!(ARGS); append!(ARGS, {fmt_cmdline_args});"]
        self.args += [f'include("{self.tool_specification.main_prgm}")']
        if use_julia_kernel == "2":
            kernel_name = self._settings.value("appSettings/juliaKernel", defaultValue="")
            extra_switches = [f"--sysimage={sysimage}"] if os.path.isfile(sysimage) else None
            self.exec_mngr = KernelExecutionManager(
                self._logger, kernel_name, *self.args, group_id=self.owner.group_id, extra_switches=extra_switches
            )
        else:
            julia_exe = self._settings.value("appSettings/juliaPath", defaultValue="")
            julia_exe = resolve_julia_executable(julia_exe)
            julia_project_path = self._settings.value("appSettings/juliaProjectPath", defaultValue="")
            self.program = [julia_exe]
            self.program.append(f"--project={julia_project_path}")
            if os.path.isfile(sysimage):
                self.program.append(f"--sysimage={sysimage}")
            alias = f"# Running 'julia {' '.join([self.tool_specification.main_prgm, *cmdline_args])}'"
            self.exec_mngr = JuliaPersistentExecutionManager(
                self._logger, self.program, self.args, alias, group_id=self.owner.group_id
            )
        # FIXME: script-less tools?

    def execute(self):
        """Executes a prepared instance."""
        ret = self.exec_mngr.run_until_complete()
        if ret != 0:
            try:
                return_msg = self.tool_specification.return_codes[ret]
                self._logger.msg_error.emit(f"\t<b>{return_msg}</b> [exit code:{ret}]")
            except KeyError:
                self._logger.msg_error.emit(f"\tUnknown return code ({ret})")
        self.exec_mngr = None
        return ret


class PythonToolInstance(ToolInstance):
    """Class for Python Tool instances."""

    def prepare(self, args):
        """See base class."""
        self.tool_specification.set_execution_settings()  # Set default execution settings
        use_jupyter_console = self.tool_specification.execution_settings["use_jupyter_console"]
        if use_jupyter_console:
            # Prepare command
            cd_command = f"%cd -q {self.basedir}"  # -q: quiet
            main_command = f'%run "{self.tool_specification.main_prgm}"'
            cmdline_args = self.tool_specification.cmdline_args + args
            if cmdline_args:
                main_command += " " + '"' + '" "'.join(cmdline_args) + '"'
            self.args = [cd_command, main_command]
            conda_exe = self._settings.value("appSettings/condaPath", defaultValue="")
            conda_exe = resolve_conda_executable(conda_exe)
            k_spec = self.tool_specification.execution_settings["kernel_spec_name"]
            env = self.tool_specification.execution_settings["env"]  # Activate environment if "conda"
            self.exec_mngr = KernelExecutionManager(
                self._logger, k_spec, *self.args, group_id=self.owner.group_id, environment=env, conda_exe=conda_exe
            )
        else:
            python_exe = self.tool_specification.execution_settings["executable"]
            python_exe = resolve_python_interpreter(python_exe)
            self.program = [python_exe]
            fp = self.tool_specification.main_prgm
            full_fp = os.path.join(self.basedir, self.tool_specification.main_prgm).replace(os.sep, "/")
            cmdline_args = [full_fp] + self.tool_specification.cmdline_args + args
            fmt_cmdline_args = '["' + repr('", "'.join(cmdline_args)).strip("'") + '"]'
            self.args += [f"import sys; sys.argv = {fmt_cmdline_args};"]
            self.args += [f"import os; os.chdir({repr(self.basedir)})"]
            exec_code = self._make_exec_code(fp, full_fp)
            self.args += [exec_code]
            alias = f"# Running 'python {' '.join([self.tool_specification.main_prgm, *cmdline_args[1:]])}'"
            self.exec_mngr = PythonPersistentExecutionManager(
                self._logger, self.program, self.args, alias, group_id=self.owner.group_id
            )

    def _make_exec_code(self, fp, full_fp):
        """Returns a string of code to run this tool instance in a python interactive session."""
        glob = f'{{"__file__": "{full_fp}", "__name__": "__main__"}}'
        return f"with open('{fp}', 'rb') as f: exec(compile(f.read(), '{fp}', 'exec'), {glob}, locals())"

    def execute(self):
        """Executes a prepared instance."""
        ret = self.exec_mngr.run_until_complete()
        if ret != 0:
            try:
                return_msg = self.tool_specification.return_codes[ret]
                self._logger.msg_error.emit(f"\t<b>{return_msg}</b> [exit code:{ret}]")
            except KeyError:
                self._logger.msg_error.emit(f"\tUnknown return code ({ret})")
        self.exec_mngr = None
        return ret


class ExecutableToolInstance(ToolInstance):
    """Class for Executable Tool instances."""

    def prepare(self, args):
        """See base class."""
        batch_path = os.path.join(self.basedir, self.tool_specification.main_prgm)
        if sys.platform != "win32":
            self.program = "sh"
            self.args.append(batch_path)
        else:
            self.program = batch_path
        self.append_cmdline_args(args)
        self.exec_mngr = ProcessExecutionManager(self._logger, self.program, *self.args, workdir=self.basedir)

    def execute(self):
        """Executes a prepared instance."""
        ret = self.exec_mngr.run_until_complete()
        if ret != 0:
            try:
                return_msg = self.tool_specification.return_codes[ret]
                self._logger.msg_error.emit(f"\t<b>{return_msg}</b> [exit code:{ret}]")
            except KeyError:
                self._logger.msg_error.emit(f"\tUnknown return code ({ret})")
        self.exec_mngr = None
        return ret
