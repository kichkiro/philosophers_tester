# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    utils.py                                           :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: kichkiro <marvin@42.fr>                    +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2023/03/28 19:52:31 by kichkiro          #+#    #+#              #
#    Updated: 2023/03/29 13:38:12 by kichkiro         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

# Libraries ------------------------------------------------------------------->

import os
import re
import subprocess

from termcolor import colored

# Functions ------------------------------------------------------------------->

def header():
    """
    Print a formatted header with ASCII art
    
    Returns:
        None
    """
    print(colored(
        "    ____  __    _ __                       __                      \n"
        "   / __ \/ /_  (_) /___  _________  ____  / /_  ___  _____         \n"
        "  / /_/ / __ \/ / / __ \/ ___/ __ \/ __ \/ __ \/ _ \/ ___/         \n"
        " / ____/ / / / / / /_/ (__  ) /_/ / /_/ / / / /  __/ /             \n"
        "/_/   /_/ /_/_/_/\____/____/\____/ .___/_/ /_/\___/_/              \n"
        "   ______         __            /_/                                \n"
        "  /_  _ /_  _____/ /____  _____                                    \n"
        "  / / / _ \/ ___/ __/ _ \/ ___/                                    \n"
        " / / /  __(__  ) /_/  __/ /                                        \n"
        "/_/  \___/____/\__/\___/_/                                       \n\n"
        "Will you die in the right way?                                     \n",
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
    Replaces the old flag with the new flag in the Makefile of a project.

    Args:
        old_flag (str): The flag to be replaced.
        new_flag (str): The new flag that will replace the old one.
        project_path (str): The path to the project directory.

    Returns:
        None
    """
    with open(f"{project_path}/Makefile", 'r+') as f:
        content = f.read()
        if len(new_flag) < len(old_flag):
            new_flag += ' ' * (len(old_flag) - len(new_flag))
        new_content = re.sub(old_flag, new_flag, content)
        f.seek(0)
        f.write(new_content)
        f.close()
