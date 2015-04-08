import os
import re
import ctypes


def checkIfAdmin():
    """Check if you are in admin mode"""
    try:
        is_admin = os.getuid() == 0
    except:
        is_admin = ctypes.windll.shell32.IsUserAnAdmin()
    return is_admin


def parse_version(search_name, filename):
    """Extract version numbers from filename

    Parses search_name_v19.exe to 19, and search_name_v20.124.exe to 20.

    """
    mo = re.search("%s_v(\d+)(\.(\d+))?\.exe$" % search_name, filename)
    if mo:
        return int(mo.group(1))

def checkIfNewerFileExists(location, search_name, current_version):
    """Check if newer file exists

    Note: This function gets confused if there are multiple files with
    the same 'main' version number (e.g. v3 and v3.1)

    :param location: path to directory containing updaters.
    :param search_name: name of the updater file (excluding the version).
    :param current_version: integer, current version number

    """
    file_list = os.listdir(location)
    found = False
    version_found = 0
    file_found = ""
    for item in file_list:
        version_number = parse_version(search_name, item)
        if current_version < version_number > version_found:
            version_found = version_number
            file_found = item
            found = True
    return found, file_found


def checkIfEqualFileExists(location, searchName):
    return os.access("%s\%s" % (location, searchName), os.F_OK)
