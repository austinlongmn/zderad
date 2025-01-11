#!/usr/bin/env python3

import argparse
import shutil
import os
import pathlib

# This program runs in a directory and creates a Microsoft word document
# containing any psudocode, python, or other code files in the directory for
# coursework submission.

def get_tmp_directory():
    "Creates and returns a temporary directory to store files."
    os.mkdir("zderad.tmp")

def cleanup():
    "Removes the temporary directory and all files within it."
    shutil.rmtree("zderad.tmp")
    
def get_tmp_file_name(relative_path):
    "Returns a temporary file name for a file."
    return "zderad.tmp/" + relative_path

def main():
    pass

if __name__ == '__main__':
    main()
