"""Process the satellites event message from a buffer."""

from datetime import datetime

from Event import BaseHiSPARCEvent


class HiSPARCSatellites(BaseHiSPARCEvent):

    def unpackMessage(self):
        """Unpack a satellites message.

        This routine unpacks a satellites message from the buffer database.

        These message are sent every 59 minutes and contain a summary of
        the gps performance, the min, mean, and max number of satellites and
        the min, mean, and max combined signal strength of the satellite
        signals.

        """
        # Initialize sequential reading mode
        self.unpackSeqMessage()

        self.version, self.database_id, \
            gps_second, gps_minute, gps_hour, gps_day, gps_month, gps_year = \
            self.unpackSeqMessage('>2B5BH')

        self.datetime = datetime(gps_year, gps_month, gps_day,
                                 gps_hour, gps_minute, gps_second)

        self.nanoseconds = 0

        self.device_id = self.unpackSeqMessage('>B')

        # The mean values are split over two bytes, the first byte
        # contains the integral part (0-99) and the second byte the
        # fractional part of the value (00-99), so divide it by 100.
        self.min_n, mean_n_integral, mean_n_fractional, self.max_n, \
            self.min_signal,  mean_signal_integral, mean_signal_fractional, \
            self.max_signal = self.unpackSeqMessage('>8B')

        if mean_n_fractional > 99 or mean_signal_fractional > 99:
            raise Exception("Invalid value for fractional part of value ")

        self.mean_n = mean_n_integral + mean_n_fractional / 100.
        self.mean_signal = mean_signal_integral + mean_signal_fractional / 100.
