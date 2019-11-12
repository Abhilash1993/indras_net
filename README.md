[![Build Status](https://travis-ci.org/gcallah/indras_net.svg?branch=master)](https://travis-ci.org/gcallah/indras_net)
[![codecov](https://codecov.io/gh/gcallah/indras_net/branch/master/graph/badge.svg)](https://codecov.io/gh/gcallah/indras_net)

Indra
=====
This is a project building an agent-based modeling system in Python. The
ultimate goal is to build a GUI front-end that will allow non-coders to build
models, while at the same time permitting coders to use Python for more
flexibility in model creation.


We are currently building **indra2**, a new version of the system. Our API
Serever is moving along,  we have a react frontend in progress, and many models
have been ported to version 2.

Developing and Contributing
---------------------------
To configure your system for development, first install Python 3 and git and
then run `make create_dev_env`. This will install some dependencies using PIP.
Follow the outputted instructions for setting your environment variables.

To build the Docker container with the development environment, run
`make dev_container`.

To run the Docker container with the development environment, run
`./dev_cont.sh`.

To run tests on Python code, run `make pytests`. To run tests on JavaScript
code, run `make jstests`. To run tests on both Python and JavaScript code,
run `make tests`. These can be run inside or outside the Docker container.
Optionally, you can first `cd` into [APIServer](APIServer), [indra](indra),
[models](models), or [webapp](webapp) before running `make tests` to run only
the tests for that directory.

To test the APIServer with the front end locally:
- Front end:
    - run `make setup_react` to install all modules listed as dependencies.
    - Find and replace the `https://indrasnet.pythonanywhere.com/` under `webapp/src/components/` to your server's address (such as `http://127.0.0.1:8000`)
    - `cd` into `webapp` and run `npm run start` 
- Back end:
    - `cd` into [APIServer](APIServer), then run `./api.sh` to start your server
