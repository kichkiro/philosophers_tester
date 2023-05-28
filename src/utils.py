#!/usr/bin/python3

"""
A set of utils functions.
"""

# Libraries ------------------------------------------------------------------>

import os
import re
import shutil
import subprocess
import sys

from termcolor import colored

# Authorship ----------------------------------------------------------------->

__author__ = "Kirill Shkirov"
__license__ = "GPL-3.0"
__email__ = "kichkiro@student.42firenze.it"
__slack__ = "kichkiro"
__status__ = "Development"

# Functions ------------------------------------------------------------------>


def banner() -> None:
    """
    Print a formatted banner with ASCII art.

    Params
    --------------------------------------------------------------------
    None

    Returns
    --------------------------------------------------------------------
    None
    """
    print(colored(
        "    ____  __    _ __                       __                     \n"
        "   / __ \/ /_  (_) /___  _________  ____  / /_  ___  __________   \n"
        "  / /_/ / __ \/ / / __ \/ ___/ __ \/ __ \/ __ \/ _ \/ ___/ ___/   \n"
        " / ____/ / / / / / /_/ (__  ) /_/ / /_/ / / / /  __/ /  (__  )    \n"
        "/_/   /_/ /_/_/_/\____/____/\____/ .___/_/ /_/\___/_/  /____/     \n"
        "   ______         __            /_/                               \n"
        "  /_  _ /_  _____/ /____  _____                                   \n"
        "  / / / _ \/ ___/ __/ _ \/ ___/                                   \n"
        " / / /  __(__  ) /_/  __/ /                                       \n"
        "/_/  \___/____/\__/\___/_/                                      \n\n"
        "Will you die in the right way?                                    \n",
        "yellow",
        attrs=["bold"]
    ))


def makefile(rules: str, must_print: bool, project_path: str) -> None:
    """
    Run the make command with specified rules on a given project path.

    Params
    --------------------------------------------------------------------
    rules : str
        The makefile rules to run.
    must_print : bool
        Whether to print output or not.
    project_path : str
        The path to the project directory.

    Returns
    --------------------------------------------------------------------
    None
    """
    process: subprocess.Popen
    make_error: bytes

    if rules != "":
        process = subprocess.Popen(
            ["make", rules, "-C", project_path],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
    else:
        process = subprocess.Popen(
            ["make", "-C", project_path],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
    _, make_error = process.communicate()
    if not process.returncode and must_print:
        print(colored("Make: OK\n", "green",))
    elif process.returncode:
        print(colored(f"Make: KO!\n\n    {make_error.decode('utf-8')}", "red"))
        sys.exit(1)


def norminette(project_path: str) -> None:
    """
    Run the norminette command on a given project path.

    Params
    --------------------------------------------------------------------
    project_path : str
        The path to the project directory.

    Returns
    --------------------------------------------------------------------
    None
    """
    process: subprocess.Popen

    process = subprocess.Popen(
        ["norminette", project_path],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    process.communicate()
    if not process.returncode:
        print(colored("Norminette: OK\n", "green"))
    else:
        print(colored("Norminette: Error!\n", "red"))


def global_finder(directory: str) -> None:
    """
    Find the number of global variables in a given directory and its
    subdirectories.

    Params
    --------------------------------------------------------------------
    directory : str
        The directory to search in.

    Returns
    --------------------------------------------------------------------
    None
    """
    global_var: int

    global_var = 0
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith((".c", ".h")):
                with open(os.path.join(root, file), "r", encoding="utf-8")\
                        as file:
                    if "g_" in file.read():
                        global_var += 1
    if global_var:
        print(colored(f"Global Var: {global_var}\n", "red"))
    else:
        print(colored(f"Global Var: {global_var}\n", "green"))


def change_flag(old_flag: str, new_flag: str, project_path: str) -> None:
    """
    Replaces the old flag with the new flag in the Makefile of a
    project.

    Params
    --------------------------------------------------------------------
    old_flag : str
        The flag to be replaced.
    new_flag : str
        The new flag that will replace the old one.
    project_path : str
        The path to the project directory.

    Returns
    --------------------------------------------------------------------
    None
    """
    temp_path: str

    temp_path = os.path.join(project_path, "Makefile.temp")
    shutil.copy2(os.path.join(project_path, "Makefile"), temp_path)

    try:
        with open(temp_path, "r", encoding="utf-8") as file, open(
                os.path.join(project_path, "Makefile"), "w", encoding="utf-8")\
                as file2:
            for line in file:
                if old_flag in line:
                    line = re.sub(old_flag, new_flag, line)
                file2.write(line)
    except Exception as err:
        print(colored(
            f"Error occurred while modifying Makefile: {err}",
            "red"
        ))
        shutil.copy2(temp_path, os.path.join(project_path, "Makefile"))
    else:
        os.remove(temp_path)
