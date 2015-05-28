import sys
sys.path.append("..")
import unittest
import struct

from HiSPARCEvent import HiSPARCEvent


class TestHiSPARCEvent(unittest.TestCase):

    def test_unpack_trace(self):
        """Test unpacking a trace

        Example trace from station 508 event 1432684741282735016 detector 4.

        """
        trace = [189, 197, 188, 198, 190, 196, 189, 199, 193, 249, 443,
                 1098, 1753, 2393, 2709, 3014, 3125, 3243, 3203, 3168,
                 3022, 2932, 2761, 2621, 2411, 2266, 2083, 1910, 1696,
                 1489, 1275, 1167, 1053, 968, 855, 783, 680, 654, 604,
                 595, 531, 509, 464, 457, 415, 409, 370, 380, 356, 354,
                 326, 343, 319, 324, 304, 305, 286, 299, 286, 306, 289,
                 314, 305, 314, 300, 300, 276, 284, 272, 286, 266, 265,
                 248, 253, 242, 257, 249, 251, 237, 247, 235, 248, 237,
                 248, 237, 247, 239, 245, 237, 253, 235, 250, 241, 239,
                 226, 230, 218, 236, 218, 231, 214, 225, 209, 219, 215,
                 227, 217, 224, 222, 260, 242, 241, 225, 226, 210, 226,
                 221, 228, 216, 226, 210, 217, 205, 218, 213, 222, 209,
                 214, 198, 211, 207, 216, 203, 218, 206, 232, 224, 229,
                 220, 230, 221, 235, 225, 229, 222, 235, 225, 229, 212,
                 227, 216, 230, 220, 220, 206, 207, 192, 200, 197, 215]

        byte_trace = []
        for i in xrange(0, len(trace), 2):
            # First byte of the first 12 bits
            byte_trace.append(trace[i] >> 4)
            # Last 4 bits the first 12 bits and first 4 bits of second 12 bits
            byte_trace.append(((trace[i] & 15) << 4) + (trace[i + 1] >> 8))
            # Last byte of the second 12 bits
            byte_trace.append(trace[i + 1] & 255)

        packed_trace = struct.pack('%dB' % (len(trace) / 2 * 3), *byte_trace)
        unpacked_trace = HiSPARCEvent.unpack_trace(packed_trace)
        self.assertEqual(trace, [int(x) for x in unpacked_trace.split(',') if not x == ''])


if __name__ == '__main__':
    unittest.main()
