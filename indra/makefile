TESTDIR = tests
PYLINT = flake8
PYLINTFLAGS = --ignore=E741,W503 --exclude=interactive.py
PYTHONFILES = $(shell ls *.py)
TEST_FILES = $(shell ls $(TESTDIR)/test_*.py)
SHELL := /bin/bash

export user_type = test

prod: tests
	-git commit -a
	git push origin master

lint: $(patsubst %.py,%.pylint,$(PYTHONFILES))

pytests: $(PYTHONFILES)
	./pytests.sh

test_agent:
	nosetests tests.test_agent --nocapture

test_composite:
	nosetests tests.test_composite --nocapture

test_env:
	$(PYLINT) $(PYLINTFLAGS) env.py
	nosetests tests.test_env --nocapture

test_registry:
	$(PYLINT) $(PYLINTFLAGS) registry.py
	nosetests tests.test_registry --nocapture

test_space:
	nosetests tests.test_space --nocapture

tests: pytests lint

%.pylint:
	$(PYLINT) $(PYLINTFLAGS) $*.py

nocrud:
	-rm *~
	-rm *.log
	-rm *.out
	-rm .*swp
	-rm *.csv
	-rm $(TESTDIR)/*~
