def getNumeroDCT():
    return 99

def matchNumeroDCT(numeroDCT):
    return numeroDCT == 99

def calculaBase(amostrasPorQuadro):
    return 2

def encode(quadro, base):
    return quadro * base + 1

def decode(quadro, base):
    return (quadro - 1)/ base