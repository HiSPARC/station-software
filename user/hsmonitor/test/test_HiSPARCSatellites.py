import sys
sys.path.append("..")
import unittest

from HiSPARCSatellites import HiSPARCSatellites

from parse_and_check import parse_and_check_data
from load_message import load_hisparc_message


class TestHiSPARCSatellites(unittest.TestCase):

    def test_satellites(self):
        satellites = load_hisparc_message('test_data/Satellites.txt')
        parse_and_check_data(self, satellites, 6, HiSPARCSatellites, 'SAT')


if __name__ == '__main__':
    unittest.main()
