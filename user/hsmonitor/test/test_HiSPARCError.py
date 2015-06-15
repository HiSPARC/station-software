import sys
sys.path.append("..")
import unittest

from HiSPARCError import HiSPARCError

from load_message import load_hisparc_message


class TestHiSPARCError(unittest.TestCase):

    def test_error(self):
        error = load_hisparc_message('test_data/Error.txt')
        hisparcerror = HiSPARCError([2, error])
        hisparcerror.uploadCode = 'ERR'
        errordata = hisparcerror.parseMessage()


if __name__ == '__main__':
    unittest.main()
