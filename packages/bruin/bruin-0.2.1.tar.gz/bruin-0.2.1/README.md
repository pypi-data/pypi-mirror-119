# Bruin CLI

A toolbox for UCLA students in various events

Project published on PyPi: https://pypi.org/project/bruin/

## Installation:
```sh
pip install bruin
```
or download this repo and run
```sh
python setup.py install
```

## Simple Usages:

### Meal
Print today's dining menu

```sh
bruin meal
```
Print hour of operations:
```sh
bruin meal --hour=['', 'all', 'De Neve', etc.]
```

Print detail menu:
```sh
bruin meal --detail=['Breakfast', 'Lunch', 'Dinner']
```

## Troubleshooting

1. *Cannot find certain packages*: Make sure you install Python 3.6 or higher and use it throughout your system.
2. *ModuleError: No module <module_name>*: Check whether the path you are running python is the same as where `pip` install all the dependencies. The root should be in the output log when you run either commands.
   