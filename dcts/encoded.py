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
        self.qtQuadros = math.ceil(len(encodedData) / tamanhoQuadro)
    
    def descartar(self, qtdDescartes):
        self.qtdDescartes = qtdDescartes
    
    def getData(self):
        ret = np.zeros(self.qtQuadros * (self.tamanhoQuadro - self.qtdDescartes))
        for i in range(0, self.qtQuadros):
            init = i * self.tamanhoQuadro
            end = init + self.tamanhoQuadro - self.qtdDescartes

            retInit = i * (self.tamanhoQuadro - self.qtdDescartes)
            retEnd = retInit + self.tamanhoQuadro - self.qtdDescartes
            ret[retInit : retEnd] = self.encodedData[init : end]
        return ret