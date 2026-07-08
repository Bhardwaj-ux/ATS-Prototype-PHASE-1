#!/bin/bash
set -o errexit

# Install Python dependencies into a local directory that will be uploaded
# with the build so the ASGI function has access to them during runtime.
BUILD_LIB_DIR=".vercel_build_python"
mkdir -p "$BUILD_LIB_DIR"
python3 -m pip install --upgrade pip || true
python3 -m pip install --no-cache-dir -r requirements.txt -t "$BUILD_LIB_DIR"

# Ensure the build lib is on PYTHONPATH when running manage commands
export PYTHONPATH="$PWD/$BUILD_LIB_DIR:$PYTHONPATH"

python manage.py migrate --noinput