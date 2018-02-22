import unittest
import numpy as np
import dcts.encoded as enc

class TestEncoded(unittest.TestCase):

    def setUp(self):
        pass

    def test_descarte(self):
        encoded = enc.WaveEncoded(np.array([1, 2, 3, 4, 1, 2, 3, 4]), 4)
        encoded.descartar(2)
        self.assertTrue(np.array_equal(encoded.getData(), [1, 2, 1, 2]))

    def test_descarte_apos_outro_descarte(self):
        encoded = enc.WaveEncoded(np.array([1, 2, 3, 4, 1, 2, 3, 4]), 4)
        encoded.descartar(3)
        encoded.getData()
        encoded.descartar(1)
        self.assertTrue(np.array_equal(encoded.getData(), [1, 2, 3, 1, 2, 3]))


if __name__ == '__main__':
    unittest.main()