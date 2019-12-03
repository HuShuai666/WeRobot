#!/bin/bash
ps -aux | grep 6060 | awk '{print $2}' | xargs kill -9
gunicorn WeRobot.wsgi:application -b 0.0.0.0:6060 -w 4 -t 300 --reload