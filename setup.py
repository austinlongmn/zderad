from setuptools import setup, find_packages

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
    packages=find_packages(),
    install_requires=["colored"],
    entry_points={
        "console_scripts": ["zderad=zderad.main:main"],
    },
)
