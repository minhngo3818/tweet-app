VENV = venv
PYTHON = $(VENV)/bin/python3
PIP = $(VENV)/bin/pip
TWEET-KEY = "key"

setup: requirements.txt
	python3 -m venv $(VENV)
	$(PIP) install -r requirements.txt

envar:
	export TWEET=$(TWEET-KEY)

update-req: 
	$(PIP) freeze > requirements.txt

migrations: 
	python3 manage.py makemigrations

migrate: migrations
	python3 manage.py migrate

run: migrate
	python3 manage.py runserver

clean:
	rm -rf __pychache__