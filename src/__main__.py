#!/usr/bin/python3

"""
Tester for the Philosophers project of school 42.
"""

# Libraries ------------------------------------------------------------------>

import os
import sys
from typing import List

from termcolor import colored

import utils
from tester import Tester

# Authorship ----------------------------------------------------------------->

__author__ = "Kirill Shkirov"
__license__ = "GPL-3.0"
__email__ = "kichkiro@student.42firenze.it"
__slack__ = "kichkiro"
__status__ = "Development"

# Functions ------------------------------------------------------------------>


def main(argv: List[str]) -> None:
    """
    The main function of the tester.

    Params
    --------------------------------------------------------------------
    argv : List[str]
        The list of arguments passed to the script.

    Returns
    --------------------------------------------------------------------
    None
    """
    project_path: str
    exe: str
    death_1: Tester
    death_2: Tester
    death_3: Tester
    valgrind_memcheck: Tester
    valgrind_helgrind: Tester
    thread_sanitizer: Tester

    if len(argv) != 2:
        print(colored("\nWrong input arguments...\n", "red", attrs=["bold"]))
        print(colored("[project_path]\n", "white"))
        sys.exit()

    project_path = os.path.abspath(argv[1])
    exe = os.path.basename(project_path)

    if exe == "philo_bonus":
        print(colored("\nBonus coming soon!", "blue"))
        sys.exit()

    utils.banner()

    death_1 = Tester(project_path, exe, "death_1")
    death_2 = Tester(project_path, exe, "death_2")
    death_3 = Tester(project_path, exe, "death_3")
    valgrind_memcheck = Tester(project_path, exe, "valgrind_memcheck")
    valgrind_helgrind = Tester(project_path, exe, "valgrind_helgrind")
    thread_sanitizer = Tester(project_path, exe, "thread_sanitizer")

    # PRE-TEST --------------------------------------------------------------->

    print(colored(
        "PRE-TEST ---------------------------------------------------------->"
        "\n", "white", attrs=["bold"]))

    utils.makefile("", True, project_path)
    utils.norminette(project_path)
    utils.global_finder(project_path)

    # DEATH TEST - One Philo ------------------------------------------------->

    print(colored(
        "DEATH TEST -------------------------------------------------------->",
        "white",
        attrs=["bold"]
    ))
    print(colored("- One philo -\n", "white"))

    death_1.run()

    # DEATH TEST - No one must die ------------------------------------------->

    print(colored(
        "DEATH TEST -------------------------------------------------------->",
        "white",
        attrs=["bold"]
    ))
    print(colored("- No one must die -\n", "white"))

    death_2.run()

    # DEATH TEST - One must die ---------------------------------------------->

    print(colored(
        "DEATH TEST -------------------------------------------------------->",
        "white",
        attrs=["bold"]
    ))
    print(colored("- One must die -\n", "white"))

    death_3.run()

    # VALGRIND --tool=memcheck ----------------------------------------------->

    print(colored(
        "VALGRIND ---------------------------------------------------------->",
        "white",
        attrs=["bold"]
    ))
    print(colored("--tool=memcheck -\n", "white"))

    valgrind_memcheck.run()

    # VALGRIND --tool=helgrind ----------------------------------------------->

    print(colored(
        "VALGRIND ---------------------------------------------------------->",
        "white",
        attrs=["bold"]
    ))
    print(colored("--tool=helgrind -\n", "white"))

    valgrind_helgrind.run()

    # ThreadSanitizer -------------------------------------------------------->

    print(colored(
        "ThreadSanitizer --------------------------------------------------->"
        '\n',
        "white",
        attrs=["bold"]
    ))

    utils.change_flag("-pthread", "-fsanitize=thread", project_path)
    utils.makefile("re", False, project_path)
    thread_sanitizer.run()
    utils.change_flag("-fsanitize=thread", "-pthread", project_path)
    utils.makefile("fclean", False, project_path)


if __name__ == "__main__":
    main(sys.argv)
