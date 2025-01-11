#!/usr/bin/env python3

import argparse
import shutil
import os
import pathlib
import tempfile

# This program runs in a directory and creates a Microsoft word document
# containing any psudocode, python, or other code files in the directory for
# coursework submission.

def get_tmp_directory():
    "Creates and returns a temporary directory to store files."
    return tempfile.mkdtemp()

def cleanup(tmp_directory):
    "Removes the temporary directory and all files within it."
    shutil.rmtree(tmp_directory)

# TODO: The main operation should be the following:
# 1. Create a Markdown file with all the code files in the directory.
# 2. Convert the Markdown file to a Microsoft Word document with pandoc.

def main():
    parser = argparse.ArgumentParser(description="Create a Microsoft Word document containing code files.")
    parser.add_argument("-m", "--output-images", help="Directory containing images of the program's output.")
    parser.add_argument("-i", "--include-glob", help="Glob pattern of files to include.")
    parser.add_argument("directory", help="The directory containing the code files.")
    parser.add_argument("output", help="The output file.")
    args = parser.parse_args()
    
    tmp_directory = get_tmp_directory()
    try:
        pass
    finally:
        cleanup(tmp_directory)

if __name__ == '__main__':
    main()
