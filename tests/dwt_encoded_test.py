import unittest
import numpy as np
import idwt.encoded as enc

class TestEncoded(unittest.TestCase):

    def setUp(self):
        pass

    def t_algo(self):
        coefs = [
            np.array([1.1, 0.5]),
            np.array([0.1, 0., 1.7, 0.1222]),
            np.array([1.2, 0.212, 0.123, 0.1234])
        ]
        encoded = enc.WaveEncoded.fromEncoded(2, 2, 4, enc.Mode.fromString('db1'), 2)
        encoded.addQuadro(coefs)
        encoded.saveToFile('result/bla.dwt')

        ne = enc.WaveEncoded.fromFile('result/bla.dwt')
        self.assertEqual(encoded.totalAmostras, 8)


if __name__ == '__main__':
    unittest.main() 