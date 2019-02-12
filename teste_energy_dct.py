import dcts.wave as wv
import dcts.codec as codec
import dcts.encoded_sorted_energy as enc
import numpy as np
import dcts.dct1 as dct1
import dcts.dct2 as dct2
import dcts.dct3 as dct3
import dcts.dct4 as dct4
import time
import os
from shutil import copyfile

codec.addAlg(dct1)
codec.addAlg(dct2)
codec.addAlg(dct3)
codec.addAlg(dct4)

prefixoNome = "f0001038.16k.q20ms.dct2.sorted0.s0"
os.makedirs('./result/' + prefixoNome)
origem = "f0001038.16k.WAV"
copyfile("./waves/" + origem, "./result/%s/%s" % (prefixoNome, origem))

def current_milli_time():
    return int(round(time.time() * 1000))

fs, audData = wv.open_wave("./waves/" + origem)

b = current_milli_time()
encoded = codec.encodeEnergy(audData, fs, 0.02, dct2, sobreposicao=0)
a = current_milli_time()
print('Tempo de encode: ', a - b)

encoded.setPorcentagemDescarte(0)

b = current_milli_time()
rest = codec.decodeEnergy(encoded)
a = current_milli_time()
print('Tempo de decode: ', a - b)

#Arquivo comprimido
encoded.saveToFile("./result/%s/encoded.dwt" % prefixoNome)

#Arquivo recuperado
wv.save_wave("./result/%s/recuperado-memoria.wav" % prefixoNome, fs, rest, 16)

#Recuperando dados comprimidos a partir do arquivo salvo
newEncoded = enc.WaveEncoded.fromFile("./result/%s/encoded.dwt" % prefixoNome)
#Recuperando amostras a partir dos dados comprimidos restaurados do arquivo
restarquivo = codec.decodeEnergy (newEncoded)

#Arquivo recuperado sobre newEncoded
wv.save_wave("./result/%s/recuperado-arquivo.wav" % prefixoNome, fs, restarquivo, 16)
