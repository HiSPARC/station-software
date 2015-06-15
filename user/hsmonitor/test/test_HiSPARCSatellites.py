import sys
sys.path.append("..")
import unittest

from HiSPARCSatellites import HiSPARCSatellites

from load_message import load_hisparc_message


class TestHiSPARCSatellites(unittest.TestCase):

    def test_satellites(self):
        satellites = load_hisparc_message('test_data/Satellites.txt')
        hisparcsatellites = HiSPARCSatellites([6, satellites])
        hisparcsatellites.uploadCode = 'SAT'
        satellitesdata = hisparcsatellites.parseMessage()


if __name__ == '__main__':
    unittest.main()
