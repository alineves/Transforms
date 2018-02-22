import unittest
import numpy as np
import dcts.codec as cd
import mock_alg

class TestCodec(unittest.TestCase):

    def setUp(self):
        pass

    def test_codec(self):
        result = cd.codec(np.array([1, 2, 3, 4, 1, 2, 3, 4]), 4, mock_alg.encode, mock_alg.calculaBase)
        self.assertTrue(np.array_equal(result, [3, 5, 7, 9, 3, 5, 7, 9]))
    
    def test_codec_total_amostras_nao_divisivel_tamanho_quadro(self):
        result = cd.codec(np.array([1, 2, 3, 4, 1, 2, 3]), 4, mock_alg.encode, mock_alg.calculaBase)
        self.assertTrue(np.array_equal(result, [3, 5, 7, 9, 3, 5, 7, 1]))
    
    def test_encode(self):
        result = cd.encode(np.array([1, 2, 3, 4, 1, 2, 3]), 2, 2, mock_alg)
        self.assertTrue(np.array_equal(result.getData(), [3, 5, 7, 9, 3, 5, 7, 1]))
    def test_decode(self):
        result = cd.decode(np.array([3, 5, 7, 9, 3, 5, 7, 1]), 2, 2, mock_alg)
        self.assertTrue(np.array_equal(result, [1, 2, 3, 4, 1, 2, 3, 0]))


if __name__ == '__main__':
    unittest.main()