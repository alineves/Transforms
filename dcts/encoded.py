import numpy as np
import math

class WaveEncoded:
    encodedData = []
    tamanhoQuadro = 0
    qtdDescartes = 0
    qtQuadros = 0
    totalAmostras = 0

    def __init__(self, encodedData, tamanhoQuadro, totalAmostras):
        self.encodedData = encodedData
        self.tamanhoQuadro = tamanhoQuadro
        self.totalAmostras = totalAmostras
        self.qtdDescartes = 0
        self.qtQuadros = math.ceil(totalAmostras / tamanhoQuadro)
    
    @classmethod
    def comAmostrasDescartadas(cls, encodedData, tamanhoQuadro, totalAmostras, qtdDescartes):
        encoded = cls(encodedData, tamanhoQuadro, totalAmostras)
        encoded.qtdDescartes = qtdDescartes
        encoded._preencherQuadros()
        return encoded
    
    def _preencherQuadros(self):
        if self.qtdDescartes == 0:
            return
        
        zeros = np.zeros(self.qtdDescartes)
        posicao_zeros_relativa = self.tamanhoQuadro - self.qtdDescartes
        for i in range(0, self.qtQuadros):
            pos = i * self.tamanhoQuadro + posicao_zeros_relativa
            self.encodedData = np.insert(self.encodedData, pos, zeros)


    def descartar(self, qtdDescartes):
        self.qtdDescartes = qtdDescartes
    
    def getDados(self):
        return self.encodedData
    
    def getDadosComprimidos(self):
        ret = np.zeros(self.qtQuadros * (self.tamanhoQuadro - self.qtdDescartes))
        for i in range(0, self.qtQuadros):
            init = i * self.tamanhoQuadro
            end = init + self.tamanhoQuadro - self.qtdDescartes

            retInit = i * (self.tamanhoQuadro - self.qtdDescartes)
            retEnd = retInit + self.tamanhoQuadro - self.qtdDescartes
            ret[retInit : retEnd] = self.encodedData[init : end]
        return ret