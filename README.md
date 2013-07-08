python-deps
===========

python-deps is a lightweight python module that computes the external
imports of a python project.  It does so statically, without importing
or running any code from the module itself.

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
