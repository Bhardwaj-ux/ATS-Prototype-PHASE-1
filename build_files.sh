#!/bin/bash
set -o errexit

python manage.py migrate --noinput