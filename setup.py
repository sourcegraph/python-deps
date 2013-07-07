from setuptools import setup

setup(
    name='deps',
    version='0.1',
    url='https://github.com/sourcegraph/python-deps',
    license='BSD',
    author='Beyang Liu',
    description='a lightweight python module that statically '
                'computes the external imports of a python project',
    install_requires=[
        'nose==1.3.0',
        'wsgiref==0.1.2',
    ],
)
