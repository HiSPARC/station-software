"""Process the CMP event message from a buffer."""

__author__="thevinh"
__date__ ="$17-sep-2009"

from datetime import datetime

from HiSparc2Event import HiSparc2Event

class CMP(HiSparc2Event):
    def __init__(self, message):
        """Proceed to unpack the message."""
        # invoke constructor of parent class
        HiSparc2Event.__init__(self, message)

    def unpackMessage(self):
        """Unpack a comparator message.
        
        This routine unpacks a comparator message from the buffer database.
        
        """
        # Initialize sequential reading mode
        self.unpackSeqMessage()

        self.version, self.database_id, \
        gps_second, gps_minute, gps_hour, gps_day, gps_month, gps_year, \
        self.nanoseconds, self.cmp_device, self.cmp_comparator, \
        self.cmp_count_over_threshold = self.unpackSeqMessage('>2B5BHL2BL')

        try:
            self.datetime = datetime(gps_year, gps_month, gps_day,
                                     gps_hour, gps_minute, gps_second)
        except ValueError:
            # In some version of DAQ/FPGA, GPS timestamps are zeroed out.
            # Make sure we have something intelligible, while also raising
            # a red flag.
            self.datetime = datetime(1900, 1, 1, 0, 0, 0)
