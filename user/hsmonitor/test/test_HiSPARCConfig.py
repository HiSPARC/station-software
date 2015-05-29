import sys
sys.path.append("..")
import unittest
import struct

from HiSPARCConfig import HiSPARCConfig

from load_message import load_hisparc_message


class TestHiSPARCConfig(unittest.TestCase):

    def test_config(self):
        config = load_hisparc_message('test_data/Config.txt')
        hisparcconfig = HiSPARCConfig([3, config])
        hisparcconfig.uploadCode = 'CFG'
        configdata = hisparcconfig.parseMessage()


if __name__ == '__main__':
    unittest.main()
