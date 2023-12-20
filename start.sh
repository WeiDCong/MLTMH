#!/bin/bash
conda activate web
gunicorn -w 4 -b 0.0.0.0:8887 app:server