"""Process the ERR event message from a buffer."""

from datetime import datetime

from Event import BaseHiSPARCEvent


class HiSPARCError(BaseHiSPARCEvent):

    def unpackMessage(self):
        """Unpack an error message.

        This routine unpacks the error messages written to the buffer by the
        LabVIEW DAQ software.

        """
        # Initialize sequential reading mode
        self.unpackSeqMessage()

        self.version, self.database_id, \
            gps_second, gps_minute, gps_hour, gps_day, gps_month, gps_year = \
            self.unpackSeqMessage('>2B5BH')

        self.datetime = datetime(gps_year, gps_month, gps_day,
                                 gps_hour, gps_minute, gps_second)

        self.nanoseconds = 0

        self.error_message = self.unpackSeqMessage('LVstring')[0]
