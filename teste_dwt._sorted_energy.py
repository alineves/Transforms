import dcts.wave as wv
import dwt.codec as codec
import dwt.encoded_sorted_energy as enc
import numpy as np
import time
import os
from shutil import copyfile

def current_milli_time():
    return int(round(time.time() * 1000))

prefixoNome = "f0001038.16k.q20ms.db10.dec3.sorted50.s0"
os.makedirs('./result/' + prefixoNome)
origem = "f0001038.16k.WAV"
copyfile("./waves/" + origem, "./result/%s/%s" % (prefixoNome, origem))

fs, audData = wv.open_wave("./waves/" + origem)

b = current_milli_time()
encoded = codec.encode(audData, fs, 0.02, 'db10', 3, sobreposicao=0)
a = current_milli_time()
print('Tempo de encode: ', a - b)
print("quantidadeQuadros", encoded.quantidadeQuadros())
encoded.setPorcentagemDescarte(0.5)

b = current_milli_time()
rest = codec.decode(encoded)
a = current_milli_time()
print('Tempo de decode: ', a - b)

#Arquivo comprimido
encoded.saveToFile("./result/%s/encoded.dwt" % prefixoNome)

#Arquivo recuperado
wv.save_wave("./result/%s/recuperado-memoria.wav" % prefixoNome, fs, rest, 16)

#Recuperando dados comprimidos a partir do arquivo salvo
newEncoded = enc.WaveEncoded.fromFile("./result/%s/encoded.dwt" % prefixoNome)
#Recuperando amostras a partir dos dados comprimidos restaurados do arquivo
restarquivo = codec.decode(newEncoded)

#Arquivo recuperado sobre newEncoded
wv.save_wave("./result/%s/recuperado-arquivo.wav" % prefixoNome, fs, restarquivo, 16)