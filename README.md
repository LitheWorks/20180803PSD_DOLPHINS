# Torpydo

A simple game of Battleship, written in Python.

# Getting started

This project requires Python 3.6. To prepare to work with it, pick one of these
options:

## Linux and macOS

Create and activate a [virtual environment][venv]. This assumes python3 is
already installed.

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
export PYTHONPATH=.
```

If you stop working on this project, close your shell, and return later, make
sure you run the `source bin/venv/activate` command again.

[venv]:https://docs.python.org/3/library/venv.html

## Windows

[Download][pywin] and install Python 3.6 for Windows. Make sure python is on
your `PATH`. Open a command prompt:

```commandline
python -m venv venv
venv\Scripts\activate.bat
pip install -r requirements.txt
set PYTHONPATH=.
```

[pywin]:https://www.python.org/downloads/windows/

## Docker

If you don't want to install anything Python-related on your system, you can
run the game inside Docker instead:

```bash
docker run -it --env PYTHONPATH=/torpydo --volume $PWD:/torpydo --workdir /torpydo python:3.6 bash
pip install -r requirements.txt
```

# Launching the game

```bash
python -m torpydo

# alternatively:
python torpydo/battleship.py
```

# Running the Tests

```
nosetests 
behave
```

to run with coverage:
```
nosetests --with-coverage
```

Run behevae tests with coverage:
```
https://stackoverflow.com/a/37447392/736079
```