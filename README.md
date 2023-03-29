# Philosophers Tester
#### <i>[subject](subject/subject.pdf) v.10</i>

<p align="center">
  <img src="img/header.png"/>
</p>

## 🛠️ - How to use? 
#### To use the tester, run the following commands:
```
git clone https://github.com/kichkiro/philosophers_tester.git
cd philosophers_tester && python3 -m venv .venv && source .venv/bin/activate && pip3 install -r requirements.txt 
python3 tester/main.py [project path]
```

#### To deactivate virtual env run:
```
deactivate
```

## 📈 - How does it work?

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
    - in this test, no philosopher should die.
- death_3:
    - in this test, a philosopher should die.
- Valgrind Memcheck:
    - to check for memory leaks.
- Valgrind Helgrind:
    - to check for concurrency issues such as, race conditions and deadlocks.
- Thread Sanitize:
	- recompile the program with the -fsanitize=thread option, ThreadSanitize is another concurrency error checking tool.

## 💀 - When must he die?
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

## 🪲 - Report bugs
To report bugs or recommend improvements, contact me:
- Slack: <b>kichkiro</b>
- E-Mail: <b>kichkiro@student.42firenze.it</b>  

## ⚖️ - License
See [LICENSE](LICENSE)
