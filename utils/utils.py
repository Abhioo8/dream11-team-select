#!/usr/bin/env python
# coding=utf-8

import os
from csv import DictWriter


def file_is_empty(path):
    """
    This function checks if a file is empty
    """
    try:
        return os.stat(path).st_size == 0
    except IOError:
        return False


def has_file_exists_not_create(file_name):
    """
    This functions checks if file exists if not create
    """
    filename = '{filename}.csv'.format(filename=file_name)
    path = '{directory}/csv/{filename}'.format(directory=os.getcwd(),
                                               filename=filename)
    if os.path.exists(path):
        return path

    return create_csv(file_name)


def create_csv(filename):
    """
    This function checks if the csv containing permits is already existing

    Parameters
    ----------
    filename: str
    """
    filename = '{filename}.csv'.format(filename=filename)
    directory = '{directory}/csv'.format(directory=os.getcwd())

    if not os.path.isdir(directory):
        os.makedirs(directory)

    path = '{directory}/csv/{filename}'.format(directory=os.getcwd(),
                                               filename=filename)
    # we will create a csv file and truncate also truncate the file if it
    # already exists
    with open(path, "w") as f:
        f.truncate()

    return path


def save_to_csv(headers, filename, record):
    """
    This function saves a record by appending it to a csv file
    It takes both a batch list file as well as generator.
    """
    filename = convert_to_filenameable(filename)
    path = has_file_exists_not_create(filename)
    with open(path, 'a') as csvfile:
        writer = DictWriter(csvfile, fieldnames=headers)
        if file_is_empty(path=path):
            writer.writeheader()
        writer.writerows(record)

    return path


def convert_to_filenameable(invalid_str):
    try:
        valid_string = invalid_str.replace("/", "_")
    except AttributeError:
        # valid string is kept None because the next line in Scraper class
        # checks if the string is returned
        valid_string = None
    return valid_string
