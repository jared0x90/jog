#!/bin/sh
gunicorn -b "0.0.0.0:80" jog:app -w 4 -D
