import unittest
import numpy as np
import dcts.dct2 as dct2
import dcts.codec as codec

class TestDct2(unittest.TestCase):

    def setUp(self):
        pass

    def test_encode_dct2(self):
        encoded = codec.encode(np.array([1, 2, 3, 4, 1, 2, 3, 4]), 2, 2, dct2)
        self.assertTrue(np.allclose(encoded.getDadosComprimidos(), [20, -6.30864406, 0, -0.448341529, 20, -6.30864406, 0, -0.448341529]))

if __name__ == '__main__':
    unittest.main()