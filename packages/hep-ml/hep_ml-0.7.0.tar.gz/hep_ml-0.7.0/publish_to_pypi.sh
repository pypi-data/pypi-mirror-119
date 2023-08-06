#!/usr/bin/env bash
# simple script to upload new versions to PyPI

echo $TWINE_USERNAME
echo $TWINE_PASSWORD

rm -f build/*
rm -f dist/*
python3 -m pip install --upgrade build twine
python3 -m build
TWINE_USERNAME=__token__ TWINE_PASSWORD=pypi-AgEIcHlwaS5vcmcCJDI3MGIzMDI5LTRiMWQtNDdiMi05YTkxLTM0NjZhM2Q1ZDYzNQACN3sicGVybWlzc2lvbnMiOiB7InByb2plY3RzIjogWyJoZXAtbWwiXX0sICJ2ZXJzaW9uIjogMX0AAAYg0VtuT7dopsFm9zUvlRgbyzAMb1as5ierLe0eZvLmCSo python3 -m twine upload dist/*