from setuptools import setup

setup(
    name='pydep',
    version='0.1',
    url='http://github.com/sourcegraph/python-deps',
    py_modules=['pydep'],
    author='Beyang Liu',
    description='a lightweight python module that statically '
                'computes the external imports of a python project',
    zip_safe=False,
    install_requires=[
        'nose==1.3.0',
        'wsgiref==0.1.2',
    ],
)
