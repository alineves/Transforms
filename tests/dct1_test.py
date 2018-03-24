import unittest
import numpy as np
import dcts.dct1 as dct1
import dcts.codec as codec

class TestDct1(unittest.TestCase):

    def setUp(self):
        pass

    def test_encode_dct1(self):
        encoded = codec.encode(np.array([1, 2, 3, 4, 1, 2, 3, 4]), 2, 2, dct1)
        self.assertTrue(np.array_equal(np.rint(encoded.getData()).astype(int), [15, -4, 0, -1, 15, -4, 0, -1]))

    def test_encode_com_tamanho_nao_divisivel_dct1(self):
        encoded = codec.encode(np.array([1, 2, 3, 4, 1, 2]), 2, 2, dct1)
        self.assertTrue(np.array_equal(np.rint(encoded.getData()).astype(int), [15, -4, 0, -1, 5,  3, -1, -3]))

    def test_decode_dct1(self):
        encoded = codec.encode(np.array([1, 2, 3, 4, 1, 2, 3, 4]), 2, 2, dct1)
        decodec = codec.decode(encoded.getData(), 2, 2, dct1)
        self.assertTrue(np.array_equal(np.rint(decodec).astype(int), [1, 2, 3, 4, 1, 2, 3, 4]))

    def _test_decode_depois_descarte_dct1(self):
        encoded = codec.encode(np.array([1, 2, 3, 4, 1, 2, 3, 4]), 2, 2, dct1)
        encoded.descartar(2)
        decodec = codec.decode(encoded.getData(), 2, 2, dct1)
        self.assertTrue(np.array_equal(np.rint(decodec).astype(int), [1, 2, 3, 4, 1, 2, 3, 4]))



if __name__ == '__main__':
    unittest.main()