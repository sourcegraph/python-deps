python-deps
===========

python-deps is a lightweight python module that computes the external
imports of a python project.  It does so statically, without importing
or running any code from the module itself.

The command and tests should be run from a clean virtualenv python.

This uses the standard lib associated with whatever python
installation used to run the module. A future version might support
specifying a path to a python env directory, to decouple the choice of
python used to execute the module vs. the python from which the names
of stdlib modules are detected.

Note: this module is a work-in-progress.

Installation
==========
```
pip install -r requirements.txt
```

Running
=======
```
python showpydep.py path/to/project/root
```

Running tests
=============
run `nosetests -s`.

Contributors
* Beyang Liu <beyang@sourcegraph.com>
