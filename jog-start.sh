#!/bin/sh
gunicorn jog:app -w 4 -D
