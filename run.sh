#!/bin/bash

IFS=","
while read -a line; do
    filename=${line[0]}
    sobreposicao=${line[1]}
    descartes=${line[2]}
    files=$(stat --printf="%s" waves/$filename)

    
    python encode.py waves/$filename $descartes $sobreposicao result/$filename.sdct1 result/$filename.semsalvar.s$sobreposicao.$descartes.wav
    nf=result/$filename.s$sobreposicao.$descartes.wav
    python decode.py result/$filename.sdct1 $nf

    dcts=$(stat --printf="%s" result/$filename.sdct1)
    peaq=$(peaq waves/$filename $nf)
    odg=$(echo "$peaq" | grep Difference | sed "s/.*: //g")
    di=$(echo "$peaq" | grep Index | sed "s/.*: //g")
    calc=$(bc <<< "scale = 10; ($files -$dcts) / $files")
    echo "$filename,$files,$sobreposicao,$descartes,$dcts,$odg,$di,$calc"
done <  teste.csv