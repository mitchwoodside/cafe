from setuptools import setup

setup(
    name='cafe',
    version='0.1.0',
    py_modules=['cafe'],
    install_requires=[
        'Click',
    ],
    entry_points={
        'console_scripts': [
            'cafe = cafe:cli',
        ],
    },
)
