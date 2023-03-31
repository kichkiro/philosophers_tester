# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    tester.py                                          :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: kichkiro <marvin@42.fr>                    +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2023/03/28 19:06:15 by kichkiro          #+#    #+#              #
#    Updated: 2023/04/01 01:16:30 by kichkiro         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

# Libraries ------------------------------------------------------------------->

import signal
import subprocess

from termcolor import colored

# Functions ------------------------------------------------------------------->

class Tester:
    """
    A class to run a set of tests on a given project and evaluate the results.

    Attributes
    ----------------------------------------------------------------------------
    project_path : str
        The path to the project to be tested.
    test : str
        The name of the test to run.

    Methods
    ----------------------------------------------------------------------------
    run():
        Runs the test cases and prints the results.

    Private Methods
    ----------------------------------------------------------------------------
    __death_1(process, stdout, stderr, args, i):
        Checks if only one philosopher is alive and died in a specific sequence.
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
            self.test_file = "tester/test/death_1"
            self.cmd = [f"{project_path}/{exe}"]
            self.test = lambda process, stdout, stderr, args, i: \
            	self.__death_1(process, stdout, stderr, args, i)
        elif test == "death_2":
            self.test_file = "tester/test/death_2"
            self.cmd = [f"{project_path}/{exe}"]
            self.test = lambda process, stdout, stderr, args, i: \
                self.__death_2(process, stdout, stderr, args, i)
        elif test == "death_3":
            self.test_file = "tester/test/death_3"
            self.cmd = [f"{project_path}/{exe}"]
            self.test = lambda process, stdout, stderr, args, i: \
                self.__death_3(process, stdout, stderr, args, i)
        elif test == "valgrind_memcheck":
            self.test_file = "tester/test/other"
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
            self.test_file = "tester/test/other"
            self.cmd = [
                "valgrind",
                "--tool=helgrind",
            	"--error-exitcode=1",
                f"{project_path}/{exe}"
            ]
            self.test = lambda process, stdout, stderr, args, i: \
                self.__valgrind(process, stdout, stderr, args, i)
        elif test == "thread_sanitizer":
            self.test_file = "tester/test/other"
            self.cmd = [f"{project_path}/{exe}"]
            self.test = lambda process, stdout, stderr, args, i: \
                self.__thread_sanitizer(process, stdout, stderr, args, i)

    def run(self):
        i = 0
        for line in open(self.test_file, 'r'):
            args = line.split()
            timeout = int(args[0]) * (int(args[1]) / 1000) * int(args[4]) * 1.5
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
            print(colored(f"TEST {i}: KO\n", "red"))
            print(colored(
				"    When is only 1 philo, he must die in this sequence:\n"
				"    1- \"timestamp_in_ms X has taken a fork\"\n"
				"    2- \"timestamp_in_ms X died\"\n",
				"red"
			))
            print(colored(f"    ARGS: {' '.join(args)}\n", "red"))
        else:
            print(colored(f"TEST {i}: OK\n", "green"))

    def __death_2(self, process, stdout, stderr, args, i):
        if "died" in stdout.decode():
            print(colored(f"TEST {i}: KO\n", "red"))
            print(colored("    No philosopher should die\n", "red"))
            print(colored(f"    ARGS: {' '.join(args)}\n", "red"))
        else:
            print(colored(f"TEST {i}: OK\n", "green"))

    def __death_3(self, process, stdout, stderr, args, i):
        if not "died" in stdout.decode():
            print(colored(f"TEST {i}: KO\n", "red"))
            print(colored("    One philosopher should die\n", "red"))
            print(colored(f"    ARGS: {' '.join(args)}\n", "red"))
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
