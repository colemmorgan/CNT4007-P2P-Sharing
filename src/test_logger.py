import unittest
import os
from logger import Logger

class TestLogger(unittest.TestCase):
    def setUp(self):
        self.test_id = 3333
        # temp log file for testing
        self.log_file = f"log_peer_{self.test_id}.log"
        
        #remove if already exists
        if os.path.exists(self.log_file):
            os.remove(self.log_file)
        self.logger = Logger(self.test_id)

    def tearDown(self):
        #clean all the handlers
        for handler in self.logger.logger.handlers[:]:
            handler.close()
            self.logger.logger.removeHandler(handler)
        
        # remove temp log
        if os.path.exists(self.log_file):
            os.remove(self.log_file)

    def test_write_log(self):
        #log some messages
        self.logger.log_made_connection(8888)
        self.logger.log_choked(1323)

        #make sure it wrote
        self.assertTrue(os.path.exists(self.log_file))

        #make sure outputs are right
        with open(self.log_file, 'r') as f:
            content = f.read()

            self.assertTrue("makes a connection to Peer 8888." in content)
            self.assertTrue("is choked by 1323." in content)
            self.assertTrue("]: Peer 3333" in content)

if __name__ == '__main__':
    unittest.main()