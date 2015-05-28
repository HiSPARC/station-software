"""Common routine for loading messages from text files"""

import os


def load_hisparc_message(filename):
    """Read a hex encoded string of data and return it as a C struct

    :param filename: path to the text file to read relative to this script.
    :return: the message from the text file.

    """
    dir_path = os.path.dirname(__file__)
    file_path = os.path.join(dir_path, filename)
    with open(file_path, 'r') as data:
        event = data.readline().strip('\n').decode('hex')
    return event
