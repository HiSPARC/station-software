import sys
sys.path.append("..")
import unittest

from WeatherConfig import WeatherConfig

from load_message import load_weather_message


class TestHiSPARCError(unittest.TestCase):

    def test_config(self):
        config = load_weather_message('test_data/WeatherConfig.txt')
        weatherconfig = WeatherConfig([18, config])
        weatherconfig.uploadCode = 'WCG'
        configdata = weatherconfig.parseMessage()


if __name__ == '__main__':
    unittest.main()
