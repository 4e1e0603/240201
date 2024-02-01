# Assessment centre

## Solution

1. Just find the hidden element on the page (trivial).
2. Base64 encoded message and password is `LInyldqBmzweK^#8s$OZpg#zeBf*0T`.
   I don't think the assignment is understandable.
3. No comment
4. No comment

```shell
mypy --show-column-numbers --namespace-packages --explicit-package-bases .
Success: no issues found in 11 source files
```

I fixed something, this remains

```shell
ruff check --unsafe-fixes --fix .
ac\exercise\messages.py:10:29: S105 Possible hardcoded password assigned to: "EXERCISE_2_WRONG_PASSWORD"
ac\exercise\views.py:31:27: PLR2004 Magic value used in comparison, consider replacing 2 with a constant variable
ac\exercise\views.py:33:27: PLR2004 Magic value used in comparison, consider replacing 3 with a constant variable
ac\exercise\views.py:35:27: PLR2004 Magic value used in comparison, consider replacing 4 with a constant variable
ac\holly\views.py:47:66: PGH003 Use specific rule codes when ignoring type issues
```

---

Hello everyone and welcome to the ISECO Assessment Centre for new colleagues. This one focuses on general programming skills and simple Python tasks.
Enough words, let's get started. First of all, you need to set some [prerequisites](#prerequisites).

## Prerequisites

* [Python 3.11](https://www.python.org/) - It's up to you, but if you want to use multiple Python versions, I highly recommend the [pyenv](https://www.google.com) application.
* [pdm](https://pdm-project.org/latest/) - Modern Python package and dependency manager.

These two prerequisites are crucial for the next steps, so be sure that both of them are installed, before move to the other steps.

## Initializing

Ok, once we have both applications installed, we can move on to initialising the whole project. To do this, please follow these steps:

* Make sure you are in the root of the project
* Create a virtual environment and install all dependencies
  * To do this, run the command `pdm install -d`
  * At the end of this step, you will have a fully prepared environment
* The next step is to initialise the internal database
  * To do this, run the command `pdm run init-db`
* Ok, now you are ready to start the project
  * To do this, run the `pdm run start` command, open your browser and go to `http://localhost:5000/exercise/1`

## Exercises

But wait, what happened? Do you see that error screen? Something about `raised exception`? Right, because this is your first exercise. Try to solve it. After that, there are 4 more exercises prepared for you. Each one focuses on a slightly different aspect of your skills, but don't worry, it's all in the day's work :-)

So have fun and if you are curious, check out the code of the whole project.

## Built With

* [Python](https://www.python.org/) - Programming language for everyone
* [flask](https://flask.palletsprojects.com/en/3.0.x/) - Python web application framework
* [pyenv](https://github.com/pyenv/pyenv) - Python version manager
* [pdm](https://pdm-project.org/latest/) - Modern Python package and dependency manager

## Authors

* **Bohumil Fiala**
