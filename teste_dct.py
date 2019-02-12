import dcts.wave as wv
import dcts.codec as codec
import dcts.encoded as enc
import numpy as np
import dcts.dct1 as dct1
import dcts.dct2 as dct2
import dcts.dct3 as dct3
import dcts.dct4 as dct4
import time
import os
from shutil import copyfile

def current_milli_time():
    return int(round(time.time() * 1000))

prefixoNome = "f0001038.16k.q20ms.dct2.descarta160.s160"
os.makedirs('./result/' + prefixoNome)
origem = "f0001038.16k.WAV"
copyfile("./waves/" + origem, "./result/%s/%s" % (prefixoNome, origem))

fs, audData = wv.open_wave("./waves/f0001038.16k.WAV")

b = current_milli_time()
encoded = codec.encode(audData, fs, 0.02, dct2, 160)
a = current_milli_time()
print('Tempo de encode: ', a - b)

encoded.descartar(160)
#Arquivo comprimido
encoded.saveToFile("./result/%s/encoded.dct" % prefixoNome)

b = current_milli_time()
decoded = codec.decodeFromEncoded(encoded, dct2)
a = current_milli_time()
print('Tempo de decode: ', a - b)

#Arquivo recuperado
wv.save_wave("./result/%s/recuperado-memoria.wav" % prefixoNome, fs, decoded, 16)

#Recuperando dados comprimidos a partir do arquivo salvo
newEncoded = enc.WaveEncoded.loadFromFile("./result/%s/encoded.dct" % prefixoNome)
#Recuperando amostras a partir dos dados comprimidos restaurados do arquivo
newdecoded = codec.decodeFromEncoded(newEncoded, dct2)

#Arquivo recuperado sobre newEncoded
wv.save_wave("./result/%s/recuperado-arquivo.wav" % prefixoNome, fs, newdecoded, 16)
