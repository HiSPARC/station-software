import sys
sys.path.append("..")
import unittest

from WeatherEvent import WeatherEvent

from load_message import load_weather_message


class TestHiSPARCEvent(unittest.TestCase):

    def test_event(self):
        event = load_weather_message('test_data/WeatherEvent.txt')
        weatherevent = WeatherEvent([16, event])
        weatherevent.uploadCode = 'WTR'
        eventdata = weatherevent.parseMessage()

if __name__ == '__main__':
    unittest.main()
