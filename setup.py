from setuptools import setup

with open("README.md") as f:
    long_description = f.read()

setup(
    name="zderad",
    version="1.0",
    description=(
        "A program to create a Microsoft Word document containing code files."
    ),
    long_description=long_description,
    author="Austin Long",
    author_email="austin@austinlong.dev",
    packages=["zderad"],  # same as name
    entry_points={
        "console_scripts": ["zderad=zderad.main:main"],
    },
)
