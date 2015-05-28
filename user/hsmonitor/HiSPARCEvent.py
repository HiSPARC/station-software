"""Process the CIC event message from a buffer."""

import struct
from datetime import datetime
from zlib import compress

from Event import BaseHiSPARCEvent
from legacy import unpack_legacy_message
import EventExportValues


class HiSPARCEvent(BaseHiSPARCEvent):

    def __init__(self, message):
        """Proceed to unpack the message."""
        super(HiSPARCEvent, self).__init__(message)

        # init the trigger rate attribute
        self.eventrate = 0

    def parseMessage(self):
        # get database flags
        tmp = struct.unpack("B", self.message[0:1])[0]
        if tmp <= 3:
            unpack_legacy_message(self)
        else:
            self.unpackMessage()

        # get all event data necessary for an upload.
        self.export_values = EventExportValues.export_values[self.uploadCode]

        return self.getEventData()

    def unpackMessage(self):
        """Unpack an event message.

        This routine unpacks a buffer message written by the LabVIEW DAQ
        software version 3.0 and above. Version 2.1.1 doesn't use a version
        identifier in the message. By including one, we can account for
        different message formats.

        Hopefully, this code is cleaner and thus easier to understand than
        the legacy code. However, you'll always have to be careful with the
        format strings.

        """
        # Initialize sequential reading mode
        self.unpackSeqMessage()

        self.version, self.database_id, self.data_reduction, \
            self.eventrate, self.num_devices, self.length, \
            gps_second, gps_minute, gps_hour, gps_day, gps_month, gps_year, \
            self.nanoseconds, self.time_delta, \
            trigger_pattern, slv_comparators, _zero_padding = \
            self.unpackSeqMessage('>2BBfBH5BH2LHBB')

        # Try to handle NaNs for eventrate. These are handled differently from
        # platform to platform (i.e. MSVC libraries are screwed). This
        # platform-dependent fix is not needed in later versions of Python.
        # So, drop this in the near future!
        if str(self.eventrate) in ['-1.#IND', '1.#INF']:
            self.eventrate = 0

        # Add slave comparators to the trigger pattern
        # Shift by 16 to add it as bits 16-19 of the trigger pattern.
        self.trigger_pattern = trigger_pattern + (slv_comparators << 16)

        self.datetime = datetime(gps_year, gps_month, gps_day,
                                 gps_hour, gps_minute, gps_second)

        # Length of a single trace
        l = self.length / 2

        # Read out and save traces and calculated trace parameters
        self.mas_stdev1, self.mas_stdev2, self.mas_baseline1, \
            self.mas_baseline2, self.mas_npeaks1, self.mas_npeaks2, \
            self.mas_pulseheight1, self.mas_pulseheight2, self.mas_int1, \
            self.mas_int2, mas_tr1, mas_tr2 = \
            self.unpackSeqMessage('>8H2L%ds%ds' % (l, l))

        self.mas_tr1 = compress(self.unpack_trace(mas_tr1))
        self.mas_tr2 = compress(self.unpack_trace(mas_tr2))

        # Read out and save slave data as well, if available
        if self.num_devices > 1:
            self.slv_stdev1, self.slv_stdev2, self.slv_baseline1, \
                self.slv_baseline2, self.slv_npeaks1, self.slv_npeaks2, \
                self.slv_pulseheight1, self.slv_pulseheight2, self.slv_int1, \
                self.slv_int2, slv_tr1, slv_tr2 = \
                self.unpackSeqMessage('>8H2L%ds%ds' % (l, l))

            self.slv_tr1 = compress(self.unpack_trace(slv_tr1))
            self.slv_tr2 = compress(self.unpack_trace(slv_tr2))

    def unpack_trace(self, raw_trace):
        """Unpack a trace.

        Traces are stored in a funny way. We have a 12-bit ADC, so two
        datapoints can (and are) stored in 3 bytes. This function unravels
        traces again.

        The for loop loops over sets of 3 bytes. It takes the first and
        adds the first half of the second byte (by masking it with
        `bin(240) = 11110000`) to it as the four least significant bits.
        The first byte is shifted 4 bits to the left and the masked
        second four to the right. The second half of the second byte is
        then taken (maked by 00001111) and shifted by a byte and added
        to the third byte. For example: `00101001 10000110 01000111` is
        turned into `001010011000` (664) and `011001000111` (1607).

        DF: I'm wondering: does the LabVIEW program work hard to accomplish
        this? If so, why do we do this in the first place? The factor 1.5
        in storage space is hardly worth it, especially considering the
        fact that this is only used in the temporary buffer.

        DF: This is legacy code. I've never tried to understand it and will
        certainly not touch it until I do.

        """
        n = len(raw_trace)
        if n % 3 != 0:
            # return None
            raise Exception("Blob length is not divisible by 3!")
        a = struct.unpack("%dB" % n, raw_trace)
        trace = []
        for i in xrange(0, n, 3):
            trace.append((a[i] << 4) + ((a[i + 1] & 240) >> 4))
            trace.append(((a[i + 1] & 15) << 8) + a[i + 2])
        trace_str = ""
        for i in trace:
            trace_str += str(i) + ","

        return trace_str
