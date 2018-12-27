from setuptools import setup

setup(
    name="adventofcode",
    version="0.0.1",
    install_requires=[
        'requests',
        'numpy',
        'pandas',
        'matplotlib',
    ],
    extras_require={"dev": [
        "pytest",
        "flake8",
        "black",
        "jedi",
        "ipython",
        'ipykernel',
        'jupyter'
    ]}
)
