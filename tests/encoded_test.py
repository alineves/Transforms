import unittest
import numpy as np
import dcts.encoded as enc

class TestEncoded(unittest.TestCase):

    def setUp(self):
        pass

    def test_descarte(self):
        encoded = enc.WaveEncoded(np.array([1, 2, 3, 4, 1, 2, 3, 4]), 4, 8)
        encoded.descartar(2)
        self.assertTrue(np.array_equal(encoded.getDadosComprimidos(), [1, 2, 1, 2]))
        self.assertEqual(encoded.totalAmostras, 8)

    def test_descarte_apos_outro_descarte(self):
        encoded = enc.WaveEncoded(np.array([1, 2, 3, 4, 1, 2, 3, 4]), 4, 8)
        encoded.descartar(3)
        encoded.getDadosComprimidos()
        encoded.descartar(1)
        self.assertTrue(np.array_equal(encoded.getDadosComprimidos(), [1, 2, 3, 1, 2, 3]))

    def test_com_amostras_descartadas(self):
        encoded = enc.WaveEncoded.comAmostrasDescartadas(np.array([1, 2, 3, 1, 2, 3]), 4, 8, 1)
        self.assertTrue(np.array_equal(encoded.getDadosComprimidos(), [1, 2, 3, 1, 2, 3]))
        self.assertTrue(np.array_equal(encoded.getDados(), [1, 2, 3, 0, 1, 2, 3, 0]))

    def test_com_amostras_descartadas_caso2(self):
        encoded = enc.WaveEncoded.comAmostrasDescartadas(np.array([1, 2, 1, 2]), 4, 8, 2)
        self.assertTrue(np.array_equal(encoded.getDados(), [1, 2, 0, 0, 1, 2, 0, 0]))
        self.assertTrue(np.array_equal(encoded.getDadosComprimidos(), [1, 2, 1, 2]))


if __name__ == '__main__':
    unittest.main()