import dcts.wave as wv
import dwt.codec as codec
import dwt.encoded as enc
import numpy as np
import time
import os
from shutil import copyfile

def current_milli_time():
    return int(round(time.time() * 1000))

prefixoNome = "f0001038.16k.q20ms.coif3.dec3.removeCd0a1.s20"
os.makedirs('./result/' + prefixoNome)
origem = "f0001038.16k.WAV"
copyfile("./waves/" + origem, "./result/%s/%s" % (prefixoNome, origem))



#Le dados do arquivo
fs, audData = wv.open_wave('./waves/' + origem)

#Aplica dwt(encode) e retorna objeto com todos 
b = current_milli_time()
encoded = codec.encodeRemoveCD(audData, fs, 0.02, 'coif3', 3, sobreposicao=20)
a = current_milli_time()
print('Tempo de encode: ', a - b)

encoded.removerCDs(0, 1)

#Recuperando amostras a partir dos dados comprimidos em memoria
b = current_milli_time()
rest = codec.decode(encoded) #aplica IDWT (decode) e retorna amostras recuperadas
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
