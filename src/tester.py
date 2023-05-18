#!/usr/bin/python3

"""
A class to run a set of tests on a given project and evaluate the 
results.
"""

# Libraries ------------------------------------------------------------------>

import signal
import subprocess

from termcolor import colored
import args

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

    Private Methods
    --------------------------------------------------------------------
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
        if test == "death_1":
            self.args = args.death_1
            self.cmd = [f"{project_path}/{exe}"]
            self.test = lambda process, stdout, stderr, args, i: \
            	self.__death_1(process, stdout, stderr, args, i)
        elif test == "death_2":
            self.args = args.death_2
            self.cmd = [f"{project_path}/{exe}"]
            self.test = lambda process, stdout, stderr, args, i: \
                self.__death_2(process, stdout, stderr, args, i)
        elif test == "death_3":
            self.args = args.death_3
            self.cmd = [f"{project_path}/{exe}"]
            self.test = lambda process, stdout, stderr, args, i: \
                self.__death_3(process, stdout, stderr, args, i)
        elif test == "valgrind_memcheck":
            self.args = args.other
            self.cmd = [
                "valgrind",
                "--tool=memcheck",
                "--leak-check=full",
            	"--error-exitcode=1",
                f"{project_path}/{exe}"
            ]
            self.test = lambda process, stdout, stderr, args, i: \
                self.__valgrind(process, stdout, stderr, args, i)
        elif test == "valgrind_helgrind":
            self.args = args.other
            self.cmd = [
                "valgrind",
                "--tool=helgrind",
            	"--error-exitcode=1",
                f"{project_path}/{exe}"
            ]
            self.test = lambda process, stdout, stderr, args, i: \
                self.__valgrind(process, stdout, stderr, args, i)
        elif test == "thread_sanitizer":
            self.args = args.other
            self.cmd = [f"{project_path}/{exe}"]
            self.test = lambda process, stdout, stderr, args, i: \
                self.__thread_sanitizer(process, stdout, stderr, args, i)


    def run(self):
        i = 0
        for args in self.args:
            timeout = args[0] * (args[1] / 1000) * args[4] * 1.5
            args = [str(arg) for arg in args]
            process = subprocess.Popen(
                self.cmd + args,
                stdout=subprocess.PIPE, 
                stderr=subprocess.PIPE
            )
            try:
                stdout, stderr = process.communicate(timeout=timeout)
                self.test(process, stdout, stderr, args, i)
            except subprocess.TimeoutExpired:
                process.send_signal(signal.SIGINT)
                print(colored(
                    f"TEST {i}: KO\n\n    Deadlock detected\n\n    "
                    f"ARGS: {' '.join(args)}\n", 
                    "red"
                ))
            i += 1


    def __death_1(self, process, stdout, stderr, args, i):
        if stdout.decode().count('\n') != 2:
            print(colored(
                f"TEST {i}: KO\n\n"
				"    When is only 1 philo, he must die in this sequence:\n"
				"    1- \"timestamp_in_ms X has taken a fork\"\n"
				"    2- \"timestamp_in_ms X died\"\n\n"
                f"    ARGS: {' '.join(args)}\n",
				"red"
			))
        else:
            print(colored(f"TEST {i}: OK\n", "green"))


    def __death_2(self, process, stdout, stderr, args, i):
        if "died" in stdout.decode():
            print(colored(
                f"TEST {i}: KO\n\n"
                "    No philosopher should die.\n\n"
                f"    ARGS: {' '.join(args)}\n",
                "red"
            ))
        else:
            print(colored(f"TEST {i}: OK\n", "green"))


    def __death_3(self, process, stdout, stderr, args, i):
        if not "died" in stdout.decode():
            print(colored(
                f"TEST {i}: KO\n\n"
                "    One philosopher should die.\n\n"
                "    HINT: The tester looks for the word 'died' in stdout.\n\n"
                f"    ARGS: {' '.join(args)}\n",
                "red"
            ))
        else:
            print(colored(f"TEST {i}: OK\n", "green"))


    def __valgrind(self, process, stdout, stderr, args, i):
        if process.returncode == 1:
            for error_line in stderr.decode('utf-8').split("\n"):
                if "ERROR SUMMARY" in error_line:
                    print(colored(
                        f"TEST {i}: KO\n\n    {error_line}\n\n    "
                        f"ARGS: {' '.join(args)}\n", 
                        "red"
                    ))
        else:
            print(colored(f"TEST {i}: OK\n", "green"))


    def __thread_sanitizer(self, process, stdout, stderr, args, i):
        if process.returncode != 0:
            for error_line in stderr.decode('utf-8').split("\n"):
                if "warnings" in error_line:
                    print(colored(
                        f"TEST {i}: KO\n\n    {error_line}\n\n    "
                        f"ARGS: {' '.join(args)}\n", 
                        "red"
                    ))
        else:
            print(colored(f"TEST {i}: OK\n", "green"))
