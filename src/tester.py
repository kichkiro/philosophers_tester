#!/usr/bin/python3

"""
A class to run a set of tests on a given project and evaluate the
results.
"""

# Libraries ------------------------------------------------------------------>

import signal
from subprocess import PIPE, Popen, TimeoutExpired
from typing import List, Union

from termcolor import colored

import tests

# Authorship ----------------------------------------------------------------->

__author__ = "Kirill Shkirov"
__license__ = "GPL-3.0"
__email__ = "kichkiro@student.42firenze.it"
__slack__ = "kichkiro"
__status__ = "Development"

# Functions ------------------------------------------------------------------>


class Tester:
    """
    Attributes
    --------------------------------------------------------------------
    project_path : str
        The path to the project to be tested.
    test : str
        The name of the test to run.

    Methods
    --------------------------------------------------------------------
    run():
        Runs the test cases and prints the results.

    __death_1(process, stdout, stderr, args, i):
        Checks if only one philosopher is alive and died in a specific
        sequence.

    __death_2(process, stdout, stderr, args, i):
        Checks if no philosopher has died.

    __death_3(process, stdout, stderr, args, i):
        Checks if at least one philosopher has died.

    __valgrind(process, stdout, stderr, args, i):
        Runs the project with Valgrind Memcheck or Helgrind.

    __thread_sanitizer(process, stdout, stderr, args, i):
        Runs the project with ThreadSanitizer.
    """
    def __init__(self, project_path: str, exe: str, test: str) -> None:
        self.project_path = project_path

        self.name: str
        self.tests: List[List[Union[int, float]]]
        self.cmd: List[str]
        self.tests: callable

        self.name = test
        if test == "death_1":
            self.tests = tests.death_1
            self.cmd = [f"{project_path}/{exe}"]
        elif test == "death_2":
            self.tests = tests.death_2
            self.cmd = [f"{project_path}/{exe}"]
        elif test == "death_3":
            self.tests = tests.death_3
            self.cmd = [f"{project_path}/{exe}"]
        elif test == "valgrind_memcheck":
            self.tests = tests.other
            self.cmd = [
                "valgrind",
                "--tool=memcheck",
                "--leak-check=full",
                "--error-exitcode=1",
                f"{project_path}/{exe}"
            ]
        elif test == "valgrind_helgrind":
            self.tests = tests.other
            self.cmd = [
                "valgrind",
                "--tool=helgrind",
                "--error-exitcode=1",
                f"{project_path}/{exe}"
            ]
        elif test == "thread_sanitizer":
            self.tests = tests.other
            self.cmd = [f"{project_path}/{exe}"]

    def run(self) -> None:
        """
        Runs the test cases and prints the results.

        Params
        ----------------------------------------------------------------
        None

        Returns
        ----------------------------------------------------------------
        None
        """
        i = 0
        for test in self.tests:
            timeout = test[0] * (test[1] / 1000) * test[4] * 1.5
            test = [str(arg) for arg in test]
            process = Popen(
                self.cmd + test,
                stdout=PIPE,
                stderr=PIPE
            )
            try:
                stdout, stderr = process.communicate(timeout=timeout)

                if self.name == "death_1":
                    self.__death_1(stdout, test, i)
                elif self.name == "death_2":
                    self.__death_2(stdout, test, i)
                elif self.name == "death_3":
                    self.__death_3(stdout, test, i)
                elif self.name == "valgrind_memcheck":
                    self.__valgrind(process, stderr, test, i)
                elif self.name == "valgrind_helgrind":
                    self.__valgrind(process, stderr, test, i)
                elif self.name == "thread_sanitizer":
                    self.__thread_sanitizer(process, stderr, test, i)
            except TimeoutExpired:
                process.send_signal(signal.SIGINT)
                print(colored(
                    f"TEST {i}: KO\n\n    Deadlock detected\n\n    "
                    f"ARGS: {' '.join(test)}\n",
                    "red"
                ))
            i += 1

    def __death_1(self, stdout: bytes, test: List[str], i: int) -> None:
        """
        Checks if only one philosopher is alive and died in a specific
        sequence.

        Params
        ----------------------------------------------------------------
        stdout : bytes
            The stdout of the project.
        test : List[str]
            The arguments passed to the project.
        i : int
            The number of the test case.

        Returns
        ----------------------------------------------------------------
        None
        """
        if stdout.decode().count('\n') != 2:
            print(colored(
                f"TEST {i}: KO\n\n"
                "    When is only 1 philo, he must die in this sequence:\n"
                "    1- \"timestamp_in_ms X has taken a fork\"\n"
                "    2- \"timestamp_in_ms X died\"\n\n"
                f"    ARGS: {' '.join(test)}\n",
                "red"
            ))
        else:
            print(colored(f"TEST {i}: OK\n", "green"))

    def __death_2(self, stdout: bytes, test: List[str], i: int) -> None:
        """
        Checks if no philosopher has died.

        Params
        ----------------------------------------------------------------
        stdout : bytes
            The stdout of the project.
        test : List[str]
            The arguments passed to the project.
        i : int
            The number of the test case.

        Returns
        ----------------------------------------------------------------
        None
        """
        if "died" in stdout.decode():
            print(colored(
                f"TEST {i}: KO\n\n"
                "    No philosopher should die.\n\n"
                f"    ARGS: {' '.join(test)}\n",
                "red"
            ))
        else:
            print(colored(f"TEST {i}: OK\n", "green"))

    def __death_3(self, stdout: bytes, test: List[str], i: int) -> None:
        """
        Checks if one philosopher has died.

        Params
        ----------------------------------------------------------------
        stdout : bytes
            The stdout of the project.
        test : List[str]
            The arguments passed to the project.
        i : int
            The number of the test case.

        Returns
        ----------------------------------------------------------------
        None
        """
        if "died" not in stdout.decode():
            print(colored(
                f"TEST {i}: KO\n\n"
                "    One philosopher should die.\n\n"
                "    HINT: The tester looks for the word 'died' in stdout.\n\n"
                f"    ARGS: {' '.join(test)}\n",
                "red"
            ))
        else:
            print(colored(f"TEST {i}: OK\n", "green"))

    def __valgrind(self, process: Popen, stderr: bytes, test: List[str],
                   i: int) -> None:
        """
        Checks if there are memory leaks.

        Params
        ----------------------------------------------------------------
        process : Popen
            The process of the project.
        stderr : bytes
            The stderr of the project.
        test : List[str]
            The arguments passed to the project.
        i : int
            The number of the test case.

        Returns
        ----------------------------------------------------------------
        None
        """
        if process.returncode == 1:
            for error_line in stderr.decode('utf-8').split("\n"):
                if "ERROR SUMMARY" in error_line:
                    print(colored(
                        f"TEST {i}: KO\n\n    {error_line}\n\n    "
                        f"ARGS: {' '.join(test)}\n",
                        "red"
                    ))
        else:
            print(colored(f"TEST {i}: OK\n", "green"))

    def __thread_sanitizer(self, process: Popen, stderr: bytes,
                           test: List[str], i: int) -> None:
        """
        Runs the project with ThreadSanitizer.

        Params
        ----------------------------------------------------------------
        process : Popen
            The process of the project.
        stderr : bytes
            The stderr of the project.
        test : List[str]
            The arguments passed to the project.
        i : int
            The number of the test case.

        Returns
        ----------------------------------------------------------------
        None
        """
        if process.returncode != 0:
            for error_line in stderr.decode('utf-8').split("\n"):
                if "warnings" in error_line:
                    print(colored(
                        f"TEST {i}: KO\n\n    {error_line}\n\n    "
                        f"ARGS: {' '.join(test)}\n",
                        "red"
                    ))
        else:
            print(colored(f"TEST {i}: OK\n", "green"))
