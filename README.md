# Philosophers Tester
### <i>[subject](subject/en.subject.pdf) v.10</i>

<br>

<p align="center">
  <img src="img/header.png"/>
</p>

<br>

# 🗔 - Commands 
### To use the tester, run the following commands:
```
git clone https://github.com/kichkiro/philosophers_tester.git
python3 -m venv .venv && source .venv/bin/activate && pip3 install -r requirements.txt 
python3 tester/main.py [project path]
```

### To deactivate virtual env run:
```
deactivate
```

# 💀 - When must he die?
```
IF n_philo == 1;

ELIF n_philo > 1:

	IF n_philo % 2 == 0: 

		IF time_to_die < (time_to_eat + time_to_sleep);

		IF time_to_eat > (time_to_die / 2);
		
	ELIF n_philo % 2 == 1:

		IF time_to_die < (time_to_eat + time_to_sleep);

		IF time_to_eat > (time_to_die / 3);
```

# 📈 - Tester

The tester performs the following tests:
- make:
    - compile the project.
- norminette:
    - run norminette.
- global variables:
    - check if global variables are present.
- death_1:
    - test the program with a single philosopher, it should die in the following sequence:
        - timestamp_in_ms X has taken a fork
		- timestamp_in_ms X died
- death_2:
    - in this test the philosopher should never die, if the tester returns KO, although no philosopher is dead check if:
		- no one has eaten more than N times.
		- you are doing 5 prints for each.
- death_3:
    - in this test a philosopher should die, if the tester returns KO, even though a philosopher is dead, check if:
		- no one has eaten more than N times.
		- you are doing 5 prints for each.
- Valgrind Memcheck:
    - check for memory leaks.
- Valgrind Helgrind:
    - to check for concurrency issues such as, race conditions and deadlocks.
- Thread Sanitize:
	- recompile the program with the -fsanitize=thread option, ThreadSanitize is another concurrency error checking tool.

<br>

# 🪲 - Report bugs
### Contact me: 
- Slack: <b>kichkiro</b>
- E-Mail: <b>kichkiro@student.42firenze.it</b>  

<br>

# ⚖️ - License
See [LICENSE](LICENSE)
