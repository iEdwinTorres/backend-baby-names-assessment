#!/usr/bin/env python
# -*- coding: utf-8 -*-

# BabyNames python coding exercise.

# Copyright 2010 Google Inc.
# Licensed under the Apache License, Version 2.0
# http://www.apache.org/licenses/LICENSE-2.0

"""
Define the extract_names() function below and change main()
to call it.

For writing regex, it's nice to include a copy of the target
text for inspiration. Here's what the HTML looks like in the
baby.html files:
...
<h3 align="center">Popularity in 1990</h3>
....
<tr align="right"><td>1</td><td>Michael</td><td>Jessica</td>
<tr align="right"><td>2</td><td>Christopher</td><td>Ashley</td>
<tr align="right"><td>3</td><td>Matthew</td><td>Brittany</td>
...

Suggested milestones for incremental development:
 - Extract all the text from the file and print it
 - Find and extract the year and print it
 - Extract the names and rank numbers and print them
 - Get the names data into a dict and print it
 - Build the [year, 'name rank', ... ] list and print it
 - Fix main() to use the extracted_names list
"""

import sys
import re
import argparse


def extract_names(filename):
    with open(filename) as f:
        text = f.read()

    names = []
    pattern = r'Popularity in (\d{4})'
    year_match = re.search(pattern, text)
    year = year_match.group(1)
    names.append(year)

    pattern = r'<td>(\d+)</td><td>(\w+)</td><td>(\w+)</td>'
    names_ranks = re.findall(pattern, text)
    names_to_rank = {}
    for rank_tuple in names_ranks:
        rank, boy_name, girl_name = rank_tuple
        if boy_name not in names_ranks:
            names_to_rank[boy_name] = rank
        if girl_name not in names_to_rank:
            names_to_rank[girl_name] = rank
    
    sorted_names = sorted(names_to_rank.items())
    for name, rank in sorted_names:
        names.append(f'{name} {rank}')
    return names


def create_parser():
    """Create a command line parser object with 2 argument definitions."""
    parser = argparse.ArgumentParser(
        description="Extracts and alphabetizes baby names from html.")
    parser.add_argument(
        '--summaryfile', help='creates a summary file', action='store_true')
    parser.add_argument('files', help='filename(s) to parse', nargs='+')
    return parser


def main(args):
    parser = create_parser()

    ns = parser.parse_args(args)

    if not ns:
        parser.print_usage()
        sys.exit(1)

    file_list = ns.files
    create_summary = ns.summaryfile

    for filename in file_list:
        names = extract_names(filename)
        text = '\n'.join(names)
        if create_summary:
            with open(f'{filename}.summary', 'w') as f:
                f.write(text)
        else:
            print(text)


if __name__ == '__main__':
    main(sys.argv[1:])
