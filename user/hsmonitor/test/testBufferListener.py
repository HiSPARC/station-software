import sys
sys.path.append("../src")
import unittest
from Interpreter import Interpreter
from StorageManager import StorageManager
from BufferListener import BufferListener

class TestBufferListener(unittest.TestCase):
    def setUp(self):
        self.dbdict = {}
        # get the information from configuration file
        self.dbdict['host'] = "localhost"
        self.dbdict['user'] = "buffer"
        self.dbdict['password'] = "PLACEHOLDER"
        self.dbdict['db'] = "buffer"
        self.dbdict['poll_interval'] = 5
        self.dbdict['poll_limit'] = 100
        self.dbdict['keep_buffer_data'] = 0
        
        # setup storagemanager
        self.sm = StorageManager(2)
        self.interpreter = Interpreter(self.sm)
        self.bufferLis = BufferListener(self.dbdict, self.interpreter)
        
    def tearDown(self):
        # get the number of events in the buffer
        #self.TotalEvents = self.bufferLis.getMessageCount()
        self.TotalEvents1 = 0

    def testConnection(self):
        self.conn = self.bufferLis.getDBConnection(self.dbdict)
        self.assert_(self.conn is not None)

    def testGetMessages(self):
        self.msgs = self.bufferLis.getBufferMessages()
        self.msgs1 = self.bufferLis.getBufferMessages()
        # test the numbers
        self.assertEqual(len(self.msgs), self.dbdict['poll_limit'])
        self.assertEqual(len(self.msgs1), self.dbdict['poll_limit'])

    def testClearMessages(self):
        self.event_ids = []
        self.msgs = self.bufferLis.getBufferMessages()
        for msg in self.msgs:
            self.event_ids.append(msg[2])
        self.TotalEvents = self.bufferLis.getMessageCount()
        self.bufferLis.clearBufferMessages(self.event_ids)
        self.TotalEvents1 = self.bufferLis.getMessageCount()
        self.assertEqual(len(self.event_ids), self.TotalEvents - self.TotalEvents1)

if __name__ == '__main__':
    unittest.main()
