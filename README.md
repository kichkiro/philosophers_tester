<img src="https://github.com/kichkiro/42_cursus/blob/assets/banner_philosophers_tester.png?raw=true" width="100%"/>

## 🛠️ - How to use?

#### First time
```bash
git clone https://github.com/kichkiro/philosophers_tester.git
cd philosophers_tester 
pip3 install -r requirements.txt 
python3 src/__main__.py [project path]
```

#### Next times
```bash
python3 src/__main__.py [project path]
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
	- recompile the program with the -fsanitize=thread option. ThreadSanitize is another concurrency error checking tool.

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
