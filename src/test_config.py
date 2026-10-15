import unittest
import os
from config import create_common_cfg, create_peer_info


class TestConfig(unittest.TestCase):
    def setUp(self):
        # create temp config file
        self.config_file = 'test_config.cfg'
        with open(self.config_file, 'w') as f:
            f.write("NumberOfPreferredNeighbors 2\n")
            f.write("UnchokingInterval 5\n")
            f.write("OptimisticUnchokingInterval 15\n")
            f.write("FileName test_file.dat\n")
            f.write("FileSize 100000\n")
            f.write("PieceSize 32678\n")
        self.peer_file = 'test_peer_info.cfg'
        # create temp peer info
        with open(self.peer_file, 'w') as f:
            f.write("1001 lin114-00.cise.ufl.edu 6001 1\n")
            f.write("1002 lin114-01.cise.ufl.edu 6002 0\n")

    def tearDown(self):

        # remove files when done testing
        os.remove(self.config_file)
        os.remove(self.peer_file)

    def test_create_common_config(self):
        #make sure its created and parsed well
        config = create_common_cfg(self.config_file)
        self.assertEqual(config.num_preferred_neighbors, 2)
        self.assertEqual(config.unchoking_interval, 5)
        self.assertEqual(config.optimistic_unchoking_interval, 15)
        self.assertEqual(config.file_name, 'test_file.dat')
        self.assertEqual(config.file_size, 100000)
        self.assertEqual(config.piece_size, 32678)
        self.assertEqual(config.num_pieces, 4) 

    def test_peer_info(self):

        #make sure peer info is parsed correctly
        peer_info = create_peer_info(self.peer_file)
        self.assertEqual(len(peer_info), 2)
        self.assertEqual(peer_info[0].peer_id, 1001)
        self.assertEqual(peer_info[0].host_name, 'lin114-00.cise.ufl.edu')
        self.assertEqual(peer_info[0].listening_port, 6001)
        self.assertTrue(peer_info[0].has_file)
        self.assertEqual(peer_info[1].peer_id, 1002)
        self.assertFalse(peer_info[1].has_file)

if __name__ == '__main__':
    unittest.main()