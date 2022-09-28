# -*- coding: utf-8 -*-
"""The Run Manager module

Contains classes and functions used to manage the runs and their tasks.

Routine Listings
----------------

See Also
--------

RunManager : Class to manage runs
TaskManager : Class to manage tasks

Notes
-----

References
----------

Examples
--------

"""

import datetime
import traceback
from pathlib import Path

from lip_pps_run_manager import __version__


def clean_path(path_to_clean: Path) -> Path:
    """Clean a path from dangerous characters

    Some characters are not recommended/supported by a given filesystem.
    To make matters worse, the set of supported characters varies from
    operating system to operating system. In order to make sure this
    code is portable and that things remain compatible, we choose a
    subset of characters on which to limit the paths used. The subset is
    essentially all letters (lower and upper case), all numbers
    augmented with the dot, underscore and dash.

    Parameters
    ----------
    path_to_clean
        The path to the directory to clean

    Raises
    ------
    TypeError
        If the parameter has the wrong type

    Returns
    -------
    Path
        The `path_to_clean` path cleaned of all characters not part of
        the reduced set

    Examples
    --------
    >>> import lip_pps_run_manager.run_manager as RM
    >>> print(RM.clean_path(Path("/tmp/2@#_run")))
    """

    if not isinstance(path_to_clean, Path):
        raise TypeError("The `path_to_clean` must be a Path type object, received object of type {}".format(type(path_to_clean)))

    # SafeCharacters = {
    # 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K',
    # 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V',
    # 'W', 'X', 'Y', 'Z',
    # 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k',
    # 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v',
    # 'w', 'x', 'y', 'z',
    # '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '.',
    # '_', '-'
    # }

    return Path(".")


def run_exists(path_to_directory: Path, run_name: str) -> bool:
    """Check if a given run already exists in a given directory

    Parameters
    ----------
    path_to_directory
        The path to the directory where to check if the run exists

    run_name
        The name of the run to check for

    Raises
    ------
    TypeError
        If either of the parameters has the wrong type

    Returns
    -------
    bool
        `True` if the run already exists, `False` if it does not exist.

    Examples
    --------
    >>> import lip_pps_run_manager.run_manager as RM
    >>> print(RM.run_exists(Path("."), "Run0001"))
    """

    if not isinstance(path_to_directory, Path):
        raise TypeError("The `path_to_directory` must be a Path " "type object, received object of type {}".format(type(path_to_directory)))
    if not isinstance(run_name, str):
        raise TypeError("The `run_name` must be a str " "type object, received object of type {}".format(type(run_name)))

    run_path = path_to_directory / run_name

    # TODO: Add check for invalid characters

    return (run_path / 'run_info.txt').is_file()


def create_run(path_to_directory: Path, run_name: str) -> Path:
    """Create a new run in a given directory

    Parameters
    ----------
    path_to_directory
        The path to the directory where to create the run

    run_name
        The name of the run to create

    Raises
    ------
    TypeError
        If either of the parameters has the wrong type

    RuntimeError
        If the run directory already exists

    Returns
    -------
    Path
        The path to the creaated run.

    Examples
    --------
    >>> import lip_pps_run_manager.run_manager as RM
    >>> print(RM.create_run(Path("."), "Run0001"))
    """

    if not isinstance(path_to_directory, Path):
        raise TypeError("The `path_to_directory` must be a Path " "type object, received object of type {}".format(type(path_to_directory)))
    if not isinstance(run_name, str):
        raise TypeError("The `run_name` must be a str " "type object, received object of type {}".format(type(run_name)))

    run_path = path_to_directory / run_name

    # TODO: Add check for invalid characters

    if run_path.is_dir():
        raise RuntimeError(
            "Unable to create the run '{}' in '{}' because a directory with that name already exists.".format(run_name, path_to_directory)
        )

    run_path.mkdir(parents=True)

    with open(run_path / "run_info.txt", "w") as out_file:
        out_file.write(
            "This directory contains data for the run '{}', created by the RunManager v{} on {}".format(
                run_name, __version__, datetime.datetime.now()
            )
        )

    return run_path


