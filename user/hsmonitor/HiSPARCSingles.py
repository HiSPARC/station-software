"""Process the singles event message from a buffer."""

from datetime import datetime

from Event import BaseHiSPARCEvent


class HiSPARCSingles(BaseHiSPARCEvent):

    def unpackMessage(self):
        """Unpack a singles message.

        This routine unpacks a singles message from the buffer database.

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

        self.mas_ch1_low, self.mas_ch1_high, \
            self.mas_ch2_low, self.mas_ch2_high, \
            self.slv_ch1_low, self.slv_ch1_high, \
            self.slv_ch2_low, self.slv_ch2_high = self.unpackSeqMessage('>8I')
