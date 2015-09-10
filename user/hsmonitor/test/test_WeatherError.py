import sys
sys.path.append("..")
import unittest

from WeatherError import WeatherError

from load_message import load_weather_message


class TestHiSPARCConfig(unittest.TestCase):

    def test_error(self):
        error = load_weather_message('test_data/WeatherError.txt')
        weathererror = WeatherError([17, error])
        weathererror.uploadCode = 'WER'
        errordata = weathererror.parseMessage()


if __name__ == '__main__':
    unittest.main()
