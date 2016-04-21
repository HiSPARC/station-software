import sys
sys.path.append("..")
import unittest

from WeatherEvent import WeatherEvent

from parse_and_check import parse_and_check_data
from load_message import load_weather_message


class TestHiSPARCEvent(unittest.TestCase):

    def test_event(self):
        event = load_weather_message('test_data/WeatherEvent.txt')
        parse_and_check_data(self, event, 16, WeatherEvent, 'WTR')


if __name__ == '__main__':
    unittest.main()
