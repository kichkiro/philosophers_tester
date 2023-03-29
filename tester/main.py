# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    main.py                                            :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: kichkiro <marvin@42.fr>                    +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2023/03/12 19:54:33 by kichkiro          #+#    #+#              #
#    Updated: 2023/03/29 19:47:57 by kichkiro         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

# Libraries ------------------------------------------------------------------->

import os
import sys

import utils
from tester import Tester
from termcolor import colored

# Main Functions -------------------------------------------------------------->

def main():
    # Init -------------------------------------------------------------------->
    
    utils.header()
    argv = sys.argv

    if len(argv) != 2:
        print(colored("Wrong input arguments...\n", "red", attrs=["bold"]))
        print(colored("[project_path]\n", "white"))
        exit()

    project_path = os.path.abspath(argv[1])

    death_1 = Tester(project_path, "death_1")
    death_2 = Tester(project_path, "death_2")
    death_3 = Tester(project_path, "death_3")
    valgrind_memcheck = Tester(project_path, "valgrind_memcheck")
    valgrind_helgrind = Tester(project_path, "valgrind_helgrind")
    thread_sanitizer = Tester(project_path, "thread_sanitizer")

    # PRE-TEST ---------------------------------------------------------------->
    
    print(colored(
        "PRE-TEST ----------------------------------------------------------->"
        "\n", "white", attrs=["bold"]))

    utils.makefile("", True, project_path)
    utils.norminette(project_path)
    utils.global_finder(project_path)
    
    # DEATH TEST - One Philo -------------------------------------------------->

    print(colored(
        "DEATH TEST --------------------------------------------------------->",
        "white", 
        attrs=["bold"]
    ))
    print(colored("- One philo -\n", "white"))

    death_1.run()

    # DEATH TEST - No one must die -------------------------------------------->

    print(colored(
        "DEATH TEST --------------------------------------------------------->",
        "white", 
        attrs=["bold"]
    ))
    print(colored("- No one must die -\n", "white"))

    death_2.run()

    # DEATH TEST - One must die ----------------------------------------------->

    print(colored(
        "DEATH TEST --------------------------------------------------------->",
        "white", 
        attrs=["bold"]
    ))
    print(colored("- One must die -\n", "white"))

    death_3.run()

    # VALGRIND --tool=memcheck ------------------------------------------------>

    print(colored(
        "VALGRIND ----------------------------------------------------------->",
        "white", 
        attrs=["bold"]
    ))
    print(colored("--tool=memcheck -\n", "white"))

    valgrind_memcheck.run()

    # VALGRIND --tool=helgrind ------------------------------------------------>

    print(colored(
        "VALGRIND ----------------------------------------------------------->",
        "white", 
        attrs=["bold"]
    ))
    print(colored("--tool=helgrind -\n", "white"))
    
    valgrind_helgrind.run()

    # ThreadSanitizer --------------------------------------------------------->
    
    print(colored(
        "ThreadSanitizer ---------------------------------------------------->"
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
    main()
