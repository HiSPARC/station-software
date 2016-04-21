import sys
sys.path.append("..")
import unittest

from WeatherError import WeatherError

from parse_and_check import parse_and_check_data
from load_message import load_weather_message


class TestHiSPARCConfig(unittest.TestCase):

    def test_error(self):
        error = load_weather_message('test_data/WeatherError.txt')
        parse_and_check_data(self, error, 17, WeatherError, 'WER')


if __name__ == '__main__':
    unittest.main()