class RunManager:
    """Class to manage PPS Runs

    This Class initializes the on disk structures if necessary.

    Parameters
    ----------
    path_to_run_storage
        The path to the directory where all the run related information
        is stored. Typically, there will be multiple processing
        steps/tasks applied to a single run and each will have its data
        stored in a single subdirectory.

    Attributes
    ----------
    path_directory

    Raises
    ------
    TypeError
        If the parameter has the incorrect type

    Examples
    --------
    >>> import lip_pps_run_manager as RM
    >>> John = RM.RunManager("Run0001")

    """

    _path_directory = Path(".")

    def __init__(self, path_to_run_directory: Path):
        if not isinstance(path_to_run_directory, Path):
            raise TypeError(
                "The `path_to_run_directory` must be a Path " "type object, received object of type {}".format(type(path_to_run_directory))
            )
        self._path_directory = path_to_run_directory

    @property
    def path_directory(self) -> Path:
        """The path directory property getter method

        This method fetches the path_directory internal attribute,
        which contains the path to the directory containing the run
        information for this run.

        Returns
        -------
        Path
            The path to the directory where the run information
            is stored.
        """
        return self._path_directory

    # @path_directory.setter
    # def path_directory(self, value):
    #    """
    #    This is the setter method
    #    where I can check it's not assigned a value < 0
    #    """
    #    self._path_directory = value

    @property
    def run_name(self) -> str:
        """The name of the run"""
        return self._path_directory.parts[-1]

    def create_run(self, raise_error: bool = False):
        """Creates a run where this `RunManager` is pointing to.

        Parameters
        ----------
        raise_error
            If `True` a `RuntimeError` is raised if the run already exists.
            If `False` no error is raised whether the run exists or not.

        Raises
        ------
        RuntimeError
            If the `raise_error` parameter is `True` and the run already
            exists or if the run directory already exists.

        Examples
        --------
        >>> import lip_pps_run_manager as RM
        >>> John = RM.RunManager("Run0001")
        >>> John.create_run(True)

        The above code should create the Run0001 directory if it doesn't
        exist or exit with a `RuntimeError` if it does.

        """
        if run_exists(self.path_directory.parent, self.run_name):
            if raise_error:
                raise RuntimeError(
                    "Can not create run '{}', in '{}' because it already exists.".format(self.run_name, self.path_directory.parent)
                )
        else:
            create_run(path_to_directory=self.path_directory.parent, run_name=self.run_name)

    def handle_task(self, task_name: str, drop_old_data: bool = True, backup_python_file: bool = True):
        """Method that creates a handle to a manager for a specific task

        The `TaskManager` that is created is under the current
        `RunManager`.

        Parameters
        ----------
        task_name
            The name of the task which is going to be processed
        drop_old_data
            If a previous directory with the same name as this tasks
            exists, this flag controls whether that data is removed or
            not. Useful when testing and rerunning multiple times, in
            order to ensure that old data from previous runs is cleaned.
        backup_python_file
            If `True` a copy of the current python file will be backed
            up in the task directory. Useful for keeping a log of
            exactly what was done.

        Raises
        ------
        TypeError
            If any parameter has the incorrect type

        Returns
        -------
        TaskManager
            The `TaskManager` to handle the task.

        Examples
        --------
        >>> import lip_pps_run_manager as RM
        >>> John = RM.RunManager("Run0001")
        >>> John.create_run()
        >>> with John.handle_task("myTask") as taskHandler:
        ...   print("Processing task")

        The above code should create the Run0001 directory and then
        create a subdirectory for the task "myTask".
        """

        if not isinstance(task_name, str):
            raise TypeError("The `task_name` must be a str " "type object, received object of type {}".format(type(task_name)))

        if not isinstance(drop_old_data, bool):
            raise TypeError("The `drop_old_data` must be a bool " "type object, received object of type {}".format(type(drop_old_data)))

        if not isinstance(backup_python_file, bool):
            raise TypeError(
                "The `backup_python_file` must be a bool " "type object, received object of type {}".format(type(backup_python_file))
            )

        script_to_backup = None
        if backup_python_file:
            script_to_backup = Path(traceback.extract_stack()[-2].filename)

        return TaskManager(
            path_to_run=self.path_directory, task_name=task_name, drop_old_data=drop_old_data, script_to_backup=script_to_backup
        )

    def get_task_directory(self, task_name: str) -> Path:
        """Retrieve the `Path` of a given task

        Parameters
        ----------
        task_name
            The name of the task of which to get the path

        Raises
        ------
        TypeError
            If any parameter has the incorrect type

        Returns
        -------
        Path
            The `Path` to the task directory.

        Warnings
        --------
        The returned directory may or may not exist.

        Examples
        --------
        >>> import lip_pps_run_manager as RM
        >>> John = RM.RunManager("Run0001")
        >>> John.create_run()
        >>> with John.handle_task("myTask") as taskHandler:
        ...   print("Processing task")
        >>> John.get_task_directory("myTask")

        The example above is using the with syntax, which will ensure
        the task directory is created.

        """

        if not isinstance(task_name, str):
            raise TypeError("The `task_name` must be a str " "type object, received object of type {}".format(type(task_name)))

        return self.path_directory / task_name


class TaskManager(RunManager):
    _task_name = ""
    _drop_old_data = True
    _script_to_backup = Path("")

    def __init__(self, path_to_run: Path, task_name: str, drop_old_data: bool = True, script_to_backup: Path = None):
        if not run_exists(path_to_directory=path_to_run.parent, run_name=path_to_run.parts[-1]):
            raise ValueError("The 'path_to_run' ({}) does not look like the directory of a run...".format(path_to_run))

        super().__init__(path_to_run_directory=path_to_run)
        self._task_name = task_name
        self._drop_old_data = drop_old_data
        self._script_to_backup = script_to_backup

    @property
    def task_name(self) -> str:
        return self._task_name

    @property
    def task_directory(self) -> Path:
        return 2
