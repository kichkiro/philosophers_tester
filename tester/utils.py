#!/usr/bin/python3

"""
A set of utils functions.
"""

# Libraries ------------------------------------------------------------------>

import re
import os
import shutil
import subprocess

from termcolor import colored

# Authorship ----------------------------------------------------------------->

__author__ = "Kirill Chkirov"
__license__ = "other"
__email__ = "kichkiro@student.42firenze.it"
__slack__ = "kichkiro"
__status__ = "Development"

# Functions ------------------------------------------------------------------>

def banner():
    """
    Print a formatted banner with ASCII art.
    
    Returns:
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


def makefile(rules: str, must_print: bool, project_path: str):
    """
    Run the make command with specified rules on a given project path.
    
    Args:
    	rules (str): The makefile rules to run.
    	must_print (bool): Whether to print output or not.
    	project_path (str): The path to the project directory.

	Returns:
        None
    """
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
    make_output, make_error = process.communicate()
    if not process.returncode and must_print:
        print(colored("Make: OK\n", "green",))
    elif process.returncode:
        print(colored(f"Make: KO!\n\n    {make_error.decode('utf-8')}", "red"))
        exit(1)


def norminette(project_path: str):
    """
    Run the norminette command on a given project path.
    
    Args:
    	project_path (str): The path to the project directory.

	Returns:
        None
    """
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


def global_finder(dir):
    """
    Find the number of global variables in a given directory and its 
    subdirectories.
    
    Args:
    	dir (str): The directory to search in.
    
    Returns:
        None
    """
    global_var = 0
    for root, dirs, files in os.walk(dir):
        for file in files:
            if file.endswith((".c", ".h")):
                with open(os.path.join(root, file), 'r') as f:
                    if "g_" in f.read():
                        global_var += 1
    if global_var:
        print(colored(f"Global Var: {global_var}\n", "red"))
    else:
        print(colored(f"Global Var: {global_var}\n", "green"))


def change_flag(old_flag: str, new_flag: str, project_path: str):
    """
    Replaces the old flag with the new flag in the Makefile of a 
    project.

    Args:
        old_flag (str): The flag to be replaced.
        new_flag (str): The new flag that will replace the old one.
        project_path (str): The path to the project directory.

    Returns:
        None
    """
    temp_path = os.path.join(project_path, "Makefile.temp")
    shutil.copy2(os.path.join(project_path, "Makefile"), temp_path)

    try:
        with open(temp_path, 'r') as f, open(
            os.path.join(project_path, "Makefile"), 'w') as g:
            for line in f:
                if old_flag in line:
                    line = re.sub(old_flag, new_flag, line)
                g.write(line)
    except Exception as e:
        print(colored(
            f"Error occurred while modifying Makefile: {e}",
            "red"
        ))
        shutil.copy2(temp_path, os.path.join(project_path, "Makefile"))
    else:
        os.remove(temp_path)

