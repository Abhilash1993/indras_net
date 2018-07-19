#!/bin/sh

# Run this from inside your container to launch Emu86.
# Although *inside* the container the web server runs at 0.0.0.0:8000,
# from outside it appears at 127.0.0.1:8000.

export user_type="Web browser"
export base_dir=""

python ./manage.py runserver 0.0.0.0:8000