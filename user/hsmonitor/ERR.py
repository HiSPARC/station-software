"""Process the ERR event message from a buffer."""

__author__ = "thevinh"
__date__ = "$17-sep-2009"

from datetime import datetime

from HiSparc2Event import HiSparc2Event


class ERR(HiSparc2Event):
    def __init__(self, message):
        """Proceed to unpack the message."""
        # invoke constructor of parent class
        HiSparc2Event.__init__(self, message)

    def unpackMessage(self):
        """Unpack a buffer error message.

        This routine unpacks the error messages written to the buffer by the
        LabVIEW DAQ software.

        """

        # Initialize sequential reading mode
        self.unpackSeqMessage()

        self.version, self.database_id, gps_second, gps_minute, gps_hour, \
        gps_day, gps_month, gps_year = self.unpackSeqMessage('>2B5BH')

        self.datetime = datetime(gps_year, gps_month, gps_day,
                                 gps_hour, gps_minute, gps_second)

        self.nanoseconds = 0

        self.error_message, = self.unpackSeqMessage('LVstring')
