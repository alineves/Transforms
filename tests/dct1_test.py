import unittest
import numpy as np
import dcts.dct1 as dct1
import dcts.codec as codec

class TestDct1(unittest.TestCase):

    def setUp(self):
        pass

    def test_encode_dct1(self):
        encoded = codec.encode(np.array([1, 2, 3, 4, 1, 2, 3, 4]), 2, 2, dct1)
        self.assertTrue(np.array_equal(np.rint(encoded).astype(int), [15, -4, 0, -1, 15, -4, 0, -1]))

    def test_decode_dct1(self):
        encoded = codec.encode(np.array([1, 2, 3, 4, 1, 2, 3, 4]), 2, 2, dct1)
        decodec = codec.decode(encoded, 2, 2, dct1)
        self.assertTrue(np.array_equal(np.rint(decodec).astype(int), [1, 2, 3, 4, 1, 2, 3, 4]))



if __name__ == '__main__':
    unittest.main()