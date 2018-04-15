import unittest
import numpy as np
import dcts.codec as cd
import dcts.dct1 as dct1
import dcts.encoded_sorted_energy as enc
import mock_alg

class TestCodec(unittest.TestCase):

    def setUp(self):
        cd.addAlg(dct1)
        pass
    
    def test_encodeEnergy(self):
        result = cd.encodeEnergy(np.array([1, 2, 3, 4, 1, 2, 3, 4]), 2, 2, mock_alg)
        self.assertTrue(np.array_equal(result.getDados(), [3, 5, 7, 9, 3, 5, 7, 9]))

    def test_encodeEnergy_com_eliminacao(self):
        result = cd.encodeEnergy(np.array([1, 2, 3, 4, 1, 2, 3, 4]), 2, 2, mock_alg)
        result.setPorcentagemDescarte(0.5)
        self.assertTrue(np.array_equal(result.getDados(), [0, 0, 7, 9, 0, 0, 7, 9]))

    def test_encodeEnergy_desordenado_com_eliminacao(self):
        result = cd.encodeEnergy(np.array([3, 2, 1, 4, 1, 4, 2, 3]), 2, 2, mock_alg)
        result.setPorcentagemDescarte(0.5)
        self.assertTrue(np.array_equal(result.getDados(), [7, 0, 0, 9, 0, 9, 0, 7]))

    def test_decodeEnergy_com_eliminacao(self):
        cd.addAlg(mock_alg)
        encoded = enc.WaveEncoded.fromEncoded(2, 8, 4, 99)
        encoded.addQuadro([7, 5, 3, 9])
        encoded.addQuadro([3, 9, 5, 7])
        encoded.setPorcentagemDescarte(0.5)

        result = cd.decodeEnergy(encoded)
        self.assertTrue(np.array_equal(result, [3, -0.5, -0.5, 4, -0.5, 4, -0.5, 3]))

    def test_encodeEnergy_dct1(self):
        encoded = cd.encodeEnergy(np.array([1, 2, 3, 4, 1, 2, 3, 4]), 2, 2, dct1)
        encoded.setPorcentagemDescarte(0.5)
        self.assertTrue(np.allclose(encoded.getDados(), [15, -4, 0, 0, 15, -4, 0, 0]))

    def test_encodeEnergy_dct1(self):
        encoded = cd.encodeEnergy(np.array([1, 2, 3, 4, 1, 2, 3, 4]), 2, 2, dct1)
        encoded.setPorcentagemDescarte(0.5)
        
        result = cd.decodeEnergy(encoded)
        self.assertTrue(np.allclose(result, [1.1666667, 1.8333333, 3.1666667, 3.8333333, 1.1666667, 1.8333333, 3.1666667, 3.8333333]))

    def test_encodeEnergy_dct1_sobreposto(self):
        encoded = cd.encodeEnergy(np.array([1, 2, 3, 4, 1, 2, 3, 4]), 2, 2, dct1, 2)
        self.assertTrue(np.allclose(encoded.getDados(), [15, -4, 0, -1, 15, 4, 0, -5, 15, -4, 0, -1]))

if __name__ == '__main__':
    unittest.main()