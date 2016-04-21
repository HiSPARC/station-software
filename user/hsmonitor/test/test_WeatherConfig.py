import sys
sys.path.append("..")
import unittest

from WeatherConfig import WeatherConfig

from parse_and_check import parse_and_check_data
from load_message import load_weather_message


class TestHiSPARCConfig(unittest.TestCase):

    def test_config(self):
        config = load_weather_message('test_data/WeatherConfig.txt')
        parse_and_check_data(self, config, 18, WeatherConfig, 'WCG')


if __name__ == '__main__':
    unittest.main()
